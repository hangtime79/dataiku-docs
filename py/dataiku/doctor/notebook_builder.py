# encoding: utf-8
"""
notebook_builder.py
Base classes for creating IPython notebooks
"""

from datetime import datetime
import jinja2
import re
from dataiku.doctor.modeling_project import extract_input_columns
from collections import defaultdict

ENVIRONMENT = jinja2.Environment(loader=jinja2.PackageLoader('dataiku.doctor', 'templates'))
SPLIT_PATTERN = re.compile("""((?:##[^\n]*\n)+)""")
STARTING_SHARP = re.compile("^#+")
UNCOMMENT_PATTERN = re.compile("^#+\s*")


def header_cell(msg=None, level=None):
    return {
        'cell_type': 'heading',
        'level': level,
        'metadata': {},
        'source': [msg]
    }


def comment_cell(comment):
    return {
        'cell_type': 'markdown',
        'metadata': {},
        'source': [comment]
    }


def code_cell(code):
    return {
        'cell_type': 'code',
        'collapsed': False,
        'language': 'python',
        'metadata': {},
        'outputs': [],
        'input': [code]
    }


def parse_cells_from_render(content):
    cell_contents = SPLIT_PATTERN.split(content)
    for cell_info in cell_contents:
        cell_info = cell_info.strip()
        if len(cell_info) > 0:
            m = STARTING_SHARP.search(cell_info)
            nb_sharps = 0 if m is None else len(m.group(0))
            if nb_sharps <= 1:
                yield code_cell(cell_info)
            else:
                lines = [
                    UNCOMMENT_PATTERN.sub("", line)
                    for line in cell_info.split("\n")
                ]
                msg = "\n".join(lines)
                if nb_sharps == 2:
                    yield comment_cell(comment=msg)
                else:
                    yield header_cell(msg=msg, level=nb_sharps - 2)


class NotebookBuilder(object):

    def __init__(self, bench_params, core_params, preprocessing_params, modeling_params):
        self.core_params = core_params
        self.bench_params = bench_params
        self.preprocessing_params = preprocessing_params
        self.modeling_params = modeling_params

    def is_supervized(self,):
        raise NotImplementedError()

    def title(self,):
        raise NotImplementedError()

    def template_name(self,):
        raise NotImplementedError()

    def template(self,):
        return ENVIRONMENT.get_template(self.template_name())

    def rescale_context(self,):
        return {
            feature_name: feature_params["rescaling_method"]
            for (feature_name, feature_params) in self.preprocessing_params["per_feature"].items()
            if feature_params["type"] == "NUMERIC" and feature_params["rescaling"]
        }

    def categorical_preprocessing_context(self,):
        methods = defaultdict(list)
        for fname in self.preprocessing_params["per_feature"].keys():
            fparams = self.preprocessing_params["per_feature"][fname]
            if fparams["role"] == "REJECT" or fparams["role"] == "TARGET":
                continue
            missing_method = fparams["missing_handling"]
            print missing_method
            if missing_method == "FLAG":
                continue
            if fparams["type"] == "CATEGORY":
                method = fparams["category_handling"]
                methods[method].append(fname)
            if fparams["type"] == "TEXT":
                method = fparams["text_handling"]
                methods[method].append(fname)
        return methods

    def handle_missing_context(self,):
        drop_rows_when_missing = []
        flag_when_missing = []
        impute_when_missing = []
        for (feature_name, feature_params) in self.preprocessing_params["per_feature"].items():
            if feature_params["role"] == "REJECT" or feature_params["role"] == "TARGET" or feature_params["type"] == "TEXT":
                continue
            method = feature_params["missing_handling"]
            if method == "DROP_ROW":
                drop_rows_when_missing.append(feature_name)
            elif method == "FLAG":
                flag_when_missing.append(feature_name)
            elif method == "IMPUTE":
                impute_when_missing.append({
                    "feature": feature_name,
                    "impute_with": feature_params["missing_impute_with"]
                })
        return {
            "drop_rows_when_missing": drop_rows_when_missing,
            "flag_when_missing": flag_when_missing,
            "impute_when_missing": impute_when_missing,
        }

    @property
    def algorithm(self,):
        return self.modeling_params['algorithm']

    def context(self,):
        categorical_features = []
        numerical_features = []
        text_features = []
        for (feature_name, feature_params) in self.preprocessing_params['per_feature'].iteritems():
            if feature_params['role'] not in {'REJECT', 'TARGET'}:
                if feature_params['type'] == 'NUMERIC':
                    numerical_features.append(feature_name)
                elif feature_params['type'] == 'CATEGORY':
                    categorical_features.append(feature_name)
                elif feature_params['type'] == 'TEXT':
                    text_features.append(feature_name)
        algorithm = self.algorithm
        if algorithm not in {'RANDOM_FOREST_CLASSIFICATION',
                             'SCIKIT_MODEL',
                             'LOGISTIC_REGRESSION',
                             'SVC_CLASSIFICATION',
                             'SGD_CLASSIFICATION',
                             'KMEANS',
                             'MiniBatchKMeans',
                             'SPECTRAL',
                             'WARD',
                             'DBSCAN',
                             'LEASTSQUARE_REGRESSION',
                             'RANDOM_FOREST_REGRESSION',
                             'RIDGE_REGRESSION',
                             'LASSO_REGRESSION',}:
            raise ValueError("Algorithm %s is unsupported." % algorithm)
        return {
            "title": self.title(),
            "dataset": self.dataset_fullname,
            "algorithm": algorithm,
            "enable_feature_selection": algorithm in {"RANDOM_FOREST_CLASSIFICATION", "RANDOM_FOREST_REGRESSION"},
            "now": datetime.utcnow(),
            "categorical_features": categorical_features,
            "numerical_features": numerical_features,
            "text_features": text_features,
            "input_columns": extract_input_columns(self.preprocessing_params, with_target=True),
            "handle_missing": self.handle_missing_context(),
            "categorical_processing": self.categorical_preprocessing_context(),
            "rescale_features": self.rescale_context(),
            "modeling_params": self.modeling_params,
            "reduce": self.preprocessing_params["reduce"],
            "is_supervized": self.is_supervized(),
        }

    @property
    def dataset_fullname(self,):
        print "###################"
        print self.core_params
        project_key = self.core_params["input"]["datasetProjectKey"]
        dataset_shortname = self.core_params["input"]["dataset"]
        return ".".join((project_key, dataset_shortname))

    def create_notebook(self,):
        context = self.context()
        content = self.template().render(context)
        cells = list(parse_cells_from_render(content))
        return {
            'metadata': {
                'name': self.title()
            },
            'nbformat': 3,
            'nbformat_minor': 0,
            'worksheets': [{"cells": cells}]
        }


class ClusteringNotebookBuilder(NotebookBuilder):
           
    def title(self):
        return 'Clustering %s' % self.dataset_fullname

    def template_name(self,):
        return "clustering.tmpl"

    def is_supervized(self,):
        return False

    def context(self,):
        context = NotebookBuilder.context(self,)
        context.update({
            "title": self.title(),
            "deduplication": self.preprocessing_params["deduplication"],
            "outliers": self.preprocessing_params['outliers'],
            "bench_params": self.bench_params,
            "is_kmean_like": self.algorithm in ("KMEANS", "MiniBatchKMeans"),
        })
        return context


class PredictionNotebookBuilder(NotebookBuilder):
           
    def title(self):
        return 'Predicting %s in %s' % (self.target_variable, self.dataset_fullname)

    @property
    def target_variable(self,):
        return self.core_params["target_variable"]

    @property
    def prediction_type(self,):
        return self.core_params["prediction_type"]

    def is_supervized(self,):
        return True
    
    def template_name(self,):
        if self.prediction_type == "regression":
            return "regression.tmpl"
        else:
            return "classification.tmpl"

    def context(self,):
        target_map = {}
        if "target_remapping" in self.preprocessing_params:
            target_map = self.preprocessing_params["target_remapping"]["pd"]
        context = NotebookBuilder.context(self,)
        context.update({
            "prediction_type": self.prediction_type,
            "target": self.target_variable,
            "deduplication": self.preprocessing_params["deduplication"],
            "target_map": target_map,
            "cross_val_ratio": self.core_params["crossval"]["samprate"],
        })
        return context

    def categorical_preprocessing_context(self,):
        if self.prediction_type == 'regression':
            impact_method = 'continuous'
        else:
            impact_method = 'multiple'
        context = NotebookBuilder.categorical_preprocessing_context(self,)
        context.update({"impact_method": impact_method})
        return context
