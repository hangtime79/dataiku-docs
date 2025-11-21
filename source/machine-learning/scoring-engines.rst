Scoring engines
#################

DSS allows you to select various engines in order to perform scoring of your models. This allows for faster execution in some cases.

.. note::

  Scoring engines are only used to actually predict rows. While they are strongly related to :doc:`training engines <algorithms/index>`,
  some models trained with one engine can be scored with another.

.. contents::
	:local:

Engines for the scoring recipe
================================

The following scoring engines are available:

* Local (DSS server only) scoring. This engine has two variants:

  * the **Python** engine provides wider compatibility but lower performance. Allows to compute :doc:`supervised/explanations`.
  * the **Optimized** scorer provides better performance and is automatically used whenever possible.

* Spark: the scoring is performed in a distributed fashion on a Spark cluster
* SQL (Regular): the model is converted to a SQL query and executed within a SQL database.
* SQL (Snowflake with Java UDF): the model uses Snowflake extended push-down. This provides much faster execution within Snowflake, and extended compatibility. Please see :doc:`/connecting/sql/snowflake` for details

The selected engine can be adjusted in the scoring recipe editor. Only engines that are compatible with the selected model and input dataset will be available.

The default settings the following:

* If the model was trained with Spark MLLib, it will be scored with the Spark engine
* Else it will be scored with the Local engine. The optimized engine will be used if available.

If you do not wish to score your model with the "optimized" engine for some reason, you may select "Force original backend" in the scoring recipe editor to revert to the original backend.

Choosing SQL (regular) engine (if your scored dataset is stored in an SQL database and your model is compatible) will generate a request to score the dataset. Note that this may create very large requests for complex models.

Engines for the API node
=========================

To score rows using the API node, the "Local" engine is used. This engine has two variants:

* the **Python** engine provides wider compatibility but lower performance.
* the **Optimized** scorer provides better performance and is automatically used whenever possible.

The Optimized engine is enabled if you check the "Use Java" option in the endpoint settings.

In other words, only models for which one of "Local (Python)" or "Local (Optimized)" is available can be scored in the API node.

Compatibility matrix
=====================

The compatibility matrix for all DSS models is the following.

Local (Python) and Local (Optimized) engines are available both in scoring recipes and API node. Spark and SQL engines are only available for the scoring recipes.

.. note::

  * For models trained with Python, the Optimized Local and Spark engines are only available if preprocessing is also compatible.
  * The SQL engine is only available if preprocessing is also compatible.

Algorithms
-----------

.. warning::

  The MLLib support is deprecated and will soon be removed.

+------------------+--------------------------------------+-------------------+----------------+-------+-------------------------------+--------------------------------+
| Training engine  |              Algorithm               | Local (Optimized) | Local (Python) | Spark | SQL (Snowflake with Java UDF) |    SQL (Regular)               |
+==================+======================================+===================+================+=======+===============================+================================+
| Python in-memory | Random forest                        | Yes               | Yes            | Yes   | Yes                           | Yes (except for multiclass)    |
+------------------+--------------------------------------+-------------------+----------------+-------+-------------------------------+--------------------------------+
| MLLib            | Random forest                        | Yes               | No             | Yes   | Yes                           | Yes (except for multiclass)    |
+------------------+--------------------------------------+-------------------+----------------+-------+-------------------------------+--------------------------------+
| Python in-memory | Gradient Boosting                    | Yes               | Yes            | Yes   | Yes                           | Yes (except for multiclass)    |
+------------------+--------------------------------------+-------------------+----------------+-------+-------------------------------+--------------------------------+
| MLLib            | Gradient Boosting (no multiclass)    | Yes               | No             | Yes   | Yes                           | Yes (except for multiclass)    |
+------------------+--------------------------------------+-------------------+----------------+-------+-------------------------------+--------------------------------+
| Python in-memory | LightGBM                             | Yes               | Yes            | Yes   | Yes                           | Yes (except for multiclass)    |
+------------------+--------------------------------------+-------------------+----------------+-------+-------------------------------+--------------------------------+
| Python in-memory | XGBoost                              | Yes               | Yes            | Yes   | Yes                           | Yes (except for multiclass)    |
+------------------+--------------------------------------+-------------------+----------------+-------+-------------------------------+--------------------------------+
| Python in-memory | Extra Trees (Scikit)                 | Yes               | Yes            | Yes   | Yes                           | Yes (except for multiclass)    |
+------------------+--------------------------------------+-------------------+----------------+-------+-------------------------------+--------------------------------+
| Python in-memory | Decision Trees                       | Yes               | Yes            | Yes   | Yes                           | Yes (no probas for multiclass) |
+------------------+--------------------------------------+-------------------+----------------+-------+-------------------------------+--------------------------------+
| MLLib            | Decision Trees                       | Yes               | No             | Yes   | Yes                           | Yes (no probas for multiclass) |
+------------------+--------------------------------------+-------------------+----------------+-------+-------------------------------+--------------------------------+
| Python in-memory | OLS, Lasso (non LARS), Ridge         | Yes               | Yes            | Yes   | Yes                           | Yes                            |
+------------------+--------------------------------------+-------------------+----------------+-------+-------------------------------+--------------------------------+
| Python in-memory | SGD                                  | Yes               | Yes            | Yes   | Yes                           | Yes                            |
+------------------+--------------------------------------+-------------------+----------------+-------+-------------------------------+--------------------------------+
| MLLib            | Linear Regression                    | Yes               | No             | Yes   | Yes                           | Yes                            |
+------------------+--------------------------------------+-------------------+----------------+-------+-------------------------------+--------------------------------+
| Python in-memory | Logistic Regression                  | Yes               | Yes            | Yes   | Yes                           | Yes                            |
+------------------+--------------------------------------+-------------------+----------------+-------+-------------------------------+--------------------------------+
| MLLib            | Logistic Regression                  | Yes               | No             | Yes   | Yes                           | Yes                            |
+------------------+--------------------------------------+-------------------+----------------+-------+-------------------------------+--------------------------------+
| Python in-memory | Neural Networks                      | Yes               | Yes            | Yes   | Yes                           | Yes                            |
+------------------+--------------------------------------+-------------------+----------------+-------+-------------------------------+--------------------------------+
| Python in-memory | Deep Neural Network                  | No                | Yes            | No    | No                            | No                             |
+------------------+--------------------------------------+-------------------+----------------+-------+-------------------------------+--------------------------------+
| Python in-memory | Naive Bayes                          | No                | Yes            | No    | No                            | No                             |
+------------------+--------------------------------------+-------------------+----------------+-------+-------------------------------+--------------------------------+
| MLLib            | Naive Bayes                          | No                | No             | Yes   | No                            | No                             |
+------------------+--------------------------------------+-------------------+----------------+-------+-------------------------------+--------------------------------+
| Python in-memory | K-nearest-neighbors                  | No                | Yes            | No    | No                            | No                             |
+------------------+--------------------------------------+-------------------+----------------+-------+-------------------------------+--------------------------------+
| Python in-memory | SVM                                  | No                | Yes            | No    | No                            | No                             |
+------------------+--------------------------------------+-------------------+----------------+-------+-------------------------------+--------------------------------+
| Python in-memory | Custom models                        | No                | Yes            | No    | No                            | No                             |
+------------------+--------------------------------------+-------------------+----------------+-------+-------------------------------+--------------------------------+
| MLLib            | Custom models                        | No                | No             | Yes   | No                            | No                             |
+------------------+--------------------------------------+-------------------+----------------+-------+-------------------------------+--------------------------------+
|                  | Ensemble model                       | No                | Yes            | No    | No                            | No                             |
+------------------+--------------------------------------+-------------------+----------------+-------+-------------------------------+--------------------------------+

Preprocessing
--------------

Local (Optimized)
%%%%%%%%%%%%%%%%%

The following preprocessing options are available for Local(Optimized)

* Numerical

  * No rescaling
  * Rescaling
  * Binning
  * Derivative features
  * Flag presence
  * Imputation
  * Drop row
  * Datetime cyclical encoding

* Categorical

  * Dummification
  * Target encoding (impact and GLMM)
  * Ordinal
  * Frequency
  * Flag presence
  * Hashing (MLLib only)
  * Impute
  * Drop row

* Text

  * Count vectorization
  * TF/IDF vectorization
  * Hashing (MLLib)

SQL (Snowflake with Java UDF)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

The following preprocessing options are available for SQL (Snowflake with Java UDF) scoring :

* Numerical

  * No rescaling
  * Rescaling
  * Binning
  * Derivative features
  * Flag presence
  * Imputation
  * Drop row
  * Datetime cyclical encoding

* Categorical

  * Dummification
  * Target encoding (impact and GLMM)
  * Ordinal
  * Frequency
  * Flag presence
  * Hashing (MLLib only)
  * Impute
  * Drop row

* Text

  * Count vectorization
  * TF/IDF vectorization
  * Hashing (MLLib)


SQL (Regular)
%%%%%%%%%%%%%%%%%

The following preprocessing options are available for SQL (regular) scoring :

* Numerical

  * No rescaling
  * Rescaling
  * Binning
  * Flag presence
  * Imputation
  * Drop row

* Categorical

  * Dummification
  * Impact coding
  * Ordinal
  * Frequency
  * Flag presence
  * Impute
  * Drop row

Text is not supported

Limitations
============

SQL (regular) engine
----------------------

The following limitations exist with SQL (regular) scoring:

* Some algorithms may not generate probabilities with SQL scoring (see table above)
* Conditional output columns are not generated with SQL scoring
* Preparation scripts are not compatible with SQL scoring
* Multiclass logistic regression and neural networks require the SQL dialect to support the GREATEST function.
