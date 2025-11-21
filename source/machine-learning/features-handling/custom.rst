Custom Preprocessing
#####################

DSS allows to define custom python preprocessings, in order to plug user-generated code which will process a feature.

Implementing a custom processor
===============================

"Custom preprocessing" must be selected in the feature handling options.

The custom processor should be a class with at least two methods:

.. code-block:: py

    def fit(self, series):
    def transform(self, series):

Here, series is a pandas Series object representing the feature column. 
The fit method does not need to return anything, but must modify the object in-place if fitting is necessary. 
The transform method must return either a pandas DataFrame or a 2-D numpy array or scipy.sparse.csr_matrix containing the preprocessed result. Note that a single processor may output several numerical features, corresponding several columns of the output.

To use your processor in the visual ML UI, you must import it and instantiate it in the code editor, by assigning the processor to the ``processor`` variable.

.. warning::

    Classes cannot be declared directly in the Models > Design tab. They must be packaged in a :doc:`library </python/reusing-code>` and imported, as demonstrated in the examples below.

Example
-------

- On the Models > Design > Feature handling tab, in the "Custom preprocessing" code editor, you should create the ``processor`` variable.

    .. code-block:: python

        from my_custom_processor import MyProcessor

        processor = MyProcessor()

- Make sure that the option "Proc. wants matrix" is disabled. (When this option is enabled, custom processors receive a single-column ``DataFrame`` instead of a ``Series``).

- In ``my_custom_processor.py``:

    .. code-block:: python

        import pandas as pd

        class MyProcessor:
            """This processor adds a new `clipped_column` column which
            clips the `original_column` at its 10th highest value"""

            def __init__(self):
                self.max_value = None

            def fit(self, series):
                # compute the 10th highest value
                self.max_value = series.nlargest(10).iloc[-1]

            def transform(self, series):
                df = pd.DataFrame(series.values, columns=["original_column"])
                df["clipped_column"] = df["original_column"].clip(upper=self.max_value)
                return df


Naming output columns
=====================

When generating features, it is important to give them a meaningful name in order to interpret the resulting model. For instance, it is convenient when analyzing the variables importance or the regression coefficients for linear models.

If you return a ``pandas.DataFrame``, the name of the columns will be the name of the output features.

If you prefer to return a numpy array or a scipy.sparse.csr_matrix, then the processor should be also have a ``names`` attribute, containing the list of the output feature names. 

Example
-------

- On the Models > Design > Feature handling tab, in the "Custom preprocessing" code editor, you should create the ``processor`` variable.

    .. code-block:: python

        from my_custom_processor import MyProcessor

        processor = MyProcessor()

- Make sure that the option "Proc. wants matrix" is disabled. (When this option is enabled, custom processors receive a single-column ``DataFrame`` instead of a ``Series``).

- In ``my_custom_processor.py``:

    .. code-block:: python

        import numpy as np

        class MyProcessor:
            """This processor adds a new `clipped_column` column which
            clips the `original_column` at its 10th highest value"""

            def __init__(self):
                self.names = ["original_column", "clipped_column"]
                self.max_value = None

            def fit(self, series):
                # compute the 10th highest value
                self.max_value = series.nlargest(10).iloc[-1]

            def transform(self, series):
                # computed the clipped series
                clipped_series = series.clip(upper=self.max_value)
                # return a numpy array with both series
                return np.array([
                    series.values,
                    clipped_series.values
                ]).T
