Features roles and types
##########################

Roles
======

A feature's role determines how it's used during machine learning.

- **Reject** means that the feature is not used
- **Input** means that the feature is used to build a model, either as a potential :doc:`predictor for a target </machine-learning/supervised/index>` or for :doc:`clustering </machine-learning/unsupervised/index>`. For time-series forecasting, **Input** means that the feature is used as an :ref:`external variable <forecasting-external-features>` (handled by some time-series forecasting models). External variables can be either known-in-advance or past-only (the latter is supported by machine-learning-based forecasting).
- **Use for display only** means that the feature is not used to build a model, but is used to label model output.  This role is currently only used by cluster models.


Variable type
===========================

A feature's variable type determines the feature handling options during machine learning.

- **Categorical** variables take one of an enumerated list values.  The goal of categorical feature handling is to encode the values of a categorical variable so that they can be treated as numeric.
- **Numerical** variables take values that can be added, subtracted, multiplied, and so on.  There are times when it may be useful to treat a numerical variable with a limited number of values as categorical.
- **Text** variables are arbitrary blocks of text.  If a text variable takes a limited number of values, it may be useful to treat it as categorical.
- **Vector** variables are arrays of numerical values, of the same length.
- **Image** variables are available for Deep learning. See :doc:`../deep-learning/images` for more information.

.. note::
   For MLflow Models, string and boolean features will be considered **Categorical**.