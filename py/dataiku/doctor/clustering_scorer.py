#!/usr/bin/env python
# encoding: utf-8
"""
clustering_scorer : Takes a trained clusterer, dataframe and outputs appropriate scoring data
"""

import math
import logging
from os import path as osp
from copy import deepcopy
import numpy as np
import pandas as pd
from sklearn.metrics import silhouette_score
from scipy.interpolate import interp1d
import constants
import json
from .utils import subsample
from collections import OrderedDict, Counter
from sklearn.ensemble import RandomForestClassifier
import heapq

SILHOUETTE_LIMIT = 2000
SCATTER_NPOINTS = 1000
NBOOTSTRAP = 10
GAP_STATISTIC_ENABLED = False
CLUSTER_GLOB = 'global_distribution'


def value_counts(series, n_most_common=100):
    """ Returns an ordered dict, value -> count

    Handles null. n.b. in new versions of pandas
    value_counts can handle null as well.
    """
    global_counts = Counter(dict(series.value_counts(sort=True, ascending=False).head(n_most_common)))
    global_counts[None] = series.isnull().sum()
    return OrderedDict(global_counts.most_common(n_most_common))


def no_nan(vals):
    return vals[~np.isnan(vals)]


def make_percentile(vals):
    percentile_x = np.linspace(0, 100, num=vals.shape[0])
    percentile_y = np.sort(vals)
    def aux(x):
        return float(interp1d(percentile_x, percentile_y)(x))
    return aux


class ClusteringModelScorer(object):
    def __init__(
            self,
            cluster_model,
            preprocessing_results,
            cluster_labels,
            preprocessing_params,
            run_folder):

        self.cluster_model = cluster_model
        self.preprocessing_params = preprocessing_params
        self.cluster_labels = cluster_labels
        self.train = preprocessing_results["TRAIN"]
        self.profiling_df = preprocessing_results["PROFILING"]
        self.train_prepca = preprocessing_results["TRAIN_PREPCA"]
        self.results_path = run_folder
        self.ret = {"metrics": {}}
        logging.info("MODEL SCORER ORIG_DF = %s" % self.profiling_df.columns)

    def drop_outliers(self,):
        return self.preprocessing_params["outliers"]["method"] == "drop"

    def add_metric(self, measure, value):
        self.ret["metrics"][measure] = {'measure': measure, 'value': value}

    def pk_path(self, path):
        return osp.join(self.results_path, path)

    def silhouette_score(self,):
        nb_rows = self.train.shape[0]
        if nb_rows > SILHOUETTE_LIMIT:
            # TODO check this !
            ratio = float(SILHOUETTE_LIMIT) / nb_rows
            labeled_train = self.train.join(self.cluster_labels)
            subset = subsample(labeled_train,
                               'cluster_labels',
                               sampling_type='stratified_forced',
                               ratio=ratio)
            return silhouette_score(subset.drop('cluster_labels', axis=1).values,
                                    subset['cluster_labels'].values,
                                    metric='euclidean')
        else:
            return silhouette_score(self.train.values, self.cluster_labels.values, metric="euclidean")

    def score(self):
        nb_clusters = len(np.unique(self.cluster_labels))
        if hasattr(self.cluster_model, "inertia_"):
            self.add_metric("Inertia", self.cluster_model.inertia_)
        if nb_clusters > 1:
            self.add_metric("Silhouette", self.silhouette_score())
        self.add_metric("Nb. clusters", nb_clusters)
        self.ret["variables_importance"] = self.variables_importance()
        self.update_final_dataset()
        logging.info("************************ Done final dataset, profiling_df %d %d" % (self.profiling_df.shape))
        self.cluster_labels = sorted(self.profiling_df["cluster_labels"].unique())
        self.cluster_description()
        self.cluster_profiling()
        self.cluster_summary()
        logging.info("DONE CLUSTER DESC")
        self.build_scatter()
        self.build_heatmap()
        self.build_facts()
        return self.ret

    def variables_importance(self):
        clf = RandomForestClassifier(n_estimators=100, n_jobs=-1)
        clf.fit(self.train_prepca.values, self.cluster_labels)
        features = self.train_prepca.columns
        return [
            {'variable': v, 'importance': i}
            for (v, i) in zip(features, clf.feature_importances_)
        ]

    def build_scatter(self):
        # we save a kind of stratified subsample (but not really).
        nb_lines = self.profiling_df.shape[0]
        sub = self.profiling_df
        if nb_lines > SCATTER_NPOINTS:
            logging.info("BUILD SCATTER PLOT %d %d" % self.profiling_df.shape)
            logging.info("COLS  %s" % self.profiling_df.columns)
            ratio = min(float(SCATTER_NPOINTS) / nb_lines, 1.0)
            sub = subsample(self.profiling_df,
                            variable='cluster_labels',
                            sampling_type='balanced',
                            ratio=ratio)
            logging.info("SUBSAMPLED %d %d " % sub.shape)
        sub.to_pickle(self.pk_path('scatter_sample.pkl'))

    def iter_facts(self,):
        K = 10
        profiling_df = self.profiling_df[self.nfact]
        self.cluster_dfs = {
            cluster_label: profiling_df[profiling_df["cluster_labels"] == cluster_label]
            for cluster_label in self.cluster_labels
        }
        for col_name in profiling_df.columns:
            if col_name == "cluster_labels":
                continue
            if col_name.startswith("factor_"):
                continue
            series = profiling_df[col_name]
            if float in series.dtype.type.mro():
                continue
            else:
                print col_name, series.dtype
            val_counts = value_counts(series, n_most_common=10)
            nb_rows = series.shape[0]
            # we only keep values for which we have a valid approximation
            # of the probability.
            val_counts = OrderedDict(
                (cat_value, count / float(nb_rows))
                for cat_value, count in val_counts.items()
                if count * (1 - count / float(nb_rows)) > 10.
            )
            for (category_value, global_ratio) in val_counts.items():
                for cluster_label in self.cluster_labels:
                    cluster_series = self.cluster_dfs[cluster_label][col_name]
                    if category_value is not None:
                        cluster_ratio = ((cluster_series == category_value).sum() + global_ratio * K) / float(cluster_series.shape[0] + K)
                        if cluster_ratio >= 0.3:
                            yield {
                                "type": "categorical",
                                "feature_label": col_name,
                                "cluster_label": cluster_label,
                                "category_value": category_value,
                                "global_ratio": global_ratio,
                                "current_ratio": cluster_ratio,
                                "diff": (global_ratio - cluster_ratio) / global_ratio,
                            }
        for cluster_stats in self.clusters_stats:
            for feature_stat in cluster_stats["feature_stats"]:
                if not math.isnan(feature_stat["diff"]):
                    yield feature_stat

    def build_facts(self,):
        fact_aggregators = [
            ["global", 10],
        ] + [[cluster_label, 3] for cluster_label in self.cluster_labels]
        facts = list(self.iter_facts())
        facts_selection_map = {}
        for [aggregator_key, limit] in fact_aggregators:
            if aggregator_key == "global":
                filtered_facts = facts  # [fact for fact in facts if predicate(fact)]
            else:
                filtered_facts = [fact for fact in facts if fact["cluster_label"] == aggregator_key]
            best_filtered_facts = list(heapq.nlargest(limit, filtered_facts, key=lambda x: abs(x["diff"])))
            facts_selection_map[aggregator_key] = best_filtered_facts
        facts_selection = {}
        facts_selection["global"] = {
            "size": self.profiling_df.shape[0],
            "facts": facts_selection_map["global"]
        }
        facts_selection["clusters"] = [
            {
                "cluster": cluster_label,
                "size": self.cluster_dfs[cluster_label].shape[0],
                "facts": facts_selection_map[cluster_label]
            }
            for cluster_label in self.cluster_labels
        ]
        facts_filepath = self.pk_path('facts.json')
        json.dump(facts_selection, open(facts_filepath, "w"))

    def build_heatmap(self,):
        variable_names = sorted(col
                                for col in self.profiling_df.columns
                                if self.profiling_df[col].dtype == np.float
                                and (":dummy:" not in col)
                                and (not col.startswith("factor_"))
                                )
        global_stats = {
            variable_name: {
                "label": variable_name,
                "mean": self.profiling_df[variable_name].mean(),
                "std": self.profiling_df[variable_name].std()
            }
            for variable_name in variable_names
        }

        def compute_stats(sub_df, cluster_label=None):
            feature_stats = []
            stats = {
                "size": sub_df.shape[0],
                "feature_stats": feature_stats
            }
            for variable_name in variable_names:
                variable_series = sub_df[variable_name]
                mean = variable_series.mean()
                std = variable_series.std()
                global_feature_stats = global_stats[variable_name]
                global_mean = global_feature_stats["mean"]
                global_std = global_feature_stats["std"]
                if global_std > 0.:
                    feature_stats.append({
                        "type": "numerical",
                        "feature_label": variable_name,
                        "cluster_label": cluster_label,
                        "mean": mean,
                        "std": std,
                        "diff": (((mean - global_mean) / global_std) if global_std > 0. else "NaN"),
                        "global_mean": global_mean,
                        "global_std": global_std
                    })
            return stats

        clusters_stats = []
        heatmap = {
            "cluster_labels": self.cluster_labels,
            "variable_names": variable_names,
            "clusters_stats": clusters_stats,
            "global_stats": global_stats,
            "nb_rows": self.profiling_df.shape[0]
        }
        for cluster_label in self.cluster_labels:
            cluster_df = self.profiling_df[self.profiling_df["cluster_labels"] == cluster_label]
            cluster_stats = compute_stats(cluster_df, cluster_label)
            cluster_stats["label"] = cluster_label
            clusters_stats.append(cluster_stats)
        heatmap_filepath = self.pk_path('heatmap.json')
        self.clusters_stats = clusters_stats
        json.dump(heatmap, open(heatmap_filepath, "w"))

    def update_final_dataset(self):
        cluster_labels = self.cluster_labels.map(lambda x: 'cluster_' + str(x))
        self.profiling_df = self.profiling_df.join(cluster_labels)
        if set(self.train.columns).intersection(self.profiling_df.columns):
            # there was no PCA.
            self.ret["reduce_vars"] = []
        else:
            self.ret["reduce_vars"] = list(self.train.columns)
            self.profiling_df = self.profiling_df.join(self.train)
        self.nfact = self.profiling_df.columns
        nb_outliers = self.profiling_df.shape[0] - self.train.shape[0]
        self.fact = ['cluster_labels']
        logging.info("shape of train : %i,%i" % self.train.shape)
        logging.info("shape of global dataframe : %i,%i" % self.profiling_df.shape)
        if self.drop_outliers():
            self.profiling_df['cluster_labels'].dropna(inplace=True)
        else:
            self.profiling_df['cluster_labels'].fillna(constants.CLUSTER_OUTLIERS, inplace=True)
        self.ret.update({
            "train_nb_records": self.train.shape[0],
            "train_nb_features": self.train.shape[1],
            "train_nb_outliers": nb_outliers
        })

    def cluster_summary(self,):
        summary = {}
        self.ret["summary"] = summary
        summary["clusters"] = []

    def cluster_description(self):
        logging.info("clusters list : %s" % np.unique(list(self.cluster_labels)))
        logging.info("cluster in dataframe : %s" % np.unique(list(self.profiling_df["cluster_labels"].values)))
        out_color = len(np.unique(self.cluster_labels))
        global_color = out_color + 1

        def mapcolor(x):
            if x == constants.CLUSTER_OUTLIERS:
                return out_color
            elif x == CLUSTER_GLOB:
                return global_color
            else:
                return int(str(x)[-1])

        # 1) for mean values ...
        variable_clust = []

        # add source variables
        if len(self.nfact) >= 2:  # cause 'cluster' in it anyway.
            temp = self.profiling_df[self.nfact].groupby('cluster_labels', as_index=False).mean()
            temp['color'] = temp['cluster_labels'].map(mapcolor)
            temp = temp.where(pd.notnull(temp), None)
            for v in temp.columns:
                if v not in ['cluster_labels', 'color']:
                    variance = round(temp[v].var(), 2) if not math.isnan(float(temp[v].var())) else 0
                    clust = []
                    for (_, cluster, val, col) in temp[['cluster_labels', v, 'color']].itertuples():
                        if not val is None:
                            clust.append({'cluster': cluster, 'value': val, 'col': col})
                    variable_clust.append({'variable': v, 'var': variance, 'values': clust})
        # add count variables
        temp = self.profiling_df[['cluster_labels']].groupby('cluster_labels', as_index=True).count()
        temp['color'] = temp.index.map(mapcolor)
        temp = temp.where(pd.notnull(temp), None)
        variance = round(temp[v].var(), 2) if not math.isnan(temp[v].var()) else 0
        clust = [
            {'cluster': cluster, 'value': value, 'col': col}
            for (cluster, value, col) in temp.itertuples()
        ]
        variable_clust.append({'variable': 'cluster_size', 'var': variance, 'values': clust})
        self.ret['cluster_description'] = variable_clust

    def cluster_profiling(self,):
        cluster_profiling = []

        # aggs = [np.min, np.max, np.median, percentile(25), percentile(75)]
        def profile_numerical(vals, scale):
            vals = np.array(vals)
            vals_no_nan = vals[~np.isnan(vals)]
            nb_rows = vals_no_nan.shape[0]
            if nb_rows < 2:
                return {
                    "min": None,
                    "max": None,
                    "median": None,
                    "percentile25": None,
                    "percentile75": None,
                    "percentile9": None,
                    "percentile91": None,
                    "std": None,
                    "distribution": None,
                    "total_no_nan": nb_rows,
                    "max_ratio": 0.0,
                    "total": vals.shape[0]
                }
            else:
                percentile = make_percentile(vals_no_nan)
                distribution = np.histogram(vals_no_nan, scale)[0]
                max_ratio = distribution.max() / float(nb_rows)
                # TODO use the interpolation option in numpy 1.9
                return {
                    "min": np.min(vals_no_nan),
                    "max": np.max(vals_no_nan),
                    "median": float(percentile(50)),
                    "percentile25": float(percentile(25)),
                    "percentile75": float(percentile(75)),
                    "percentile9": float(percentile(9)),
                    "percentile91": float(percentile(91)),
                    "std": np.std(vals_no_nan),
                    "distribution": distribution,
                    "max_ratio": max_ratio,
                    "total_no_nan": nb_rows,
                    "total": vals.shape[0]
                }

        def profile_categorical(vals, categories):
            nb_rows = vals.shape[0]
            if nb_rows == 0:
                return {
                    "distribution": None,
                    "max_ratio": 0.0,
                    "total_no_nan": nb_rows,
                    "total": nb_rows
                }
            else:
                counts = value_counts(vals, n_most_common=30)
                distribution = [
                    {
                        "label": category,
                        "total_no_nan": counts.get(category, 0),
                        "ratio": counts.get(category, 0) / float(nb_rows)
                    }
                    for category in categories
                ]
                max_ratio = max(counts.values()) / float(nb_rows)
                return {
                    "distribution": distribution,
                    "max_ratio": max_ratio,
                    "total": nb_rows,
                    "total_no_nan": nb_rows
                }

        # add source variables
        if len(self.nfact) >= 2:  # cause 'cluster' in it anyway.
            profiling_df = self.profiling_df[self.nfact]
            cluster_labels = profiling_df["cluster_labels"]
            cluster_names = sorted(np.unique(cluster_labels))
            for col in profiling_df.columns:
                if col == "cluster_labels":
                    continue
                if col.startswith("factor_"):
                    continue
                col_profiling = {"variable": col}
                per_cluster = []
                col_profiling["per_cluster"] = per_cluster
                if float in profiling_df[col].dtype.type.mro():
                    col_profiling["type"] = "numerical"
                    cluster_profiling.append(col_profiling)
                    col_vals = profiling_df[col]
                    col_vals_no_na = no_nan(col_vals)
                    percentile = make_percentile(col_vals_no_na)
                    scale_start = percentile(5)
                    scale_stop = percentile(95)
                    max_ratio = 0.01
                    col_profiling["scale"] = {
                        "min": scale_start,
                        "max": scale_stop,
                    }
                    if scale_stop - scale_start == 0:
                        continue
                    scale = np.linspace(scale_start, scale_stop, num=61)
                    col_profiling["global"] = profile_numerical(col_vals, scale)
                    max_ratio = max(max_ratio, col_profiling["global"]["max_ratio"])
                    for cluster_label in cluster_names:
                        filtered_col_vals = np.array(col_vals[cluster_labels == cluster_label])
                        cluster_profile = profile_numerical(filtered_col_vals, scale)
                        max_ratio = max(max_ratio, cluster_profile["max_ratio"])
                        cluster_profile["cluster_name"] = cluster_label
                        per_cluster.append(cluster_profile)
                    col_profiling["scale"]["max_ratio"] = max_ratio
                else:
                    col_profiling["type"] = "categorical"
                    # categorical stuff.
                    col_vals = profiling_df[col]
                    global_counts = value_counts(col_vals, n_most_common=30)
                    # global_counts contains the counts for the category values we break down on
                    mask = col_vals.isin(global_counts.keys())
                    if None in global_counts:
                        mask |= col_vals.isnull()
                    col_vals = col_vals[mask]
                    cluster_profiling.append(col_profiling)
                    col_profiling["global"] = profile_categorical(col_vals, global_counts.keys())
                    max_ratio = 0.0
                    for cluster_label in cluster_names:
                        filtered_col_vals = col_vals[cluster_labels == cluster_label]
                        cluster_profile = profile_categorical(filtered_col_vals, global_counts.keys())
                        cluster_profile["cluster_name"] = cluster_label
                        max_ratio = max(max_ratio, cluster_profile["max_ratio"])
                        per_cluster.append(cluster_profile)
                    scale = {"max_ratio": max_ratio}
                    col_profiling["scale"] = scale
                    scale["categories"] = global_counts.keys()
        self.ret['cluster_profiling'] = cluster_profiling
        logging.info("DONE cluster description")

    def _generate_uniform_points(self):
        random_df = pd.DataFrame()
        for c in self.train.columns:
            v = np.random.uniform(self.train[c].min(), self.train[c].max(), self.train.shape[0])
            s = pd.DataFrame(pd.Series(v, name=c + '__rand'))
            random_df = pd.concat((random_df, s), axis=1)
        return random_df

    def _reference_dispersion(self, mod):
        fake_data = self._generate_uniform_points()
        dispersion = np.log(mod.fit(fake_data).inertia_)
        return dispersion

    def gap_statistic(self, model, nboot):
        disps = [self._reference_dispersion(deepcopy(model)) for k in range(nboot)]
        esp = np.mean(disps)
        var = np.std(disps) * math.sqrt(1 + 1. / nboot)
        real = np.log(model.inertia_)
        return (esp - real, var)
