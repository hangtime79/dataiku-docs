import time
import unicodedata
import numpy as np
from datetime import datetime


EPOCH = datetime(1900, 1, 1)


def datetime_to_epoch(series):
    return (series - EPOCH) / np.timedelta64(1, 's')


def unix_time_millis():
    return int(1000 * time.time())


def strip_accents(s):
    return ''.join(
        c
        for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
    )


def coerce_series(series, feature_type):
    if feature_type == 'NUMERIC':
        if series.dtype == np.dtype('<M8[ns]'):
            return datetime_to_epoch(series)
        else:
            try:
                return series.astype('double')
            except Exception:
                raise ValueError('Series contains non-numerical values')
    elif feature_type == 'CATEGORY' or feature_type == 'TEXT':
        return series.astype('unicode')
    else:
        raise ValueError("Feature type %s is unknown. Expected NUMERIC or CATEGORY.")


def coerce_dataframe(df, params):
    """ Coerce the columns of the coerce_dataframe with
    regard to the params object.
    """
    for fname, fparams in params.iteritems():
        role = fparams['role']
        if role == 'REJECT':
            continue
        if fname not in df.columns:
            if role != 'TARGET':
                raise ValueError('The feature %s doesn\'t exist in the dataset' % fname)
        else:
            feature_type = fparams['type']
            try:
                df[fname] = coerce_series(df[fname], feature_type)
            except ValueError, e:
                raise ValueError("Feature %s error: %s" % (fname, e.message))



from listener import ProgressListener
from subsampler import subsample
from magic_main import magic_main
