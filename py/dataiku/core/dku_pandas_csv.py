import csv
from pandas.core.index import Index, MultiIndex, _ensure_index
from pandas.tseries.period import PeriodIndex, DatetimeIndex
import pandas.core.common as com
import pandas.lib as lib
import numpy as np

class DKUUTF8Writer:
    """
    A CSV writer which will write rows to CSV file "f" while ensuring UTF8
    write. Supports both str-as-utf8 and unicode as input
    """
    def __init__(self, f, dialect=None, **kwds):
        self.stream = f
        self.writer = csv.writer(self.stream, dialect=dialect, **kwds)

    # This method is normally never called
    def writerow(self, row):
        row = [s.encode("utf8") is isinstance(s, unicode) for s in row]
        self.writer.writerow(row)

    def writerows(self, rows):
        # In order to support unicode input, we still need to check if
        # The passed string is a unicdoe one. It's a bit costly, but we
        # can't really avoid this.

        # Note that both writerow and writerows do modify their input.
        # It's ugly, but pandas does the same (and actually, pandas constructs)
        # the rows arrays in Cython by copying from the real Dataframe.
        for i, row in enumerate(rows):
            # It's a tiny bit faster than a list comprehension
            for j, s in enumerate(row):
                if isinstance(s, unicode):
                    rows[i][j] = s.encode("utf-8")
        self.writer.writerows(rows)

# Why we use this:
#  - When using df.to_csv(), pandas does not care at all about encoding, so
#    it can only write str (if they are utf8) and unicode-that-are-in-ascii-range
#  - When using df.to_csv(encoding=utf8), all works properly, but it uses panda's
#    check_as_is and pprint_thing method which are insanely slow.
#
# This formatter uses a unicode-aware CSV writer which supports both str-as-utf8 and
# any unicode.
#
# Approximate performance measurements:
#  - df.to_csv(): 100
#  - df.to_csv(encoding=) : 1000
#  - This method: 180
class DKUCSVFormatter(object):

    def __init__(self, obj, path_or_buf=None, sep=",", na_rep='', float_format=None,
                 cols=None, header=True, index=True, index_label=None,
                 mode='w', nanRep=None, encoding=None, quoting=None,
                 line_terminator='\n', chunksize=None,
                 tupleize_cols=False, quotechar='"', date_format=None,
                 doublequote=True, escapechar=None):

        self.obj = obj

        self.path_or_buf = path_or_buf
        self.sep = sep
        self.na_rep = na_rep
        self.float_format = float_format

        self.header = header
        self.index = index
        self.index_label = index_label
        self.mode = mode
        self.encoding = encoding

        if quoting is None:
            quoting = csv.QUOTE_MINIMAL
        self.quoting = quoting

        if quoting == csv.QUOTE_NONE:
            # prevents crash in _csv
            quotechar = None
        self.quotechar = quotechar

        self.doublequote = doublequote
        self.escapechar = escapechar

        self.line_terminator = line_terminator

        self.date_format = date_format

        self.tupleize_cols = tupleize_cols
        self.has_mi_columns = isinstance(obj.columns, MultiIndex
                                         ) and not self.tupleize_cols

        # validate mi options
        if self.has_mi_columns:
            if cols is not None:
                raise TypeError("cannot specify cols with a MultiIndex on the "
                                "columns")

        if cols is not None:
            if isinstance(cols, Index):
                cols = cols.to_native_types(na_rep=na_rep,
                                            float_format=float_format,
                                            date_format=date_format)
            else:
                cols = list(cols)
            self.obj = self.obj.loc[:, cols]

        # update columns to include possible multiplicity of dupes
        # and make sure sure cols is just a list of labels
        cols = self.obj.columns
        if isinstance(cols, Index):
            cols = cols.to_native_types(na_rep=na_rep,
                                        float_format=float_format,
                                        date_format=date_format)
        else:
            cols = list(cols)

        # save it
        self.cols = cols

        # preallocate data 2d list
        self.blocks = self.obj._data.blocks
        ncols = sum(b.shape[0] for b in self.blocks)
        self.data = [None] * ncols

        if chunksize is None:
            chunksize = (100000 / (len(self.cols) or 1)) or 1
        self.chunksize = int(chunksize)

        self.data_index = obj.index
        if isinstance(obj.index, PeriodIndex):
            self.data_index = obj.index.to_timestamp()

        if (isinstance(self.data_index, DatetimeIndex) and
                date_format is not None):
            self.data_index = Index([x.strftime(date_format)
                                     if notnull(x) else ''
                                     for x in self.data_index])

        self.nlevels = getattr(self.data_index, 'nlevels', 1)
        if not index:
            self.nlevels = 0

    def save(self):
        # create the writer & save
        if hasattr(self.path_or_buf, 'write'):
            f = self.path_or_buf
            close = False
        else:
            print "Get handle on %s" % self.path_or_buf
            f = com._get_handle(self.path_or_buf, self.mode,
                                encoding=self.encoding)
            close = True

        try:
            writer_kwargs = dict(lineterminator=self.line_terminator,
                                 delimiter=self.sep, quoting=self.quoting,
                                 doublequote=self.doublequote,
                                 escapechar=self.escapechar,
                                 quotechar=self.quotechar)
            self.writer = DKUUTF8Writer(f, **writer_kwargs)
            self._save()
        finally:
            if close:
                f.close()

    def _save_header(self):

        writer = self.writer
        obj = self.obj
        index_label = self.index_label
        cols = self.cols
        has_mi_columns = self.has_mi_columns
        header = self.header
        encoded_labels = []

        has_aliases = isinstance(header, (tuple, list, np.ndarray, Index))
        if not (has_aliases or self.header):
            return
        if has_aliases:
            if len(header) != len(cols):
                raise ValueError(('Writing %d cols but got %d aliases'
                                  % (len(cols), len(header))))
            else:
                write_cols = header
        else:
            write_cols = cols

        if self.index:
            # should write something for index label
            if index_label is not False:
                if index_label is None:
                    if isinstance(obj.index, MultiIndex):
                        index_label = []
                        for i, name in enumerate(obj.index.names):
                            if name is None:
                                name = ''
                            index_label.append(name)
                    else:
                        index_label = obj.index.name
                        if index_label is None:
                            index_label = ['']
                        else:
                            index_label = [index_label]
                elif not isinstance(index_label, (list, tuple, np.ndarray, Index)):
                    # given a string for a DF with Index
                    index_label = [index_label]

                encoded_labels = list(index_label)
            else:
                encoded_labels = []

        if not has_mi_columns:
            encoded_labels += list(write_cols)

        # write out the mi
        if has_mi_columns:
            columns = obj.columns

            # write out the names for each level, then ALL of the values for
            # each level
            for i in range(columns.nlevels):

                # we need at least 1 index column to write our col names
                col_line = []
                if self.index:

                    # name is the first column
                    col_line.append(columns.names[i])

                    if isinstance(index_label, list) and len(index_label) > 1:
                        col_line.extend([''] * (len(index_label) - 1))

                col_line.extend(columns.get_level_values(i))

                writer.writerow(col_line)

            # add blanks for the columns, so that we
            # have consistent seps
            encoded_labels.extend([''] * len(columns))

        # write out the index label line
        writer.writerow(encoded_labels)

    def _save(self):

        self._save_header()

        nrows = len(self.data_index)

        # write in chunksize bites
        chunksize = self.chunksize
        chunks = int(nrows / chunksize) + 1

        for i in range(chunks):
            start_i = i * chunksize
            end_i = min((i + 1) * chunksize, nrows)
            if start_i >= end_i:
                break

            self._save_chunk(start_i, end_i)

    def _save_chunk(self, start_i, end_i):

        data_index = self.data_index

        # create the data for a chunk
        slicer = slice(start_i, end_i)
        for i in range(len(self.blocks)):
            b = self.blocks[i]
            d = b.to_native_types(slicer=slicer, na_rep=self.na_rep,
                                  float_format=self.float_format,
                                  date_format=self.date_format)

            for col_loc, col in zip(b.mgr_locs, d):
                # self.data is a preallocated list
                self.data[col_loc] = col

        ix = data_index.to_native_types(slicer=slicer, na_rep=self.na_rep,
                                        float_format=self.float_format,
                                        date_format=self.date_format)

        lib.write_csv_rows(self.data, ix, self.nlevels, self.cols, self.writer)
