#!/usr/bin/env python
# encoding: utf-8
"""
dataset.py : Interaction with DSS datasets
Copyright (c) 2013-2014 Dataiku SAS. All rights reserved.
"""

import json
import os
from os import path as osp
import pandas as pd
import sys
import csv
import atexit
import time
from platform_exec import open_dku_stream, read_dku_json, DKUOutStream
import warnings
import numpy as np
import requests
import threading
import dku_pandas_csv
from dkujson import dump_to_filepath, load_from_filepath
import codecs
from itertools import izip_longest
from dateutil import parser as date_iso_parser
import struct
import Queue
import threading, logging

if sys.version_info<(2,7,6):
    # Python < 2.7.6 doesn't support writing a bytearray in a cStringIO
    from StringIO import StringIO
else:
    from cStringIO import StringIO

FULL_SAMPLING = {"samplingMethod": "FULL"}


def parse_iso_date(s):
    if s == "":
        return None
    else:
        return date_iso_parser.parse(s)

# Loads the export button in IPython.
try:
    from ..notebook import export
    export.setup()
except:
    pass

FLOW = None
if "DKUFLOW_SPEC" in os.environ:
    FLOW = json.loads(os.environ["DKUFLOW_SPEC"])

# ---------------------------
#
# Example content of FLOW
#
#    {
#       "in":[
#          {
#             "name":"datasetname",
#             "partitions":[
#                part1,
#                part2,
#                part3
#             ]
#          }
#       ],
#       "out":[{
#             "name":"datasetname",
#             "partition":"part",
#             "path":path
#          }, ...
#        ]
#    }


DEFAULT_TIMEOUT = 30

if FLOW is not None:
    # Timeout has been introduced to cope with ipython leaks.
    # As a default value, we have an infinite timeout when in flow.
    DEFAULT_TIMEOUT = -1

# We want to stderr something on DeprecationWarning
warnings.resetwarnings()


DKU_PANDAS_TYPES_MAP = {
    'int': np.int32,
    'bigint': np.int64,
    'float': np.float32,
    'double': np.float64,
    'boolean': np.bool
}


# used to stream typed fields in iter_tuples.
CASTERS = {
    "int": int,
    "bigint": int,
    "float": float,
    "double": float,
    "date": parse_iso_date,
    "boolean": bool
}


PANDAS_DKU_TYPES_MAP = {
    'int64': 'bigint',
    'float64': 'double',
    'float32': 'float',
    'int32': 'int',
    'object': 'string',
    'int': 'int',
    'float': 'float',
    'bool': 'boolean',
    }

# TODO Use a proper directory pattern here,
# and default to the env variable?
#
# Environment variable can get ugly especially
# when unit testing


def unique(g):
    vals = set()
    for val in g:
        if val not in vals:
            yield val
            vals.add(val)


def set_dip_home(dip_home):
    os.environ['DIP_HOME'] = dip_home


def get_dip_home():
    return os.environ['DIP_HOME']

def get_shared_secret():
    with open('%s/shared-secret.txt' % get_dip_home(), 'r') as fp:
        secret = fp.read()
        return secret.strip()

def none_if_throws(f):
    def aux(*args, **kargs):
        try:
            return f(*args, **kargs)
        except:
            return None
    return aux


(GENERATING,              # underlying  generator is currently working
 IDLE,                    # waiting for the generator user to call .next()
 TIMEOUT_REACHED,         # timeout has been reached
 END_OF_ITERATOR,
 TERMINATED,) = range(5)  # we reached the generator last element.


class IteratorWithTimeOut(object):

    __slots__ = ('generator', 'state', 'timeout',
                 'wake_me_up', 'touched', 'iterator', )

    def __init__(self, iterator, timeout=-1):
        self.iterator = iterator
        self.state = IDLE
        self.timeout = timeout
        self.touched = True
        self.wake_me_up = threading.Event()

    def check_timeout(self,):
        while self.state != TERMINATED:
            if self.touched is False and self.state == IDLE:
                # reached timeout !
                self.state = TIMEOUT_REACHED
                # closing underlying iterator right away
                self.iterator.close()
                # terminating the thread
                break
            if self.state == IDLE:
                self.touched = False
            self.wake_me_up.wait(self.timeout)

    def iterate(self,):
        if self.timeout > 0:
            timeout_thread = threading.Thread(target=self.check_timeout)
            timeout_thread.daemon = True
            timeout_thread.start()
        try:
            while True:
                self.state = GENERATING
                val = self.iterator.next()
                self.state = IDLE
                yield val
                self.touched = True
                if self.state == TIMEOUT_REACHED:
                    # we didn't reach the end of the file
                    # we returned because of the timeout.
                    raise StopIteration("Timeout Reached")
        finally:
            if self.state != TIMEOUT_REACHED:
                # we are here, either because
                # we reached the end of the stream
                # or the stream rose an exception.
                self.state = TERMINATED
                self.wake_me_up.set()


class Schema(list):
    def __init__(self, data):
        list.__init__(self, data)

    def _repr_html_(self,):
        s = "<table>"
        s += "<tr><th>Column</th><th>Type</th></tr>"
        for col in self:
            s += "<tr><td>%s</td><td>%s</td></tr>" % (col["name"], col["type"])
        s += "</table>"
        return s


def default_project_key():
    if "DKU_CURRENT_PROJECT_KEY" not in os.environ:
        raise Exception("Please specify for which project key you want datasets list")
    else:
        return os.environ["DKU_CURRENT_PROJECT_KEY"]


def create_sampling_argument(sampling='head',
                             sampling_column=None,
                             limit=None,
                             ratio=None,):
    if type(sampling) == dict:
        # HACK : in the doctor we happen to have
        # the sampling in the java format already.
        # Rather than convert them twice, we
        # use this loophole and return the sampling dictionary
        # directly.
        return sampling
    if sampling_column is not None and sampling != "random-column":
        raise ValueError("sampling_column argument does not make sense with %s sampling method." % sampling)
    if sampling == "head":
        if ratio is not None:
            raise ValueError("target_ratio parameter is not supported by the head sampling method.")
        if limit is None:
            return FULL_SAMPLING
        else:
            return {
                "samplingMethod": "HEAD_SEQUENTIAL",
                "maxRecords": limit
            }
    elif sampling == "random":
        if ratio is not None:
            if limit is not None:
                raise ValueError("Cannot set both ratio and limit.")
            return {
                "samplingMethod": "RANDOM_FIXED_RATIO",
                "targetRatio": ratio
            }
        elif limit is not None:
            return {
                "samplingMethod": "RANDOM_FIXED_NB",
                "maxRecords": limit
            }
        else:
            raise ValueError("Sampling method random requires either a parameter limit or ratio")
    elif sampling == "random-column":
        if sampling_column is None:
            raise ValueError("random-column sampling method requires a sampling_column argument.")
        if ratio is not None:
            raise ValueError("ratio parameter is not handled by sampling column method.")
        if limit is None:
            raise ValueError("random-column requires a limit parameter")
        return {
            "samplingMethod": "COLUMN_BASED",
            "maxRecords": limit,
            "column": sampling_column
        }
    else:
        raise ValueError("Sampling %s is unsupported" % sampling)


class Dataset:
    """This is a handle to obtain readers and writers on a dataiku Dataset.
    From this Dataset class, you can:

    * Read a dataset as a Pandas dataframe
    * Read a dataset as a chunked Pandas dataframe
    * Read a dataset row-by-row
    * Write a pandas dataframe to a dataset
    * Write a series of chunked Pandas dataframes to a dataset
    * Write to a dataset row-by-row
    * Edit the schema of a dataset"""

    @staticmethod
    def list(project_key=None):
        """Lists the names of datasets. If project_key is None, the current
        project key is used."""
        project_key = project_key or default_project_key()
        datasets = []
        path = osp.join(get_dip_home(), "config", "projects", project_key, "datasets")
        for jsonFile in os.listdir(path):
            if jsonFile.endswith('.json'):
                json = load_from_filepath(osp.join(path, jsonFile))
                if not json:
                    print >>sys.stderr, "Unable to read", jsonFile
                    continue
                try:
                    datasets.append(json['name'])
                except KeyError:
                    print >>sys.stderr, "Error on", jsonFile
        return datasets

    def get_filepath(self,):
        relpath = "projects/%s/datasets/%s.json" % (self.project_key, self.short_name)
        if FLOW is not None:
            # When in flow, the dataset config is copied
            # in a separate directory to avoid
            # possible interaction with other scripts.
            return os.path.join(FLOW["localConfigPath"], relpath)
        else:
            # ... in other case, we directly read the dataset conf
            #dataset_relpath = "config/projects/%s/datasets/%s.json" % (self.project_key, self.short_name)
            return osp.join(os.environ["DIP_HOME"], "config", relpath)

    def __init__(self, name, project_key=None):
        self.name = name
        self.cols = None
        self.read_partitions = None
        self.writePartition = None
        self.writable = False
        self.readable = False

        if FLOW is not None:
            # Spec:
            #  { "in" : [ {"name" : "datasetname", "partitions" : [part1, part2, part3} ],
            #    "out" : [ { "name" : "datasetname", "partition" : "part", "path" : path } ]
            print "In Flow mode, checking if I can access this dataset: %s" % json.dumps(FLOW)
            for input_dataset in FLOW["in"]:
                if input_dataset["smartName"] == self.name or input_dataset["fullName"] == self.name:
                    self.readable = True
                    self.name = input_dataset["fullName"]
                    if "partitions" in input_dataset:
                        self.read_partitions = input_dataset["partitions"]
            for outputDataset in FLOW["out"]:
                if outputDataset["smartName"] == self.name or outputDataset["fullName"] == self.name:
                    self.name = outputDataset["fullName"]
                    self.writable = True
                    if "partition" in outputDataset:
                        self.writePartition = outputDataset["partition"]
            if not self.readable and not self.writable:
                raise Exception("Dataset %s cannot be used : declare it as input or output of your recipe" % self.name)
            (self.project_key, self.short_name) = self.name.split(".", 1)
        else:
            if "." not in name:
                try:
                    self.project_key = project_key or default_project_key()
                    self.short_name = name
                    self.name = self.project_key + "." + name
                except:
                    raise Exception("Dataset %s is specified with a relative name, "
                                    "but no default project was found. Please use complete name" % self.name)
            else:
                # use gave a full name
                (self.project_key, self.short_name) = self.name.split(".", 1)
                if project_key is not None and self.project_key != project_key:
                    raise ValueError("Project key %s incompatible with fullname dataset %s." % (project_key, name))
            if not osp.exists(self.get_filepath()):
                raise Exception("Dataset '%s' doesn't exist (%s)" % (name, self.get_filepath()))
            self.readable = True
            self.writable = True

    @property
    def full_name(self,):
        return self.project_key + "." + self.short_name

    def _repr_html_(self,):
        s = "Dataset[   <b>%s</b>   ]</br>" % self.name
        s += self.read_schema()._repr_html_()
        return s

    def dataset_filepath(self,):
        relative_filepath = "config/projects/%s/datasets/%s.json" % (self.project_key, self.short_name)
        return osp.join(get_dip_home(), relative_filepath)

    def set_write_partition(self,spec):
        """Sets which partition of the dataset gets written to when
        you create a DatasetWriter. Setting the write partition is
        not allowed in Python recipes, where write is controlled by
        the Flow."""
        if FLOW is not None:
            raise Exception("You cannot explicitely set partitions when "
                            "running within Dataiku Flow")
        self.writePartition = spec

    def add_read_partitions(self, spec):
        """Add a partition or range of partitions to read.

        The spec argument must be given in the DSS partition spec format.
        You cannot manually set partitions when running inside
        a Python recipe. They are automatically set using the dependencies.


        """
        if FLOW is not None:
            raise Exception("You cannot explicitely set partitions when "
                            "running within Dataiku Flow")
        if self.read_partitions is None:
            self.read_partitions = []
        self.read_partitions.append(spec)

    def addReadPartitions(self, *args, **kwargs):
        warnings.warn("Use add_read_partitions instead", DeprecationWarning)
        self.add_read_partitions(*args, **kwargs)

    def readSchema(self):
        warnings.warn("Use add_read_partitions instead", DeprecationWarning)
        return self.read_schema()

    def read_schema(self, raise_if_empty=True):
        """Gets the schema of this dataset, as an array of column names"""
        if self.cols is None:

            if FLOW is None:
                port = os.getenv('DKU_BACKEND_PORT')
                apiPath = "dip/api/streaming"
            else:
                port = FLOW["jekPort"]
                apiPath = "kernel/streaming"

            resp = requests.post("http://127.0.0.1:%s/%s/get-schema/"%(port,apiPath), data={
                "fullDatasetName": self.full_name
            }, headers = {"X-DKU-IPythonSharedSecret": get_shared_secret()})

            if resp.status_code==200:
                self.cols = json.loads(resp.text).get("columns")
            else:
                json_data = resp.text
                err_msg = 'No error message available. Check full logs.'
                if json_data:
                    err_msg = json.loads(json_data).get("message",err_msg)
                print 'Unable to fetch schema for %s : %s'%(self.name,err_msg)

        if raise_if_empty and len(self.cols) == 0:
            raise Exception(
                "No column in schema of %s."
                " Have you set up the schema for this dataset?" % self.name)
        return Schema(self.cols,)

    def dku_dump_args(self, sampling=None, columns=None):
        args = ["dataset-dump", "-d", "\t", "--style", "excel"]
        if columns is not None:
            args += ["-c", ",".join(columns)]
        args += ["--sampling", json.dumps(sampling)]
        args += [self.name]
        if self.read_partitions is not None:
            for p in self.read_partitions:
                args.append("-p")
                args.append(p)
        return args

    def get_dataframe(self,
                      columns=None,
                      sampling='head',
                      sampling_column=None,
                      limit=None,
                      ratio=None,
                      infer_with_pandas=True,
                      parse_dates=True,):
        """Read the dataset (or its selected partitions, if applicable)
        as a Pandas dataframe.

        Pandas dataframes are fully in-memory, so you need to make
        sure that your dataset will fit in RAM before using this.

        Keywords arguments:

        * columns -- When not None, returns only the given list of columns (default None)
        * limit -- Limits the number of rows returned (default None)
        * sampling -- Sampling method, if:

                * 'head' returns the first rows of the dataset. Incompatible with ratio parameter.
                * 'random' returns a random sample of the dataset
                * 'random-column' returns a random sample of the dataset. Incompatible with limit parameter.

        * sampling_column -- Select the column used for "columnwise-random" sampling (default None)
        * ratio -- Limits the ratio to at n% of the dataset. (default None)
        * infer_with_pandas -- uses the types detected by pandas rather than the dataset schema as detected in DSS. (default True)
        * parse_dates -- Date column in DSS's dataset schema are parsed  (default True)

        Inconsistent sampling parameter raise ValueError.

        Note about encoding:

            * Column labels are "unicode" objects
            * When a column is of string type, the content is made of utf-8 encoded "str" objects
        """
        (names, dtypes, parse_date_columns) = self._get_dataframe_schema(
            columns=columns,
            parse_dates=parse_dates,
            infer_with_pandas=infer_with_pandas)
        with self._stream(infer_with_pandas=infer_with_pandas,
                          sampling=sampling,
                          sampling_column=sampling_column,
                          limit=limit,
                          ratio=ratio,
                          columns=columns) as dku_output:
            return pd.read_table(dku_output,
                                 names=names,
                                 dtype=dtypes,
                                 header=None,
                                 sep='\t',
                                 doublequote=True,
                                 quotechar='"',
                                 parse_dates=parse_date_columns)

    def asDataFrame(self, infer_with_pandas=True,):
        warnings.warn("Use get_dataframe instead", DeprecationWarning)
        return self.get_dataframe(infer_with_pandas)

    def _stream(self,
                infer_with_pandas=True,
                sampling="head",
                sampling_column=None,
                limit=None,
                ratio=None,
                columns=None):
        if not self.readable:
            raise Exception("You cannot read dataset %s, "
                            "it is not declared as an input" % self.name)
        if FLOW is not None:
            add_env = {"DKU_FLOW": "1"}
        else:
            add_env = {}
        sampling_params = create_sampling_argument(
            sampling=sampling,
            sampling_column=sampling_column,
            limit=limit,
            ratio=ratio,)
        dku_dump_args = self.dku_dump_args(sampling=sampling_params, columns=columns)
        return open_dku_stream(dku_dump_args, add_env=add_env)

    def _get_dataframe_schema(self,
                              columns=None,
                              parse_dates=True,
                              infer_with_pandas=False):
        names = []
        dtypes = {}
        schema = self.read_schema()
        for col in schema:
            n = col["name"]
            t = col["type"]
            if t in DKU_PANDAS_TYPES_MAP:
                dtypes[n] = DKU_PANDAS_TYPES_MAP[t]
            else:
                dtypes[n] = np.object_
            names.append(n)
        if columns is not None:
            columns = list(unique(columns))
            names = columns
            dtypes = {
                column_name: column_type
                for (column_name, column_type) in dtypes.iteritems()
                if column_name in columns
            }

        # if parse_dates is set to True,
        # list up the index of the columns set up as dates by DSS
        # and forward them to pandas.
        if parse_dates is True:
            parse_dates = [
                col_id
                for (col_id, col_schema) in enumerate(self.read_schema())
                if col_schema["type"] == "date" and (columns is None or col_id in columns)
            ]
            if len(parse_dates) == 0:
                parse_dates = False
        if infer_with_pandas:
            dtypes = None
        return (names, dtypes, parse_dates)

    def iter_dataframes(self,
                        chunksize=10000,
                        infer_with_pandas=True,
                        sampling="head",
                        sampling_column=None,
                        parse_dates=True,
                        limit=None,
                        ratio=None,
                        columns=None):
        """Read the dataset to Pandas dataframes by chunks of fixed size.

        Returns a generator over pandas dataframes.

        Useful is the dataset doesn't fit in RAM."""
        if not self.readable:
            raise Exception("You cannot read dataset %s, "
                            "it is not declared as an input" % self.name)
        (names, dtypes, parse_date_columns) = self._get_dataframe_schema(
            columns=columns,
            parse_dates=parse_dates,
            infer_with_pandas=infer_with_pandas)
        with self._stream(infer_with_pandas=infer_with_pandas,
                          sampling=sampling,
                          sampling_column=sampling_column,
                          limit=limit,
                          ratio=ratio,
                          columns=columns) as dku_output:
            df_it = pd.read_table(
                dku_output,
                dtype=dtypes,
                names=names,
                low_memory=True,
                header=None,
                sep='\t',
                doublequote=True,
                chunksize=chunksize,
                iterator=True)
            for df in df_it:
                yield df

    def asStream(self):
        warnings.warn("Use iter_rows or iter_tuples instead",
                      DeprecationWarning)
        return self.iter_tuples()

    def writeFromDataFrame(self, df):
        warnings.warn("Use write_from_dataframe instead", DeprecationWarning)
        self.write_from_dataframe(df)

    def write_with_schema(self, df):
        """Writes this dataset (or its target partition, if applicable) from
        a single Pandas dataframe.

        This variant replaces the schema of the output dataset with the schema
        of the dataframe.

        Encoding node: strings MUST be in the dataframe as UTF-8 encoded str objects.
        Using unicode objects will fail.
        """
        if not hasattr(df, "to_csv"):
            raise ValueError("Method write_with_schema expects a "
                             "dataframe as argument. You gave a %s" %
                             (df is None and "None" or df.__class__))
        self.write_schema(get_schema_from_df(df))
        self.write_from_dataframe(df)

    def _out_stream(self,):
        return DKUOutStream(["dataset-write", self.name])

    def write_from_dataframe(self, df, infer_schema=False, write_direct=False):
        """Writes this dataset (or its target partition, if applicable) from
        a single Pandas dataframe.

        This variant does not edit the schema of the output dataset, so you must
        take care to only write dataframes that have a compatible schema.
        Also see "write_with_schema".

        Encoding node: strings MUST be in the dataframe as UTF-8 encoded str objects.
        Using unicode objects will fail.

        arguments:
        df -- input panda dataframe.
        """
        if not hasattr(df, "to_csv"):
            raise ValueError("Method write_from_dataframe expects a "
                             "dataframe as argument. You gave a %s" %
                             (df is None and "None" or df.__class__))
        if not self.writable:
            raise Exception("You cannot write dataset %s, "
                            "it is not decalred as an output" % self.name)
        try:
            if infer_schema:
                self.write_schema_from_dataframe(df)

            with self.get_writer() as writer:
                writer.write_dataframe(df)

        except AttributeError as e:
            raise TypeError("write_from_dataframe is a expecting a "
                            "DataFrame object. You provided a " +
                            df.__class__.__name__, e)

    def iter_rows(self,
                  sampling='head',
                  sampling_column=None,
                  limit=None,
                  ratio=None,
                  log_every=-1,
                  timeout=DEFAULT_TIMEOUT):
        """Returns a generator on the rows (as a dict-like object) of the
        data (or its selected partitions, if applicable)

        Keyword arguments:
        * limit -- maximum number of rows to be emitted
        * log_every -- print out the number of rows read on stdout

        Field values are casted according to their types.
        String are parsed into "unicode" values.
        """
        col_names = [col["name"] for col in self.read_schema()]
        col_idx = {
            col_name: col_id
            for (col_id, col_name) in enumerate(col_names)
        }
        for row_tuple in self.iter_tuples(sampling=sampling,
                                          sampling_column=sampling_column,
                                          limit=limit,
                                          ratio=ratio,
                                          log_every=log_every,
                                          timeout=timeout):
            yield DatasetCursor(row_tuple, col_names, col_idx)

    def _iter_tuples_no_timeout(self,
                                sampling=None,
                                log_every=-1,
                                columns=None):
        """
        Same as iter_tuples but without the timeout.
        """
        if not self.readable:
            raise Exception("You cannot read dataset %s, it is "
                            "not declared as an input" % self.name)
        schema = self.read_schema()
        casters = [
            CASTERS.get(col["type"], lambda s:s)
            for col in schema
        ]
        dku_dump_args = self.dku_dump_args(sampling=sampling, columns=columns)
        if FLOW is not None:
            add_env = {"DKU_FLOW": "1"}
        else:
            add_env = {}
        with open_dku_stream(dku_dump_args, add_env=add_env) as dku_output:
            count = 0
            for row_tuple in UnicodeReader(dku_output,
                                           delimiter='\t',
                                           quotechar='"',
                                           doublequote=True):
                yield [none_if_throws(caster)(val)
                       for (caster, val) in izip_longest(casters, row_tuple)]
                count += 1
                if log_every > 0 and count % log_every == 0:
                    print "Dataset<%s> - read %i lines" % (self.name, count)

    def iter_tuples(self,
                    sampling='head',
                    sampling_column=None,
                    limit=None,
                    ratio=None,
                    log_every=-1,
                    timeout=DEFAULT_TIMEOUT,
                    columns=None):
        """ Returns the rows of the dataset as tuples.
        The order and type of the values are the same are matching
        the dataset's parameter

        Keyword arguments:

        * limit -- maximum number of rows to be emitted
        * log_every -- print out the number of rows read on stdout
        * timeout -- time (in seconds) of inactivity  after which
          we want to close the generator if nothing has been read. Without it notebooks typically tend to leak "DKU" processes.

        Field values are casted according to their types.
        String are parsed into "unicode" values.
        """
        sampling_params = create_sampling_argument(
            sampling=sampling,
            sampling_column=sampling_column,
            limit=limit,
            ratio=ratio,)
        generator = self._iter_tuples_no_timeout(sampling=sampling_params,
                                                 log_every=log_every,
                                                 columns=columns)
        val_it = IteratorWithTimeOut(iterator=generator,
                                     timeout=timeout).iterate()
        while True:
            yield val_it.next()

    def rowAsDict(self, row):
        warnings.warn("Use iter_rows", DeprecationWarning)
        cols = self.read_schema()
        out = {}
        for i in range(len(row)):
            out[cols[i]["name"]] = row[i]
        return out

    def getWriter(self):
        warnings.warn("Use get_writer instead", DeprecationWarning)
        return self.get_writer()

    def get_writer(self):
        """Get a stream writer for this dataset (or its target
           partition, if applicable). The writer must be closed as soon as you don't need it."""
        return DatasetWriter(self,)

    def write_schema(self, columns):
        """Write the dataset schema into the dataset JSON
        definition file.

        Sometimes, the schema of a dataset being written is
        known only by the code of the Python script itself.
        In that case, it can be useful for the Python script
        to actually modify the schema of the dataset.
        Obviously, this must be used with caution.
        'columns' must be an array of dicts like
        { 'name' : 'column name', 'type' : 'column type'}
        """
        if not self.writable:
            raise Exception("You cannot write the schema for the dataset %s, "
                            "as it is not declared as an output" % self.name)
        for column in columns:
            if "type" not in column:
                raise Exception("Columns %s has no attribute type"
                                % str(column))
            if "name" not in column:
                raise Exception("Columns %s has no attribute name"
                                % str(column))
            if not isinstance(column['name'], basestring):
                raise Exception("Columns %s name attribute is not a string"
                                % str(column))
            if not isinstance(column['type'], basestring):
                raise Exception("Columns %s type attribute is not a string"
                                % str(column))

        if FLOW is None:
            port = os.getenv('DKU_BACKEND_PORT')
            apiPath = "dip/api/streaming"
        else:
            port = FLOW["jekPort"]
            apiPath = "kernel/streaming"

        requests.post("http://127.0.0.1:%s/%s/set-schema/"%(port,apiPath), data={
            "fullDatasetName": self.full_name,
            "schemaData": json.dumps({
                "userModified": "false",
                "columns": columns
            })
        }, headers = {"X-DKU-IPythonSharedSecret": get_shared_secret()})
        self.cols = None

    def write_schema_from_dataframe(self, df):
        self.write_schema(get_schema_from_df(df))

    def writeSchema(self, columns):
        warnings.warn("Use write_schema instead", DeprecationWarning)
        self.write_schema(columns)

    def _getJSON(self):
        return load_from_filepath(self.get_filepath())

    def _writeJSON(self, obj):
        return dump_to_filepath(self.get_filepath(), obj)


class DatasetCursor(object):
    """ A dataset cursor that helps iterating on
        rows.
    """

    __slots__ = ('_col_idx', '_col_names', '_val')

    def __init__(self, val, col_names, col_idx):
        self._col_idx = col_idx
        self._col_names = col_names
        self._val = val

    def __getitem__(self, col_name):
        try:
            col_id = self._col_idx.get(col_name)
            return self._val[col_id]
        except KeyError:
            raise KeyError("Column '%s' is not declared in the schema"
                           % col_name)
        except IndexError:
            raise KeyError("CSV file number of column does not match. Expected"
                           " %i, got %i" %
                           (len(self._col_names, len(self._val))))

    def __len__(self,):
        return len(self._col_idx)

    def __iter__(self,):
        return iter(self._col_names)

    def __contains__(self, k):
        return k in self._col_idx

    def column_id(self, name,):
        return self._col_idx.get(name)

    def keys(self,):
        return self._col_names

    def items(self,):
        return zip(self._col_names, self._val)

    def values(self,):
        return self._val

    def __repr__(self,):
        return repr(dict(self.items()))

    def get(self, col_name, default_value=None):
        if col_name in self._col_idx:
            col_id = self._col_idx.get(col_name)
            return self._val[col_id]
        else:
            return default_value

class TimeoutExpired(Exception):
    pass

class TimeoutableQueue(Queue.Queue):
    def __init__(self,size):
        Queue.Queue.__init__(self,size)

    # Return when :
    # - The queue is empty
    # - The timeout expired (without raising!)
    def join_with_timeout(self, timeout):
        self.all_tasks_done.acquire()
        try:
            endtime = time.time() + timeout
            while self.unfinished_tasks:
                remaining = endtime - time.time()
                if remaining <= 0.0:
                    raise TimeoutExpired
                self.all_tasks_done.wait(remaining)
        finally:
            self.all_tasks_done.release()


# Send data over HTTP using chunked encoding.
class RemoteStreamWriter(threading.Thread):

    def __init__(self,id,waiter):
        self.id = id
        self.error_message = None
        self.waiter = waiter
        self.chunk_queue_size = 10
        self.chunk_size = 5000000 # 5MN seems to be the best (both 1MB & 10MB are slower)
        self.queue = TimeoutableQueue(self.chunk_queue_size)
        self.buffer = StringIO()
        self.end_mark = self
        self.streaming_api = StreamingAPI()
        threading.Thread.__init__(self)
        self.daemon = True
        self.start()

    def _check_health(self):
        if self.error_message:
            raise Exception(self.error_message)
        if not self.queue:
            raise Exception("Stream has been closed")


    def read(self):
        raise Exception("Don't call me baby")

    def flush(self):
        self._check_health()
        if self.buffer.tell()>0:
            self.queue.put(self.buffer.getvalue())
            self.buffer = StringIO()
        while True:
            q = self.queue
            if not q:
                break
            try:
                q.join_with_timeout(1000)
                break
            except TimeoutExpired:
                continue

        if self.error_message:
            raise Exception(self.error_message)


    def write(self, data):
        self._check_health()
        self.buffer.write(data)
        if self.buffer.tell() > self.chunk_size:
            self.flush()

    def close(self):
        self._check_health()
        self.queue.put(self.end_mark)
        self.flush()
        if self.error_message:
            raise Exception(self.error_message)

    def _generate(self):
        while True:
            if not self.waiter.is_still_alive():
                logging.info("Write session has been interrupted")
                return
            logging.info("Waiting for data to send ...")
            try:
                item = self.queue.get(True,10)
            except Queue.Empty:
                # no, no ! empty chunks are forbidden by the HTTP spec  !
                #yield ''
                logging.info("No data to send, waiting more...")
                continue
            if item is self.end_mark:
                logging.info("Got end mark, ending send")
                break
            else:
                logging.info("Sending data (%s)" % len(item))
                yield item
                self.queue.task_done()

    def run(self):
        try:
            print 'Initializing data stream (%s)'%self.id
            self.streaming_api.push_data(self.id,self._generate())
            self.queue.task_done()
        except Exception as e:
            self.error_message = 'Error : %s'%e
        finally:
            self.queue = None


import pprint
# Wrap API call to the streaming API. It is implemented by DatasetWritingService in the backend.
class StreamingAPI:

    def __init__(self):
        if FLOW is None:
            port = os.getenv('DKU_BACKEND_PORT')
            apiPath = "dip/api/streaming"
            self.activity_id = ""
        else:
            port = FLOW["jekPort"]
            apiPath = "kernel/streaming"
            self.activity_id = FLOW["currentActivityId"]
        self.base_url = "http://127.0.0.1:%s/%s"%(port,apiPath)
        self.headers = {"X-DKU-IPythonSharedSecret": get_shared_secret()}

    def init_write_session(self,request):
        request["activityId"] = self.activity_id
        try:
            resp = requests.post('%s/init-write-session/'%self.base_url,
                                 data={"request": json.dumps(request)},
                                 headers = self.headers)
        except Exception as e:
            raise Exception('Invalid backend response : %s'%str(e))

        # This call is NOT supposed to fail. We always get a session ID.
        # If the request is invalid, the error must be retrieved by wait_write_session()
        return json.loads(resp.text).get('id')

    def wait_write_session(self,id):
        try:
            resp = requests.get('%s/wait-write-session/'%self.base_url,params={"id": id},
                                headers = self.headers)
        except Exception as e:
            raise Exception('Invalid backend response : %s'%str(e))

        if resp.status_code == requests.codes.ok:
            decoded_resp = json.loads(resp.text)
            if decoded_resp["ok"]:
                writtenRows = decoded_resp["writtenRows"]
                print '%s rows successfully written (%s)'%(writtenRows,id)
            else:
                msg = 'An error occurred during dataset write (%s): %s'%(id.encode("utf8"), decoded_resp["message"].encode('utf-8'))
                raise Exception(msg)
        else:
            raise Exception('Invalid backend response, code %s'%resp.status_code)



    def push_data(self,id,generator):
        resp = requests.put('%s/push-data/'%self.base_url,params={"id": id},
                            headers = self.headers,data=generator)
        # We don't really care about whether this call failed or not.
        if resp.status_code != 200:
            print 'Streaming: push-data call failed with code %s'%resp.status_code

# Create a thread which is waiting for the streaming session to complete.
class WriteSessionWaiter(threading.Thread):
    def __init__(self,session_id):
        self.session_id = session_id
        self.exception = None
        self.alive = True
        self.streaming_api = StreamingAPI()
        threading.Thread.__init__(self)
        self.daemon = True
        self.start()

    def raise_on_failure(self):
        if self.exception is not None:
            raise self.exception, self.exception_type, self.traceback

    def is_still_alive(self):
        return self.alive

    def wait_end(self):
        self.join()
        self.raise_on_failure()

    def run(self):
        try:
            self.streaming_api.wait_write_session(self.session_id)
        except Exception as e:
            logging.exception("ohoho")
            self.exception, self.exception_type, self.traceback = sys.exc_info()
        finally:
            self.alive = False


def _dataset_writer_atexit_handler():
    DatasetWriter.atexit_handler()

class DatasetWriter:
    """Handle to write to a dataset. Use Dataset.get_writer() to obtain a DatasetWriter.

    Very important: a DatasetWriter MUST be closed after usage. Failure to close a
    DatasetWriter will lead to incomplete or no data being written to the output dataset
    """

    active_writers = dict()

    @staticmethod
    def atexit_handler():
        tobeclosed = []
        for k,v in DatasetWriter.active_writers.iteritems():
            print 'WARNING : A dataset writer MUST be closed (%s)'%k
            tobeclosed+=[v]
        DatasetWriter.active_writers = dict()
        for v in tobeclosed:
            v.close()

    def __init__(self,dataset):

        if DatasetWriter.active_writers.get(dataset.full_name):
            raise Exception('Unable to instanciate a new dataset writer. There is already another active writer for this dataset (%s).'%dataset.full_name)

        # The HTTP writer thread
        self.remote_writer = None

        self.streaming_api = StreamingAPI()

        # Copy the target partition ID so it can't be changed
        self.writePartition = dataset.writePartition if dataset.writePartition else ""

        # Dataset object
        self.dataset = dataset

        # By default, data schema == dataset schema
        self.data_schema = None

        # Column names
        self.column_names = None

        # Waiter thread
        self.waiter = None

        # CSV writer used for writing individual rows
        self.csv_writer = None

        # Register itself as active writer
        DatasetWriter.active_writers[dataset.full_name]= self

    # Initialize the streaming machinery the first time it is called.
    # We cannot do this before because we don't known the schema of the written data before.
    #
    # Subsequent calls will raise an exception is the stream is broken.
    def _start_once(self,data_schema=None):
        if self.waiter:
            self.waiter.raise_on_failure()

        if not self.remote_writer:
            if data_schema is not None:
                self.data_schema = data_schema
            else:
                self.data_schema = self.dataset.read_schema()

            self.column_names = [
                col["name"]
                for col in self.data_schema
            ]

            id = self.streaming_api.init_write_session({
                "dataSchema": {
                    "userModified": "false",
                    "columns": self.data_schema
                },
                "method":"STREAM",
                "partitionSpec":self.writePartition,
                "fullDatasetName":self.dataset.full_name
            })
            # Initialize a thread which is waiting for the end OR for an error to occur
            self.waiter = WriteSessionWaiter(id)

            # Initialize another thread which is in charge of streaming data to the backend
            self.remote_writer = RemoteStreamWriter(id,self.waiter)
        else:
            # TODO : check data_schema against the previous one ?
            pass


    def write_tuple(self, row):
        """Write a single row from a tuple or list of column values.
        Columns must be given in the order of the dataset schema.

        Encoding note: strings MUST be given as Unicode object. Giving str objects will
        fail.
        """
        self._start_once()
        if not self.csv_writer:
            self.csv_writer = UnicodeWriter(self.remote_writer,delimiter=',',quotechar='"',
                                            doublequote=True,lineterminator='\n')
        self.csv_writer.writerow([val if val is not None else "" for val in row])

    def write_row_array(self, row):
        # warnings.warn("Use write_tuple instead", DeprecationWarning)
        self.write_tuple(row)

    def writeRowArray(self, array):
        warnings.warn("Use write_tuple instead", DeprecationWarning)
        self.write_row_array(array)

    def write_row_dict(self, row_dict):
        """Write a single row from a dict of column name -> column value.

        Some columns can be omitted, empty values will be inserted instead.

        Encoding note: strings MUST be given as Unicode object. Giving str objects will
        fail.
        """
        self._start_once()
        if self.column_names is None:
            raise Exception("To write as a dict, you need to define the"
                            "output dataset schema beforehands.")
        out = [
            row_dict.get(column_name, "")
            for column_name in self.column_names
        ]
        self.write_tuple(out)

    def writeRowDict(self, dic):
        warnings.warn("Use write_row_dict instead", DeprecationWarning)
        self.write_row_dict(dic)

    def write_dataframe(self,df):
        """Appends a Pandas dataframe to the dataset being written.

        This method can be called multiple times (especially when you have been
        using iter_dataframes to read from an input dataset)

        Encoding node: strings MUST be in the dataframe as UTF-8 encoded str objects.
        Using unicode objects will fail.
        """
        self._start_once(get_schema_from_df(df))
        dku_pandas_csv.DKUCSVFormatter(df, self.remote_writer,
                                       index=None, header=False, sep=',',
                                       quoting=csv.QUOTE_MINIMAL,).save()

    def close(self):
        """Closes this dataset writer"""
        if DatasetWriter.active_writers.get(self.dataset.full_name) == self:
            del DatasetWriter.active_writers[self.dataset.full_name]

        self._start_once()
        self.remote_writer.flush()
        self.remote_writer.close()
        self.waiter.wait_end()

    def __enter__(self,):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

def get_schema_from_df(df):
    ''' A simple function that returns a DSS schema from
    a Pandas dataframe, to be used when writing to a dataset
    from a data frame'''
    schema = []

    if len(set(df.columns)) != len(list(df.columns)):
        raise Exception("DSS doesn't support dataframes containing multiple columns with the same name.")

    for col_name in df.columns:
        col_val = df[col_name]
        pda_col_type = str(col_val.dtype)
        column_type = {
            'name': col_name,
            'type': PANDAS_DKU_TYPES_MAP.get(pda_col_type, "string")
        }
        schema.append(column_type)
    return schema


# See https://docs.python.org/2/library/csv.html


class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """
    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")


class UnicodeReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        utf_recoded_f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(utf_recoded_f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self


class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = StringIO()
        self.writer = csv.writer(self.queue, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([unicode(s).encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)
