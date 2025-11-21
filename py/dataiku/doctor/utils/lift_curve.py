#!/usr/bin/env python
# encoding: utf-8
"""
lift_curve.py
"""
import os
import pandas as pd
import numpy as np
import json


# TODO undferstand and test that
# definitely broken because of the __target__ label pasing

class LiftBuilder(object):
    
    def __init__(self, data, actual, predicted):
        self.data = data
        self.actual = actual
        self.predicted = predicted
        
    def _make_cuts(self):
        isCut = False
        while not isCut:
            for c in xrange(10, 1, -1):
                print "run", c
                try:
                    self.data['percentile_id'] = pd.qcut(self.data[self.predicted], c).labels
                    self.data['percentile_label'] = pd.qcut(self.data[self.predicted], c)
                    isCut = True
                    break
                except Exception, e:
                    if c == 2:
                        print str(e)
                        raise
                        break
                    pass
        
    def _get_labels(self):
       self.labels = self.data[['percentile_id', 'percentile_label']].drop_duplicates()
       self.labels = self.labels.set_index('percentile_id')
        
    def _get_stats(self):
        lift = self.data.groupby(['percentile_id', '__target__']).size().reset_index()
        lift.columns = ['percentile_id', '__target__', 'count']
        lift = lift.pivot_table(values="count", cols='__target__', rows="percentile_id", fill_value=0, aggfunc="sum").sort_index(ascending=False)
        lift['prop'] = lift[1].astype(np.float64) / (lift[0] + lift[1])
        real_prop = lift[1].astype(np.float64).sum() / (lift[0].sum() + lift[1].sum())
        lift['lift'] = lift['prop'] / real_prop
        lift['curve'] = lift[1].astype(np.float64).cumsum() / lift[1].sum()
        lift['bin_size'] = (lift[0] + lift[1]).astype(np.float64).cumsum() / (lift[0] + lift[1]).sum()
        lift = lift.join(self.labels)
        lift = lift.reset_index()
        lift['percentile_idx'] = lift.index
        f = lambda row: '%s %s' % (row['percentile_idx'], row['percentile_label'])
        lift['percentile'] = lift.apply(f, axis=1)
        return json.loads(lift.to_json(orient='records'))
        
    def _get_wizard(self):
        return {
            "positives": self.data['__target__'].sum(),
            "total": len(self.data)
        } 
        
    def build(self):
        wizard = self._get_wizard() 
        self._make_cuts()
        self._get_labels()
        return {
                "curve":self._get_stats(), 
                "wizard" : wizard
        }