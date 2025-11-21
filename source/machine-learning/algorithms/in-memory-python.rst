In-memory Python
################

Most algorithms (except time series forecasting) are based on the `Scikit Learn <http://scikit-learn.org/>`_, the `LightGBM <https://github.com/microsoft/LightGBM>`_ or the `XGBoost <https://github.com/dmlc/xgboost>`_ machine learning libraries.

This engine provides in-memory processing.  The train and test sets must fit in memory. Use the sampling settings if needed.

.. contents:: :depth: 2
	:local:


Prediction algorithms
=======================

Prediction with this engine supports the following algorithms.


(Regression) Ordinary Least Squares
-------------------------------------

Ordinary Least Squares or Linear Least Squares is the simplest algorithm for linear regression.  The target variable is computed as the sum of weighted input variables. OLS finds the appropriate weights by minimizing the cost function (ie, how 'wrong' the algorithm is).

OLS is very simple and provides a very "explainable" model, but:

- it cannot automatically fit data for which the target variable is not the result of a linear combination of input features
- it is highly sensitive to errors in the input dataset and prone to overfitting

Parameters:

- **Parallelism:** Number of cores used for parallel training. Using more cores leads to faster training but at the expense of more memory consumption, especially for large training datasets. (-1 means 'all cores')

(Regression) Ridge Regression
-------------------------------

Ridge Regression addresses some problems of Ordinary Least Squares by imposing a penalty (or regularization term) to the weights. Ridge regression uses a L2 regularization. L2 regularization reduces the size of the coefficients in the model.

Parameters:

- **Regularization term (auto-optimized or specific values)**: Auto-optimization is generally faster than trying multiple values, but it does not support sparse features (like text hashing)
- **Alpha**: The regularization term. This parameter can be optimized.

(Regression) Lasso Regression
-------------------------------

Lasso Regression is another linear model, using a different regularization term (L1 regularization). L1 regularization reduces the number of features included in the final model.

Parameters:

- **Regularization term (auto-optimized or specific values)**: Auto-optimization is generally faster than trying multiple values, but it does not support sparse features (like text hashing)
- **Alpha**: The regularization term. This parameter can be optimized.


.. _classification-logistic-regression:

(Classification) Logistic regression
---------------------------------------------

Despite its name, Logistic Regression is a classification algorithm using a linear model (ie, it computes the target feature as a linear combination of input features). Logistic Regression minimizes a specific cost function (called logit or sigmoid function), which makes it appropriate for classification.  A simple Logistic regression algorithm is prone to overfitting and sensitive to errors in the input dataset. To address these issues, it is possible to use a penalty (or regularization term ) to the weights.

Logistic regression has two parameters:

- **Regularization (L1 or L2 regularization)**: L1 regularization reduces the number of features that are used in the model. L2 regularization reduces the size of the coefficient for each feature.
- **C**: Penalty parameter C of the error term. A low value of C will generate a smoother decision boundary (higher bias) while a high value aims at correctly classifying all training examples, at the risk of overfitting (high variance). (C corresponds to the inverse of a regularization parameter). You can try several values of C by using a comma-separated list.


.. _random forest:

(Regression & Classification) Random Forests
---------------------------------------------

*Decision tree classification* is a simple algorithm which builds a decision tree. Each node of the decision tree includes a condition on one of the input features.

A *Random Forest* regressor is made of many decision trees. When predicting a new record, it is predicted by each tree, and each tree "votes" for the final answer of the forest.
The forest then averages the individual trees answers. When "growing" (ie, training) the forest:

- for each tree, a random sample of the training set is used;
- for each decision point in the tree, a random subset of the input features is considered.

Random Forests generally provide good results, at the expense of "explainability" of the model.

Parameters:

- **Number of trees**: Number of trees in the forest.  Increasing the number of trees in a random forest does not result in overfitting. This parameter can be optimized.
- **Feature sampling strategy:** Adjusts the number of features to sample at each split.

  - Automatic will select 30% of the features.
  - Square root and Logarithm will select the square root or base 2 logarithm of the number of features respectively
  - Fixed number will select the given number of features
  - Fixed proportion will select the given proportion of features

- **Maximum depth of tree**: Maximum depth of each tree in the forest. Higher values generally increase the quality of the prediction, but can lead to overfitting. High values also increase the training and prediction time. Use 0 for unlimited depth (ie, keep splitting the tree until each node contains a single target value)
- **Minimum samples per leaf**: Minimum number of samples required in a single tree node to split this node. Lower values increase the quality of the prediction (by splitting the tree mode), but can lead to overfitting and increased training and prediction time.
- **Parallelism:** Number of cores used for parallel training. Using more cores leads to faster training but at the expense of more memory consumption, especially for large training datasets.
- **Allow sparse matrices:** Whether to allow DSS to use sparse matrices for training. Internally, DSS will use a heuristic on whether to train on sparse matrices, which may help reduce CPU and RAM usage. This can be particularly useful when using either Dummy Encoding categorical feature handling, or hashing-based text feature handling.


(Regression & Classification)  Gradient Boosted Trees
-----------------------------------------------------

Gradient boosted trees are another ensemble method based on decision trees. Trees are added to the model sequentially, and each tree attempts to improve the performance of the ensemble as a whole.  The advantages of GBRT are:

- Natural handling of data of mixed type (= heterogeneous features)
- Predictive power
- Robustness to outliers in output space (via robust loss functions)

Please note that you may face scalability issues, due to the sequential nature of boosting it can hardly be parallelized.

The gradient boosted tree algorithm has four parameters:

- **Number of boosting stages**: The number of boosting stages to perform. Gradient boosting is fairly robust to over-fitting so a large number usually results in better performance. This parameter can be optimized.
- **Learning rate**: Multiplier applied to all base learners. Lower values slow down convergence and can make the model more robust. Typical values: 0.01 - 0.3. This parameter can be optimized.
- **Loss:** The available loss functions depend upon whether this is a classification or regression problem.

    - **Classification:** Deviance refers to deviance (equivalent to logistic regression) for classification with probabilistic outputs. For exponential loss, gradient boosting recovers the AdaBoost algorithm.
    - **Regression:** Choose from least squares, least absolution deviation, or Huber.  Huber is a combination of Least Square and Least Absolute Deviation.

- **Maximum depth of tree:** Maximum depth of each tree. High values can increase the quality of the prediction, but can also lead to over-fitting. Typical values: 3 - 10. This parameter can be optimized.
- **Allow sparse matrices:** Whether to allow DSS to use sparse matrices for training. Internally, DSS will use a heuristic on whether to train on sparse matrices, which may help reduce CPU and RAM usage. This can be particularly useful when using either Dummy Encoding categorical feature handling, or hashing-based text feature handling.
- **Minimum samples per leaf**: Minimum number of samples required in a single tree node to split this node. Lower values increase the quality of the prediction (by splitting the tree mode), but can lead to overfitting and increased training and prediction time.

This algorithm also provides the ability to visualize partial dependency plots of your features.

(Regression & Classification) LightGBM
--------------------------------------

`LightGBM uses a specific library <https://lightgbm.readthedocs.io>`_ instead of scikit-learn.

LightGBM is a tree-based gradient boosting library designed to be distributed and efficient. It provides fast training speed, low memory usage, good accuracy and is capable of handling large scale data.

Parameters:

- **Maximum number of trees:** LightGBM has an early stopping mechanism so the exact number of trees will be optimized. High number of actual trees will increase the training and prediction time. Typical values: 50 - 200. This parameter can be optimized.
- **Maximum depth of tree:** Maximum depth of each tree. High values can increase the quality of the prediction, but can also lead to over-fitting. Typical values: 3 - 10.
- **Number of leaves:** Maximum tree leaves for base learners. Typical values range between 20 and 500. This parameter can be optimized.
- **Learning rate:** Multiplier applied to all base learners. Lower values slow down convergence and can make the model more robust. Typical values: 0.01 - 0.3. This parameter can be optimized.
- **Minimum split gain:** Minimum loss reduction required to make a further partition on a leaf node of the tree. This parameter can be optimized.
- **Minimum child weight:** Minimum sum of instance weight (hessian) needed in a child (leaf). High values can prevent over-fitting by learning highly specific cases. Smaller values allow leaf nodes to match a small set of rows, which can be relevant for highly imbalanced datasets. This parameter can be optimized.
- **Minimum leaf samples:** Minimum number of data samples needed in a leaf. This parameter can be optimized.
- **Colsample by tree:** Fraction of the features to be used in each tree. Typical values: 0.5 - 1. This parameter can be optimized.
- **L1 regularization:** L1 regularization coefficient applied to the weight of potential splits for their evaluation during tree-building. Aims at reducing over-fitting and the complexity of trees. This parameter can be optimized.
- **L2 regularization:** L2 regularization coefficient applied to the weight of potential splits for their evaluation during tree-building. Aims at reducing over-fitting and the complexity of trees. This parameter can be optimized.
- **Use Bagging:** Bagging can be used to speed up training and/or prevent over-fitting but can also make specific cases harder to learn. Enabling bagging allows to configure the "Subsample" parameters.
- **Subsample ratio:** Subsample ratio for the data to be used in each tree. Low values can prevent over-fitting but can make specific cases harder to learn. Typical values: 0.5 - 1. Note that 1. will de facto disable bagging.
- **Subsample frequency:** Frequency (in number of iterations) at which bagging must be performed. Setting a value of k means "perform bagging every k iterations". Note that 0 will de facto disable bagging.
- **Early stopping:** Use the LightGBM's built-in early stopping mechanism so the exact number of trees will be optimized (up to the specified maximum number of trees). The cross-validation scheme defined in the **Train & validation** tab will be used. This parameter will always be optimized during the hyperparameter search step. The model training fitting step won't re-optimize it.
- **Early stopping rounds:** The optimizer stops if the loss never decreases for this consecutive number of iterations. Typical values: 4 - 10.
- **Parallelism:** Number of cores used for parallel training (-1 means "all cores"). Using more cores leads to faster training but at the expense of more memory consumption, especially for large training datasets.
- **Allow sparse matrices:** Whether to allow DSS to use sparse matrices for training. Internally, DSS will use a heuristic on whether to train on sparse matrices, which may help reduce CPU and RAM usage. This can be particularly useful when using either Dummy Encoding categorical feature handling, or hashing-based text feature handling.

(Regression & Classification) XGBoost
-----------------------------------------------------

`XGBoost uses a specific library <https://xgboost.readthedocs.io>`_ instead of scikit-learn.

XGBoost is an advanced gradient boosted tree algorithm. It has support for parallel processing, regularization, early stopping which makes it a very fast, scalable and accurate algorithm.

Parameters:

- **Maximum number of trees:** XGBoost has an early stopping mechanism so the exact number of trees will be optimized. High number of actual trees will increase the training and prediction time. Typical values: 50 - 200. This parameter can be optimized.
- **Early stopping:** Use the XGBoost's built-in early stopping mechanism so the exact number of trees will be optimized (up to the specified maximum number of trees). The cross-validation scheme defined in the **Train & validation** tab will be used. This parameter will always be optimized during the hyperparameter search step. The model training fitting step won't re-optimize it.
- **Early stopping rounds:** The optimizer stops if the loss never decreases for this consecutive number of iterations. Typical values: 4 - 10.
- **Maximum depth of tree:** Maximum depth of each tree. High values can increase the quality of the prediction, but can also lead to over-fitting. Typical values: 3 - 10. This parameter can be optimized.
- **Learning rate:** Multiplier applied to all base learners. Lower values slow down convergence and can make the model more robust. Typical values: 0.01 - 0.3. This parameter can be optimized.
- **L2 regularization:** L2 regularization coefficient applied to the weight of potential splits for their evaluation during tree-building. Aims at reducing over-fitting and the complexity of trees. This parameter can be optimized.
- **L1 regularization:** L1 regularization coefficient applied to the weight of potential splits for their evaluation during tree-building. Aims at reducing over-fitting and the complexity of trees. This parameter can be optimized.
- **Gamma:** Minimum loss reduction required to make a further partition on a leaf node of the tree. This parameter can be optimized.
- **Minimum child weight:** Minimum sum of instance weight (hessian) needed in a child (leaf). High values can prevent over-fitting by learning highly specific cases. Smaller values allow leaf nodes to match a small set of rows, which can be relevant for highly imbalanced datasets. This parameter can be optimized.
- **Subsample:** Subsample ratio for the data to be used in each tree. Low values can prevent over-fitting but can make specific cases harder to learn. Typical values: 0.5 - 1. This parameter can be optimized.
- **Colsample by tree:** Fraction of the features to be used in each tree. Typical values: 0.5 - 1. This parameter can be optimized.
- **Parallelism:** Number of cores used for parallel training (-1 means "all cores"). Using more cores leads to faster training but at the expense of more memory consumption, especially for large training datasets.
- **Allow sparse matrices:** Whether to allow DSS to use sparse matrices for training. Internally, DSS will use a heuristic on whether to train on sparse matrices, which may help reduce CPU and RAM usage. This can be particularly useful when using either Dummy Encoding categorical feature handling, or hashing-based text feature handling. If enabled, the output model will not be exportable to SQL or PMML.
- **Custom missing value:** Allows choosing a specific value to treat as missing, instead of the default of np.nan. Beware that this value is compared after preprocessing, which can include averaging and value imputing. This setting has no effect with sparse matrices.


(Regression & Classification) Decision Tree
---------------------------------------------

Decision Trees (DTs) are a non-parametric supervised learning method used for classification and regression. The goal is to create a model that predicts the value of a target variable by learning simple decision rules inferred from the data features.

Parameters:

- **Maximum depth**: The maximum depth of the tree. This parameter can be optimized.
- **Criterion (Gini or Entropy)**: The function to measure the quality of a split. Supported criteria are “gini” for the Gini impurity and “entropy” for the information gain.  This applies only to classification problems.
- **Minimum samples per leaf**: Minimum number of samples required to be at a leaf node. This parameter can be optimized.
- **Split strategy (Best or random)**. The strategy used to choose the split at each node. Supported strategies are “best” to choose the best split and “random” to choose the best random split.


(Regression & Classification) Support Vector Machine
------------------------------------------------------

Support Vector Machine is a powerful 'black-box' algorithm for classification. Through the use of kernel functions, it can learn complex non-linear decision boundaries (ie, when it is not possible to compute the target as a linear combination of input features). SVM is effective with large number of features. However, this algorithm is generally slower than others.

Parameters:

- **Kernel (linear, RBF, polynomial, sigmoid)**: The kernel function used for computing the similarity of samples. Try several to see which works the best.
- **C**: Penalty parameter C of the error term.  A low value of C will generate a smoother decision boundary (higher bias) while a high value aims at correctly classifying all training examples, at the risk of overfitting (high variance). (C corresponds to the inverse of a regularization parameter). This parameter can be optimized.
- **Gamma**: Kernel coefficient for RBF, polynomial and sigmoid kernels. Gamma defines the 'influence' of each training example in the features space. A low value of gamma means that each example has 'far-reaching influence', while a high value means that each example only has close-range influence. If no value is specified (or 0.0), then 1/nb_features is used. This parameter can be optimized.
- **Tolerance**: Tolerance for stopping criterion.
- **Maximum number of iterations**: Number of iterations when fitting the model. -1 can be used to specific no limit.

(Regression & Classification) Stochastic Gradient Descent
----------------------------------------------------------

SGD is a family of algorithms that reuse concepts from Support Vector Machines and Logistic Regression. SGD uses an optimized method to minimize the cost (or loss ) function, making it particularly suitable for large datasets (or datasets with large number of features).

Parameters:

- **Loss function (logit or modified Huber)**: Selecting 'logit' loss will make the SGD behave like a Logistic Regression. Enabling 'modified huber' loss will make the SGD behave quite like a Support Vector Machine.
- **Iterations**: number of iterations on the data
- **Penalty (L1, L2 or elastic net)**: L1 and L2 regularization are similar to those for linear and logistic regression. Elastic net regularization is a combination of L1 and L2 regularization.
- **Alpha**: Regularization parameter. A high value of alpha (ie, more regularization) will generate a smoother decision boundary (higher bias) while a lower value (less regularization) aims at correctly classifying all training examples, at the risk of overfitting (high variance). This parameter can be optimized.
- **L1 ratio**: ElasticNet regularization mixes both L1 and L2 regularization. This ratio controls the proportion of L2 in the mix. (ie: 0 corresponds to L2-only, 1 corresponds to L1-only). Defaults to 0.15 (85% L2, 15% L1).
- **Parallelism**: Number of cores used for parallel training. Using more cores leads to faster training but at the expense of more memory consumption, especially for large training datasets.

(Regression & Classification) K Nearest Neighbors
--------------------------------------------------

K Nearest Neighbor classification makes predictions for a sample by finding the k nearest samples and assigning the most represented class among them.

*Warning:* this algorithm requires storing the entire training data into the model. This will lead to a very large model if the data is larger than a few hundred lines. Predictions may also be slow.

Parameters:

- **K:** The number of neighbors to examine for each sample. This parameter can be optimized.
- **Distance weighting:** If enabled, voting across neighbors will be weighed by the inverse distance from the sample to the neighbor.
- **Neighbor finding algorithm:**  The method used to find the nearest neighbors to each point. Has no impact on predictive performance, but will have a high impact on training and prediction speed.

  * Automatic: a method will be selected empirically depending on the data.
  * KD & Ball Tree : stores the data points into a partitioned data structure for efficient lookup.
  * Brute force: will examine every training sample for every prediction. Usually inefficient.

- **p:** The exponent of the Minkowski metric used to search neighbors. For p = 2, this gives Euclidean distance, for p = 1, Manhattan distance. Greater values lead to the Lp distances.


.. _regression-classification-extra-random-trees:


(Regression & Classification) Extra Random Trees
-------------------------------------------------

Extra trees, just like Random Forests, are an ensemble model. In addition to sampling features at each stage of splitting the tree, it also samples random threshold at which to make the splits. The additional randomness may improve generalization of the model.

Parameters:

- **Numbers of trees:** Number of trees in the forest. This parameter can be optimized.
- **Feature sampling strategy:** Adjusts the number of features to sample at each split.

  * Automatic will select 30% of the features.
  * Square root and Logarithm will select the square root or base 2 logarithm of the number of features respectively
  * Fixed number will select the given number of features
  * Fixed proportion will select the given proportion of features

- **Maximum depth of tree:** Maximum depth of each tree in the forest. Higher values generally increase the quality of the prediction, but can lead to overfitting. High values also increase the training and prediction time. Use 0 for unlimited depth (ie, keep splitting the tree until each node contains a single target value). This parameter can be optimized.
- **Minimum samples per leaf:** Minimum number of samples required in a single tree node to split this node. Lower values increase the quality of the prediction (by splitting the tree mode), but can lead to overfitting and increased training and prediction time. This parameter can be optimized.
- **Parallelism:** Number of cores used for parallel training. Using more cores leads to faster training but at the expense of more memory consumption, especially for large training datasets.

(Regression & Classification) Artificial Neural Network
-------------------------------------------------------

Neural Networks are a class of parametric models which are inspired by the functioning of neurons. They consist of several "hidden" layers of neurons, which receive inputs and transmit them to the next layer, mixing the inputs and applying non-linearities, allowing for a complex decision function.

Parameters:

- **Hidden layer sizes:** Number of neurons on each hidden layer. Separate by commas to add additional layers.
- **Activation:** The activation function for the neurons in the network.
- **Alpha:** L2 regularization parameter. Higher values lead to smaller neuron weights and a more generalizable, although less sharp model.
- **Max iterations:** Maximum iterations for learning. Higher values lead to better convergence, but take more time.
- **Convergence tolerance:** If the loss does not improve by this ratio over two iterations, training stops.
- **Early stopping:** Whether the model should use validation and stop early.
- **Solver:** The solver to use for optimization. LBFGS is a batch algorithm and is not suited for larger datasets.
- **Shuffle data:** Whether the data should be shuffled between epochs (recommended, unless the data is already in random order).
- **Initial Learning Rate:** The initial learning rate for gradient descent.
- **Automatic batching:** Whether batches should be created automatically (will use 200, or the whole dataset if there are less samples). Uncheck to select batch size.
- **beta_1:** beta_1 parameter for ADAM solver.
- **beta_2:** beta_2 parameter for ADAM solver.
- **epsilon:** epsilon parameter for ADAM solver.


(Regression & Classification) Lasso Path
------------------------------------------

The Lasso Path is a method which computes the LASSO path (ie. for all values of the regularization parameter). This is performed using LARS regression. It requires a number of passes on the data equal to the number of features. If this number is large, computation may be slow. This computation allows to select a given number of non-zero coefficients, ie. to select a given number of features. After training, you will be able to visualize the LASSO path and select a new number of features.

Parameters:

- **Maximum features:** The number of kept features. Input 0 to have all features enabled (no regularization). Has no impact on training time.


(Regression & Classification) Deep Neural Network
----------------------------------------------------

Deep Neural Networks are a class of fully-connected feedforward artificial neural networks, composed of one or several "hidden" layers of nodes, or computational units, called neurons.
Each neuron from a hidden layer gets information from all nodes of the previous layer and feeds its output to all nodes of the subsequent layer.
Given a set of features and a target, Deep Neural Networks can learn and approximate complex nonlinear functions for both regression and classification, in a supervised fashion using the backpropagation technique.

.. note::

  - The number of parameters of Deep Neural Networks make them prone to overfitting when trained on small amounts of data. Using the Early stopping parameter can help generalise better.
  - The reproducibility of results across multiple trainings is not guaranteed.

Parameters:

- **Hidden layers**: Number of hidden layers in the network.
- **Units per layer**: Number of neurons in each hidden layer. All layers will have the same number of units.
- **Learning Rate**: Learning rate for gradient descent.
- **Early stopping**: Use built-in early stopping mechanism to optimize the number of epochs The cross-validation scheme defined in the "Hyperparameters" tab will be used.
- **Early stopping patience**: Number of epochs to wait for improvement of the monitor value until the training process is stopped.
- **Early stopping threshold**: Ignore score improvements smaller than threshold.
- **Batch size**: Number of training samples processed before the internal model parameters are updated.
- **Dropout**: Regularization that randomly zeroes elements of the hidden layers input. The dropout value is the probability of an element to be zeroed.
- **L2 regularization**: L2 regularization adds penalty to high-valued weights and biases in the network by forcing them to be small.
- **L1 regularization**: L1 regularization adds penalty to weights in the network by shrinking them towards 0. It can lead to ignoring some neurons.

(Regression) Generalized Linear Models
----------------------------------------


Generalized Linear Models (GLMs) are a generalization of the Ordinary Linear Regression where:

* The distribution of the response variable can be chosen from any exponential distribution (not only a gaussian distribution).
* The relationship between the linear model and the response variable can be chosen from any link function (not only the identity function).

These models allow flexibility on the dependency between the regressors and the response and are widely used in the Insurance industry to answer specific modelization needs. The GLM implementation comes from glum package. Regression Splines rely on patsy.

For GLM, DSS also supports custom views and recipes.

This capability is provided by the "GLM" plugin, which you need to install. Please see :doc:`/plugins/installing`. This plugin is :doc:`Not supported </troubleshooting/support-tiers>`.

Please see our `GLM plugin page <https://www.dataiku.com/product/plugins/glm/>`_ for detailed documentation.


.. _custom.models.regression:

(Regression & Classification) Custom Models
-------------------------------------------

You can make custom models using Python. Your custom models should be scikit-learn compatible:

- They must implement the methods ``fit`` and ``predict``.
- They must subclass ``sklearn.base.BaseEstimator``.
- They must receive the parameters of the ``__init__`` function as explicit keyword arguments

.. warning::

    Classes cannot be declared directly in the Models > Design tab. They must be packaged in a :doc:`library </python/reusing-code>` and imported, as demonstrated in the examples below.

For more details and advanced examples, please refer to :ref:`Advanced Custom Models <custom.models>`.

Regression
^^^^^^^^^^

Example
"""""""

- On the Models > Design > Algorithms tab, in the "Custom python model" code editor, you should create the ``clf`` variable.

    .. code-block:: python

        from custom_python_model import MyRandomRegressor

        clf = MyRandomRegressor()

- In ``custom_python_model.py``:

    .. code-block:: python

        from sklearn.base import BaseEstimator
        import numpy as np
        import pandas as pd

        class MyRandomRegressor(BaseEstimator):
            """This model predicts random values between the mininimum and the maximum of y"""

            def fit(self, X, y):
                self.y_range = [np.min(y), np.max(y)]

            def predict(self, X):
                return np.random.uniform(self.y_range[0], self.y_range[1], size=X.shape[0])

.. _custom.models.classification:

Classification
^^^^^^^^^^^^^^

In addition to ``fit`` and ``predict``, a classifier must also have a ``classes_`` attribute, and it can implement a ``predict_proba`` method.

Example
"""""""

- On the Models > Design > Algorithms tab, in the "Custom python model" code editor, you should create the ``clf`` variable.

    .. code-block:: python

        from custom_python_model import MyRandomClassifier

        clf = MyRandomClassifier()

- In ``custom_python_model.py``:

    .. code-block:: python

        from sklearn.base import BaseEstimator
        import numpy as np
        import pandas as pd

        class MyRandomClassifier(BaseEstimator):
            """This model predicts classes randomly"""

            def fit(self, X, y):
                self.classes_ = list(set(y))

            def predict(self, X):
                return np.random.choice(self.classes_, size=X.shape[0])

            def predict_proba(self,X):
                return np.random.rand(X.shape[0], len(self.classes_))


.. note::

    For linear binary classification models, it is possible to display the fitted regression coefficients in the "Regression coefficients" tab of the model report. To do so, you need to specify them using the scikit-learn approach, i.e. the custom classifier must satisfy the following conditions:

    - The classifier has attributes ``coef_`` and ``intercept_``.
    - These attributes are either of type ``numpy.ndarray`` or ``list``.
    - These attributes only have one row (i.e. ``coef_.shape[0] == 1``, or ``len(coef_) == 1`` if of type ``list``, and same thing for ``intercept_``).
    - ``len(clf.coef_[0])`` is equal to the number of preprocessed features (i.e. the number of columns in the train dataframe).

(Regression & Classification) Plugin Models
-----------------------------------------------

You can also build and use plugin models using Python. 

See :doc:`/plugins/reference/prediction-algorithms` for more details.


.. _timeseries-forecasting-algorithms:

Time series forecasting algorithms
==================================

Time series forecasting algorithms rely on the `GluonTS <https://ts.gluon.ai/>`_, `pmdarima <https://alkaline-ml.com/pmdarima/>`_, `statsmodels <https://www.statsmodels.org>`_ and `prophet <https://facebook.github.io/prophet/>`_ libraries.

Trivial identity
----------------

Trivial identity uses the last values in the forecasting horizon to predict the future.

Seasonal naive
--------------

Seasonal naive uses the values from previous season to predict the future.

Parameters:

- **Season length:**  Number of time steps in each season. Higher values increase training time.

AutoARIMA
---------

AutoARIMA automatically finds the optimal ARIMA (AutoRegressive Integrated Moving Average) model according to an information criterion.
It performs a search over the model orders within given constraints, and select the set of parameters that optimizes the provided information criterion.
Note that AutoARIMA may be slow for multiple time series, because it trains as many models as there are time series.

Parameters:

- **Stationary time series:** If checked, specifies that the time series is known to be stationary; otherwise not known *a priori*, so the model should auto-detect stationarity.
- **p:** p is the order (number of time lags) of the auto-regressive (AR) model.
- **First-differencing order (d):** Degree of differencing. ARIMA models that include differencing (i.e. when d is positive) assume that the data becomes stationary after differencing. If no value is provided, the value will automatically be selected based on the results of the unit root test; the runtime might be significantly longer.

    - **Maximum value of d**
- **Unit root test:** Type of test to use to detect stationarity. (Kwiatkowski–Phillips–Schmidt–Shin, Augmented Dickey Fuller, Phillips-Perron)
- **q:** q is the order (number of time lags) of the moving-average (MA) model.
- **Season length (m):** Number of time steps in each season. Season length can greatly impact the outcome. For higher values training time is increased; the model might not even converge.
- **P:** P is the order of the auto-regressive (AR) part of the seasonal model.
- **Seasonal differencing term (D):** If no value is provided, the value will automatically be selected based on the results of the seasonal unit root test.

    - **Maximum value of D**
- **Seasonal unit root test:** Type of test to use to detect seasonality. (Osborn-Chui-Smith-Birchenhall, Canova-Hansen)
- **Q:** Q is the order of the moving-average (MA) part of the seasonal model.
- **Upper bound for orders:** Allows to limit the search space: ARIMA models where p + q + P + Q is greater than the given value will not be fitted. Must be strictly greater than the sum of the starting values of each order.
- **Maximum iterations:** Maximum number of function evaluations during the search of the best ARIMA model orders.
- **Information criterion:** Information criterion minimized to find the best ARIMA model. (Akaike, Corrected Akaike, Bayes, Hannan-Quinn, "Out-of-bag" score)
- **Solver method:** Determines which solver from scipy.optimize is used: Newton-Raphson, Nelder-Mead, Broyden-Fletcher-Goldfarb-Shanno, Limited-memory BFGS, Powell, Conjugate gradient, Newton conjugate gradient, or Global basin-hopping.


ARIMA
---------

ARIMA (AutoRegressive Integrated Moving Average) is a statistical model used for time series forecasting. It combines autoregression (AR), differencing to achieve stationarity (I), and a moving average component (MA) to capture dependencies in data over time. Additionally, it supports seasonal components (S) to model seasonal patterns and exogenous variables (X) to incorporate external factors that influence the forecast.

Parameters:

- **p:** p is the order (number of time lags) of the auto-regressive (AR) model.
- **d:** Degree of differencing. ARIMA models that include differencing (i.e. when d is positive) assume that the data becomes stationary after differencing.
- **q:** q is the order (number of time lags) of the moving-average (MA) model.
- **P:** P is the order of the auto-regressive (AR) part of the seasonal model.
- **D:** Degree of seasonal differencing. Seasonal ARIMA models that include differencing (i.e. when D is positive) assume that the data becomes stationary after differencing.
- **Q:** Q is the order of the moving-average (MA) part of the seasonal model.
- **s:** s is the season length of the model.
- **Trend:** Deterministic trend of the model.
- **Enforce stationarity:** Require the autoregressive parameters to match a stationary process.
- **Enforce invertibility:** Require the moving average parameters to match an invertible process.
- **Concentrate scale:** Whether or not to concentrate the variance of the error term out of the likelihood.

Seasonal trend
--------------

Seasonal trend first subtracts the data seasonality estimated with STL (Seasonal and Trend decomposition using Loess). It then forecasts the deseasonalized data using an Exponential Smoothing model adjusted for trends.

Parameters:

- **Season length:** Number of time steps in each season, must be strictly greater than 1. Season length can greatly impact the outcome. Higher values increase training time.
- **Seasonal smoother length:** Must be an odd integer. Recommended value should be greater or equal to 7.
- **Trend smoother length:** Must be an odd integer, strictly greater than the season length.

    - **Use default trend smoother length:** If enabled, use the smallest odd integer greater than (1.5 * season length) / (1 - 1.5 / seasonal smoother length).
- **Low pass filter length:** Must be an odd integer.

    - **Use default low pass filter length:** If enabled, use the smallest odd integer strictly greater than the season length.
- **Degree of seasonal LOESS:** Degree of the LOESS smoothing polynomial for the seasonal component: constant or linear (i.e. constant and trend).
- **Degree of trend LOESS:** Degree of the LOESS smoothing polynomial for the trend component: constant or linear (i.e. constant and trend).
- **Degree of low pass LOESS:** Degree of the LOESS smoothing polynomial for the low pass component: constant or linear (i.e. constant and trend).
- **Seasonal jump:** Seasonal linear interpolation step. LOESS smoothing is used every *seasonal_jump* steps and values between two steps are linearly interpolated. Higher values reduce estimation time.
- **Trend jump:** Trend linear interpolation step. LOESS smoothing is used every *trend_jump* steps and values between two steps are linearly interpolated. Higher values reduce estimation time.
- **Low pass filter jump:** Low pass filter linear interpolation step. LOESS smoothing is used every *low_pass_jump* steps and values between two steps are linearly interpolated. Higher values reduce estimation time.


ETS
---------

ETS (Error, Trend, Seasonality) is a forecasting model that decomposes a time series into error, trend, and seasonal components.

Parameters:

- **Error:** Options are Multiplicative (M) and Additive (A).
- **Trend:** Options are  Multiplicative (M), Additive (A) and None (N).
- **Damped trend:** Whether to try regular trend, or damped trend (d).
- **Seasonality:** Options are Multiplicative (M), Additive (A) and None (N).
- **Season length:** Number of time steps in a season.
- **Random state:** Using a fixed random seed allows for reproducible result.
- **Unstable models:** Several parameter combinations are known to be unstable (AMN, AMA, AMdN, AMdA, AMM, AMdM, MMA, MMdA, ANM, AAM, AAdM) and are excluded by default from the hyperparameter search. This allows them to be included.


Prophet
-------

Prophet is a procedure for forecasting time series data based on an additive model where non-linear trends are fit with yearly, weekly, and daily seasonality. It works best with time series that have strong seasonal effects and several seasons of historical data.

Parameters:

- **Changepoint prior scale:** Parameter modulating the flexibility of the automatic changepoint selection. Large values will allow many changepoints, small values will allow few changepoints.
- **Growth:** Specify a linear, logistic or flat trend.
- **Seasonality prior scale:** Parameter modulating the strength of the seasonality model. Larger values allow the model to fit larger seasonal fluctuations, smaller values dampen the seasonality.
- **Seasonality mode:** *Additive* or *Multiplicative*.
- **Yearly seasonality:** *Auto*, *Always* or *Never*. Use a Fourier decomposition to fit the yearly seasonality (*Auto* means only when input data is longer than 2 years).
- **Weekly seasonality:** *Auto*, *Always* or *Never*. Use a Fourier decomposition to fit the weekly seasonality (*Auto* means only when input data is longer than 2 weeks).
- **Daily seasonality:** *Auto*, *Always* or *Never*. Use a Fourier decomposition to fit the daily seasonality (*Auto* means only when input data is longer than 2 days).
- **External features prior scale:** Parameter modulating the strength of the external features components model (only used when external features are selected).
- **Changepoint range:** Proportion of history in which trend changepoints will be estimated.
- **Number of changepoints:** Potential changepoints are selected uniformly from the first *Changepoint range* proportion of the history.
- **Random state:** Using a fixed random seed allows for reproducible result.

.. note::

    Prophet is only available for python 3.7+ code environments.


Non-Parametric Time Series
--------------------------

Non-Parametric Time Series predictor predicts future values by sampling from past observations. The sampling weights can follow either a uniform or exponentially decreasing distribution, and optionally take into account the seasonality of the time series.

For a **non-seasonal** NPTS model, past observations can be sampled using a uniform distribution, or an exponential distribution whose probability decreases with the time distance to the observation (recent observations thus have a higher probability to be sampled than distant past ones).

For a **seasonal** NPTS model, time features based on the frequency of the time series are computed. Past observations can either be sampled using a uniform distribution amongst observations with the same values for the computed time features, or using an exponential distribution whose probability decreases with both the time distance to the past observation and the distance w.r.t computed time features. External features can also be used along with, or instead of, the computed time features.

Parameters:

- **Context length:** Number of considered time steps before making predictions.

    - **Use default context length:** If enabled, use the model's default context length (1100).
- **Kernel type:** Exponential or Uniform.
- **Exponential kernel weight:** Single weight for the features to use in the exponential kernel.
- **Use a seasonal model:** If enabled, time features determined based on the frequency of the time series are added to the default feature map.

    - **Use default time features:** Provide extra time features computed based on the frequency of the time series (minute of hour for minutely, hour of day for hourly...). For a seasonal model, the default time features are always used when no external features have been provided.
    - **Feature scale:** Multiplicative scale to apply on time features (custom and/or default). This allows to sample past seasons with higher probability.

Simple Feed Forward
-------------------

Simple Feed Forward is a simple neural network that forecasts probability distributions for the next forecasting horizon values, given the preceding context length values.

Training parameters:

- **Learning rate:** Initial learning rate (decays during training).
- **Batch size:** The size of the batches to be used for training and prediction.
- **Epochs:** Number of epochs to be trained.
- **Number of batches per epoch**

    - **Use default nb. of batches per epoch:** If enabled, use the number for which each time step appears in one sample per epoch on average.

Model parameters:

- **Context length:** Number of considered time steps before making predictions.

    - **Use default context length:** If enabled, use the model's default value (equal to the forecasting horizon).
- **Output distribution:** Distribution to fit. (Student't distribution, Gaussian distribution, Negative binomial distribution)
- **Batch normalisation:** Normalize the layers' inputs by re-centering and re-scaling. This can make deep neural networks faster and more stable.
- **Mean scaling:** Scale the network input by the data mean and the network output by its inverse.
- **Hidden layer sizes:** Number of nodes in each hidden layer. Specify one value per layer.
- **Number of parallel samples:** Number of evaluation samples per time series to increase parallelism during inference.

DeepAR
------

DeepAR is an autoregressive recurrent neural network that forecasts probability distributions for the next forecasting *horizon values* given the preceding *context length* values. It also uses lagged values and time features, automatically computed based on the selected time frequency.

Training parameters:

- **Learning rate:** Initial learning rate (decays during training).
- **Batch size**, for training and prediction.
- **Epochs:** Number of epochs to be trained.
- **Number of batches per epoch**

    - **Use default nb. of batches per epoch:** If enabled, use the number for which each time step appears in one sample per epoch on average.

Model parameters:

- **Context length:** Number of considered time steps before making predictions.

    - **Use default context length:** If enabled, use the model's default value (equal to the forecasting horizon).
- **Output distribution:** Distribution to fit. (Student's t, Gaussian, Negative binomial)
- **Encode identifiers:** Encode time series identifiers and use them as external features (*feat_static_cat* in GluonTS).
- **Number of RNN layers**
- **Number of cells per layer**
- **Cell type:** Long short-term memory (LSTM) or Gated recurrent unit (GRU).
- **Dropout cell type:** ZoneoutCell, RNNZoneoutCell, VariationalDropoutCell, or VariationalZoneoutCell.
- **Dropout regularization parameter**
- **Alpha:** Scaling coef. of activation regularization.
- **Beta:** Scaling coef. of temporal activation regularization.
- **Scale target values:** For each time series, rescale the target by its average absolute value.
- **Minimum scale:**  Default scale (used if the time series has only zeroes).
- **Number of parallel samples:** Number of evaluation samples per time series, to increase parallelism during inference.

Transformer
-----------

Transformer estimator is a transformer neural network that forecasts probability distributions for the next *forecasting horizon* values, given the preceding *context length* values. It also uses lagged values and time features, automatically computed based on the selected time frequency.

Training parameters:

- **Learning rate:** Initial learning rate (decays during training).
- **Batch size**, for training and prediction.
- **Epochs:** Number of epochs to be trained.
- **Number of batches per epoch**

    - **Use default nb. of batches per epoch:** If enabled, use the number for which each time step appears in one sample per epoch on average.

Model parameters:

- **Context length:** Number of considered time steps before making predictions.

    - **Use default context length:** if enabled, use the model's default value (equal to the forecasting horizon).
- **Output distribution:** Distribution to fit. (Student's t, Gaussian, Negative binomial)
- **Encode identifiers:** Encode time series identifiers and use them as external features (*feat_static_cat* in GluonTS).
- **Transformer network dimension:** Embedding dimension of the input.
- **Dimension scale of hidden layer:**  Dimension scale of the inner hidden layer of the transformer’s feedforward network.
- **Number of heads in the multi-head attention**
- **Dropout regularization parameter**
- **Number of parallel samples:** Number of evaluation samples per time series, to increase parallelism during inference.

Multi-horizon Quantile - Convolutional Neural Network (MQ-CNN)
--------------------------------------------------------------

MQ-CNN (Multi-horizon Quantile - Convolutional Neural Network) is a convolutional neural network that uses a quantile decoder to make predictions for the next *forecasting horizon* values given the preceding *context length* values. It also uses time features, automatically computed based on the selected time frequency. The model forecasts the same quantiles as the ones selected for the evaluation metrics.

Training parameters:

- **Learning rate:** Initial learning rate (decays during training).
- **Batch size**, for training and prediction.
- **Epochs:** Number of epochs to be trained.
- **Number of batches per epoch**

    - **Use default nb. of batches per epoch:** If enabled, use the number for which each time step appears in one sample per epoch on average.

Model parameters:

- **Context length:** Number of considered time steps before making predictions.

    - **Use default context length:** If enabled, use the model's default value (equal to the forecasting horizon).
- **Encode identifiers:** Encode time series identifiers and use them as external features (*feat_static_cat* in GluonTS).
- **MLP layer sizes:** Dimensions of the Multi Layer Perceptron layers of the decoder. Use one value per layer.
- **Number of channels:** Number of channels for each layer of the encoder (which is a stack of dilated convolutions). Specify one value per layer. More channels usually means better performance and larger network size.
- **Convolution dilations:** Dilation of the convolutions in each layer of the encoder. Specify one value per layer. Should be of same length as the number of channels. Greater numbers correspond to a greater receptive field of the network, which is usually better with longer context lengths.
- **Kernel sizes:** Kernel sizes (i.e. window sizes) of the convolutions in each layer of the encoder. Specify one value per layer. Should be of same length as the number of channels.
- **Scale target values:** For each time series, rescale the target by its average absolute value.


Clustering algorithms
=======================

K-means
-----------------------------------------------

The k-means algorithm clusters data by trying to separate samples in *n* groups, minimizing a criterion known as the ‘inertia’ of the groups.

Parameters:

- **Number of clusters:** This parameter can be optimized.
- **Seed:** Used to generate reproducible results. 0 or no value means that no known seed is used (results will not be fully reproducible)
- **Parallelism:** Number of cores used for parallel training. Using more cores leads to faster training but at the expense of more memory consumption. If -1 all CPUs are used. For values below -1, (n_cpus + 1 + value) are used: ie for -2, all CPUs but one are used.

Gaussian Mixture
-----------------------------------------------

The Gaussian Mixture Model models the distribution of the data as a "mixture" of several
populations, each of which can be described by a single multivariate normal distribution.

An example of such a distribution is that of sizes among adults, which is described by the mixture of two distributions:
the sizes of men, and those of women, each of which is approximately described by a normal distribution.

Parameters:

- **Number of mixture components:** Number of populations. This parameter can be optimized.
- **Max Iterations:** The maximum number of iterations to learn the model. The Gaussian Mixture model uses the Expectation-Maximization algorithm, which is iterative, each iteration running on all of the data. A higher value of this parameter will lead to a longer running time, but a more precise clustering. A value between 10 and 100 is recommended.
- **Seed:** Used to generate reproducible results. 0 or no value means that no known seed is used (results will not be fully reproducible)

Mini-batch K-means
-----------------------------------------------

The Mini-Batch k-means is a variant of the k-means algorithm which uses mini-batches to reduce the computation time, while still attempting to optimise the same objective function.

Parameters:

- **Numbers of clusters:** This parameter can be optimized.
- **Seed:** Used to generate reproducible results. 0 or no value means that no known seed is used (results will not be fully reproducible)

Agglomerative Clustering
-----------------------------------------------

Hierarchical clustering is a general family of clustering algorithms that build nested clusters by merging them successively. This hierarchy of clusters represented as a tree (or `dendrogram <http://en.wikipedia.org/wiki/Dendrogram>`_). The root of the tree is the unique cluster that gathers all the samples, the leaves being the clusters with only one sample.

Parameters:

- **Numbers of clusters:** This parameter can be optimized.

Spectral Clustering
-----------------------------------------------

Spectral clustering algorithm uses the graph distance in the nearest neighbor graph. It does a low-dimension embedding of the affinity matrix between samples, followed by a k-means in the low dimensional space.

Parameters:

- **Numbers of clusters:** This parameter can be optimized.
- **Affinity measure:** The method to computing the distance between samples. Possible options are nearest neighbors, RBF kernel and polynomial kernel.
- **Gamma:** Kernel coefficient for RBF and polynomial kernels.
  Gamma defines the 'influence' of each training example in the features space.
  A low value of gamma means that each example has 'far-reaching influence', while a high value means that each example only has close-range influence.
  If no value is specified (or 0.0), then 1/nb_features is used.
- **Coef0:** Independent term for 'polynomial' or 'sigmoid' kernel function.
- **Seed:** Used to generate reproducible results. 0 or no value means that no known seed is used (results will not be fully reproducible)

DBSCAN
-----------------------------------------------

The DBSCAN algorithm views clusters as areas of high density separated by areas of low density. Due to this rather generic view, clusters found by DBSCAN can be any shape, as opposed to k-means which assumes that clusters are convex shaped. Numerical features should use standard rescaling.

There are two parameters that you can modify in DBSCAN:

- **Epsilon:** Maximum distance to consider two samples in the same neighborhood. You can try several values by using a comma-separated list
- **Min. Sample ratio:** Minimum ratio of records in its neighborhood for a point to be considered as a core point. This includes the point itself. If set to a higher value, DBSCAN will find denser clusters, whereas if it is set to a lower value, the found clusters will be more sparse.

HDBSCAN
-----------------------------------------------

HDBSCAN is an algorithm built on top of DBSCAN, by exploring values of its main hyperparameter (max distance for points to be considered neighbors). Hence, HDBSCAN builds clusters as areas of high density separated by areas of low density. Due to this rather generic view, clusters found by HDBSCAN can be any shape, as opposed to k-means which assumes that clusters are convex shaped.
Numerical features should use standard rescaling.

There is one parameter that you can modify in HDBSCAN:

- **Min. cluster ratio:** Minimum ratio of records to form a cluster. Groupings smaller than this size will be left as noise. You can try several values

Interactive Clustering (Two-step clustering)
---------------------------------------------

Interactive clustering is based on a two-step clustering algorithm. This two-staged algorithm first agglomerates data points into small clusters using K-Means clustering. Then, it applies agglomerative hierarchical clustering in order to further cluster the data, while also building a hierarchy between the smaller clusters, which can then be interpreted. It therefore allows to extract hierarchical information from datasets larger than a few hundred lines, which cannot be achieved through standard methods.
The clustering can then be manually adjusted in DSS's interface.

Parameters:

- **Number of Pre-clusters:** The number of clusters for KMeans preclustering. It is recommended that this number be lower than a couple hundred for readability.
- **Number of clusters:** The number of clusters in the hierarchy. The full hierarchy will be built and displayed, but these clusters will be used for scoring.
- **Max Iterations:** The maximum number of iterations for preclustering. KMeans is an iterative algorithm. A higher value of this parameter will lead to a longer running time, but a more precise pre-clustering. A value between 10 and 100 is recommended.
- **Seed:** Used to generate reproducible results. 0 or no value means that no known seed is used (results will not be fully reproducible)

Isolation Forest (Anomaly Detection)
------------------------------------

Isolation forest is an anomaly detection algorithm. It isolates observations by creating a Random Forest of trees, each splitting samples in different partitions. Anomalies tend to have much shorter paths from the root of the tree. Thus, the mean distance from the root provides a good measure of non-normality.

Parameters:

- **Number of trees:** Number of trees in the forest.
- **Contamination:** Expected proportion of anomalies in the data.
- **Anomalies to display:** Maximum number of anomalies to display in the model report. Too high a number may cause memory and UI problems.

.. _custom.models.clustering:

Custom Clustering Models
------------------------

You can make custom models using Python. Your custom models should be scikit-learn compatible:

- They must implement the methods ``fit`` and ``predict``.
- They must subclass ``sklearn.base.BaseEstimator``.
- They must receive the parameters of the ``__init__`` function as explicit keyword arguments
- ``predict`` must return a ndarray of cluster ids >= 0

For clustering tasks, the number of clusters can be passed to the model through the interface.

Moreover, the model should implement the method ``fit_predict(self, X)``, in addition to ``fit(self, X)`` and ``predict(self, X)``.

.. warning::

    Classes cannot be declared directly in the Models > Design tab. They must be packaged in a :doc:`library </python/reusing-code>` and imported, as demonstrated in the examples below.

For more details and advanced examples, please refer to :ref:`Advanced Custom Models <custom.models>`.


Example
^^^^^^^

- On the Models > Design > Algorithms tab, in the "Custom python model" code editor, you should create the ``clf`` variable.

    .. code-block:: python

        from custom_python_model import MyRandomClusteringModel

        clf = MyRandomClusteringModel()

- In ``custom_python_model.py``:

    .. code-block:: python

        from sklearn.base import BaseEstimator
        import numpy as np
        import pandas as pd

        class MyRandomClusteringModel(BaseEstimator):
            """This model assigns clusters randomly"""

            def fit(self, X):
                pass

            def predict(self, X):
                return np.random.choice([0, 1, 2], size=X.shape[0])

            def fit_predict(self, X):
                return np.random.choice([0, 1, 2], size=X.shape[0])


.. _custom.models:

Advanced Custom Models
======================

This section shows advanced concepts for building custom models.

For simple use cases, please refer to:

- :ref:`Custom models for regression <custom.models.regression>`
- :ref:`Custom models for classification <custom.models.classification>`
- :ref:`Custom models for clustering <custom.models.clustering>`

Handling parameters
-------------------

The estimator must be clonable by ``sklearn.base.clone()`` which only clones attributes that have constructor arguments with the same name.

Therefore, when using parameters at the class level, custom models should always:

- receive the parameters of the ``__init__`` function as explicit keyword arguments
- implement ``get_params(deep=True)`` and ``set_params(**params)``

These methods can either be implemented manually or by having the class extend ``sklearn.base.BaseEstimator``.

.. _column.labels:

Retrieving column names in the custom model
-------------------------------------------

In order to have access to the column names of the preprocessed dataset (ie: ``X``  in the functions ``fit`` and ``predict``), a method ``set_column_labels(self, column_labels)`` can be implemented in the model.
If this method exists, DSS will automatically call it and provide the list of the column names as argument.


.. warning::

    The column labels passed to the function ``set_column_labels`` are the labels of the prepared and preprocessed columns resulting from the preparation script followed by features handling. Hence, their name may not correspond to the original columns of the dataset.
    For instance, if automatic pairwise linear combinations were enabled, some columns may take the form: ``pw_linear:<A>+<B>``. To find the exact name of the columns, it is advisable to print the column labels received in ``set_column_labels``.

Example
^^^^^^^

- On the Models > Design > Algorithms tab, in the "Custom python model" code editor, you should create the ``clf`` variable.

    .. code-block:: python

        from custom_python_model import MyCustomRegressor

        important_column_name = ...
        clf = MyCustomRegressor(important_column_name)

- In ``custom_python_model.py``:

    .. code-block:: python

        from sklearn.base import BaseEstimator

        class MyCustomRegressor(BaseEstimator):

            def __init__(self, important_column=None, column_labels=None):
                self.important_column = important_column
                self.column_labels = column_labels

            def set_column_labels(self, column_labels):
                # in order to preserve the attribute `column_labels` when cloning
                # the estimator, we have declared it as a keyword argument in the
                # `__init__` and set it there
                self.column_labels = column_labels

            def fit(self, X, y):
                if self.important_column is not None:
                    # Retrieve the index of the important column
                    column_index = self.column_labels.index(self.important_column)

                    # Retrieve the corresponding data column
                    column = X[:, column_index]

                # Finish the implementation of the fit function
                ...

            def predict(self, X):
                # Implement the predict function
                ...

Advanced example: Setting monotonicity constraints
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following example uses XGBoost and shows how to set monotonicity constraints on specific columns given their name.

- On the Models > Design > Algorithms tab, in the "Custom python model" code editor, you should create the ``clf`` variable.

    .. code-block:: python

        from constrained_python_model import MyConstrainedRegressor

        clf = MyConstrainedRegressor(["important_column"])

- In ``constrained_python_model.py``:

    .. code-block:: python

        from xgboost import XGBRegressor
        from sklearn.base import BaseEstimator
        import numpy as np

        class MyConstrainedRegressor(BaseEstimator):

            def __init__(self, monotone_column_labels=None, column_labels=None, xgb_regressor=None):
                if monotone_column_labels is None:
                    self.monotone_column_labels = []
                else:
                    self.monotone_column_labels = monotone_column_labels
                self.column_labels = column_labels
                if xgb_regressor is None:
                    self.xgb_regressor = XGBRegressor()
                else:
                    self.xgb_regressor = xgb_regressor

            def set_column_labels(self, column_labels):
                # in order to preserve the attribute `column_labels` when cloning
                # the estimator, we have declared it as a keyword argument in the
                # `__init__` and set it there
                self.column_labels = column_labels

            def fit(self, X, y):
                # Init the constraints array
                monotone_constraints = np.zeros(X.shape[1], int)

                for monotone_column_label in self.monotone_column_labels:
                    # Retrieve the index of the column that should be monotonic
                    # NB: the corresponding data would then be X[:, monotone_column_index]
                    monotone_column_index = self.column_labels.index(monotone_column_label)

                    # Set the increasing monotonic constraint for the corresponding column
                    monotone_constraints[monotone_column_index] = 1

                # Convert the list into a XGBoost-compatible parameter
                stringified_monotone_constraints = "(" + ",".join(map(str, monotone_constraints)) + ")"

                # Instanciate and fit the XGBoost model
                self.xgb_regressor.set_params(monotone_constraints=stringified_monotone_constraints)
                self.xgb_regressor.fit(X, y)

            def predict(self, X):
                return self.xgb_regressor.predict(X)

Creating a custom clustering model using the isolation forest algorithm
-----------------------------------------------------------------------

To create a custom clustering model using the isolation forest algorithm, make sure to map values from `-1, 1` to `0, 1`.

    .. code-block:: python

        from sklearn.ensemble import IsolationForest

        class CustomIsolationForest(IsolationForest):

            def get_cluster_labels(self):
                return["regular", "anomalies"]

            def predict(self, X):
                scored = super(CustomIsolationForest, self).predict(X)
                scored[scored == 1] = 0  # "regular" cluster
                scored[scored == -1] = 1  # "anomalies" cluster
                return scored

        clf = CustomIsolationForest(n_estimators=100, random_state=0)

.. _xgboost_upgrade_macros:

XGBoost models upgrade macros
=============================

:ref:`In Dataiku 13<releases_notes.13.limitations.xgboost>`, XGBoost versions 1.5, 1.6, and 1.7 are now supported.

When upgrading, Dataiku automatically updates its base environment to use the most recent supported version available for its base Python version.

This upgrade is breaking for XGBoost models in:

- evaluate recipes
- scoring recipes without :doc:`Optimized scoring </machine-learning/scoring-engines>`
- row-level explanations
- plugin-provided model views

In order to work around all possible issues, we provide `macros (through a plugin) <https://www.dataiku.com/product/plugins/xgboost-version-bump/>`_ to upgrade saved models to a format compatible with all our supported XGBoost versions. This plugin is safe to run on all models on your instances, whether or not the backing code environment of your model has changed.