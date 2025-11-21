Step 2: Test different Machine Learning models for heart failures prediction
============================================================================

In this notebook, we will test different Machine Learning approaches to
predict heart failures using
`scikit-learn <https://scikit-learn.org/stable/>`__ models (logistic
regression, SVM, decision tree, and random forest). For each model, we
will first perform a grid search to find the best parameters, then train
the model on the train set using these best parameters and finally log
everything (parameters, performance metrics, and models) to keep track
of the results of our different experiments and be able to compare
afterward. Our `Experiment Tracking
capability <https://doc.dataiku.com/dss/latest/mlops/experiment-tracking/index.html>`__
relies on the `MLflow
framework <https://www.mlflow.org/docs/2.17.2/tracking.html>`__.

*Tip:* Experiment Tracking allows you to save all experiment-related
information that you care about for every experiment you run. In
Dataiku, this can be done when coding using the `MLflow Tracking
API <https://www.mlflow.org/docs/2.17.2/tracking.html>`__. You can then
explore and compare all your experiments in the Experiment Tracking UI.

0. Import packages
------------------

**Make sure you’re using the correct code environment** (see
prerequisites)

To be sure, go to **Kernel > Change kernel** and choose
``py_quickstart``

.. code:: ipython3

    %pylab inline


.. parsed-literal::

    Populating the interactive namespace from numpy and matplotlib


.. code:: ipython3

    import dataiku
    from dataiku import pandasutils as pdu
    import pandas as pd
    from utils import model_training
    import mlflow
    from sklearn.linear_model import LogisticRegression
    from sklearn.svm import SVC
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.ensemble import RandomForestClassifier


.. code:: ipython3

    import warnings
    warnings.filterwarnings('ignore')

.. code:: ipython3

    client = dataiku.api_client()
    client._session.verify = False

1. Import the train dataset
---------------------------

.. code:: ipython3

    dataset_heart_measures_train = dataiku.Dataset("heart_measures_train")
    df = dataset_heart_measures_train.get_dataframe(limit=100000)

2. Set the experiment environment
---------------------------------

As we would like to keep track of all the experiment-related information
(performance metrics, parameters and models) for our different ML
experiments, we must use a Dataiku managed folder to store all this
information. This section is about creating (or accessing if it already
exists) the required managed folder.

2.1 Set the required parameters for creating/accessing the managed folder
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: ipython3

    # Set parameters
    experiment_name = "Binary Heart Disease Classification"
    experiments_managed_folder_name = "Binary classif experiments"
    project = client.get_default_project()
    mlflow_extension = project.get_mlflow_extension()

2.2 Create/access the managed folder
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: ipython3

    # Create the managed folder if it doesn't exist
    if experiments_managed_folder_name not in [folder['name'] for folder in project.list_managed_folders()]:
        connections = client.list_connections_names('all')
        for connection in connections:
            try:
                project.create_managed_folder(experiments_managed_folder_name, connection_name=connection)
                break
            except Exception:
                continue
        
    # Get the managed folder id
    experiments_managed_folder_id = [folder['id'] for folder in project.list_managed_folders() if folder['name']==experiments_managed_folder_name][0] 
    
    # Get the managed folder using the id
    experiments_managed_folder = project.get_managed_folder(experiments_managed_folder_id)  

2.3 Prepare data for training
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: ipython3

    # Prepare data for experiment
    target= ["HeartDisease"]
    X = df.drop(target, axis=1)
    y = df[target[0]]

3. Test different modeling approaches
-------------------------------------

This section will test different models: a Logistic Regression, an SVM,
a Decision Tree, and a Random Forest. For each type of model, we will
proceed in several steps:

1. Set the experiment (where to log the results) and start a new run.

2. Define the set of hyperparameters to test.

3. Perform a grid search on these hyperparameters using the
   ``find_best_parameters`` function from the ``model_training.py`` file
   in the project library.

4. Cross-evaluate the model with the best hyperparameters on 5 folds
   using the ``cross_validate_scores`` function from the
   ``model_training.py`` file in the project library.

5. Train the model on the train set using the best hyperparameters.

6. Log the experiment’s results (parameters, performance metrics, and
   model).

You can find more information on the tracking APIs in the `MLflow
tracking
documentation <https://www.mlflow.org/docs/2.17.2/tracking.html>`__.

3.1 Logistic Regression
~~~~~~~~~~~~~~~~~~~~~~~

We use the `Scikit-Learn Logistic
Regression <https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html>`__
model.

.. code:: ipython3

    with project.setup_mlflow(managed_folder=experiments_managed_folder) as mlflow:
        mlflow.set_experiment(experiment_name)
    
        with mlflow.start_run(run_name="Linear Regression"):
            
            # Find best hyper parameters using a grid search
            lr = LogisticRegression(random_state = 42)
            cv = 5
            params = {'penalty':['none','l2']}
            scoring = ['accuracy', 'precision', 'recall', 'roc_auc', 'f1']
            print("Searching for best parameters...")
            lr_best_params = model_training.find_best_parameters(X, y, lr, params, cv=cv)
            print(f"Best parameters: {lr_best_params}")
            
            # Set the best hyper parameters
            lr.set_params(**lr_best_params)
            
            # Cross evaluate the model on the best hyper parameters
            lr_metrics_results = model_training.cross_validate_scores(X, y, lr, cv=cv, scoring=scoring)
            print(f'Average values for evaluation metrics after cross validation: {", ".join(f"{key}: {round(value, 2)}" for key, value in lr_metrics_results.items())}')
            
            # Train the model on the whole train set
            lr.fit(X,y)
            
            # Log the experiment results 
            mlflow.log_params(lr_best_params)
            mlflow.log_metrics(lr_metrics_results)
            mlflow.sklearn.log_model(lr, artifact_path="model")
            print("Best parameters, cross validation metrics, and the model have been saved to Experiment Tracking")


.. parsed-literal::

    2024/06/28 21:09:16 INFO mlflow.tracking.fluent: Experiment with name 'Binary Heart Disease Classification' does not exist. Creating a new experiment.


.. parsed-literal::

    Searching for best parameters...
    Best parameters: {'penalty': 'l2'}
    Average values for evaluation metrics after cross validation: accuracy: 0.86, precision: 0.86, recall: 0.89, roc_auc: 0.91, f1: 0.87
    Best parameters, cross validation metrics, and the model have been saved to Experiment Tracking


3.2 Support Vector Machine:
~~~~~~~~~~~~~~~~~~~~~~~~~~~

We use the `Scikit-Learn
SVC <https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html>`__
model.

.. code:: ipython3

    with project.setup_mlflow(managed_folder=experiments_managed_folder) as mlflow:
        mlflow.set_experiment(experiment_name)
    
        with mlflow.start_run(run_name="SVM"):
            
            # Find best hyper parameters using a grid search
            svm = SVC(random_state = 42)
            cv = 5
            params = {'C': [0.1,1, 10], 'gamma': [1,0.1,0.01,0.001],'kernel': ['rbf', 'poly', 'sigmoid']}
            scoring = ['accuracy', 'precision', 'recall', 'roc_auc', 'f1']
            print("Searching for best parameters...")
            svm_best_params = model_training.find_best_parameters(X, y, svm, params, cv=cv)
            print(f"Best parameters: {svm_best_params}")
            
            # Set the best hyper parameters
            svm.set_params(**svm_best_params)
            
            # Cross evaluate the model on the best hyper parameters
            svm_metrics_results = model_training.cross_validate_scores(X, y, svm, cv=cv, scoring=scoring)
            print(f'Average values for evaluation metrics after cross validation: {", ".join(f"{key}: {round(value, 2)}" for key, value in svm_metrics_results.items())}')
            
            # Train the model on the whole train set
            svm.fit(X,y)
            
            # Log the experiment results 
            mlflow.log_params(svm_best_params)
            mlflow.log_metrics(svm_metrics_results)
            mlflow.sklearn.log_model(svm, artifact_path="model")
            print("Best parameters, cross validation metrics, and the model have been saved to Experiment Tracking")


.. parsed-literal::

    Searching for best parameters...
    Best parameters: {'C': 10, 'gamma': 0.01, 'kernel': 'rbf'}
    Average values for evaluation metrics after cross validation: accuracy: 0.87, precision: 0.86, recall: 0.91, roc_auc: 0.92, f1: 0.89
    Best parameters, cross validation metrics, and the model have been saved to Experiment Tracking


3.3 Decision Tree:
~~~~~~~~~~~~~~~~~~

We use the `Scikit-Learn Decision
Tree <https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html#sklearn.tree.DecisionTreeClassifier>`__
model.

.. code:: ipython3

    with project.setup_mlflow(managed_folder=experiments_managed_folder) as mlflow:
        mlflow.set_experiment(experiment_name)
    
        with mlflow.start_run(run_name="Decision Tree"):
            
            # Find best hyper parameters using a grid search
            dtc = DecisionTreeClassifier(random_state = 42)
            cv = 5
            params = {'max_depth' : [4,5,6,7,8],
                      'criterion' :['gini', 'entropy']}
            scoring = ['accuracy', 'precision', 'recall', 'roc_auc', 'f1']
            print("Searching for best parameters...")
            dtc_best_params = model_training.find_best_parameters(X, y, dtc, params, cv=cv)
            print(f"Best parameters: {dtc_best_params}")
            
            # Set the best hyper parameters
            dtc.set_params(**dtc_best_params)
            
            # Cross evaluate the model on the best hyper parameters
            dtc_metrics_results = model_training.cross_validate_scores(X, y, dtc, cv=cv, scoring=scoring)
            print(f'Average values for evaluation metrics after cross validation: {", ".join(f"{key}: {round(value, 2)}" for key, value in dtc_metrics_results.items())}')
            
            # Train the model on the whole train set
            dtc.fit(X,y)
            
            # Log the experiment results 
            mlflow.log_params(dtc_best_params)
            mlflow.log_metrics(dtc_metrics_results)
            mlflow.sklearn.log_model(dtc, artifact_path="model")
            print("Best parameters, cross validation metrics, and the model have been saved to Experiment Tracking")


.. parsed-literal::

    Searching for best parameters...
    Best parameters: {'criterion': 'gini', 'max_depth': 6}
    Average values for evaluation metrics after cross validation: accuracy: 0.82, precision: 0.84, recall: 0.83, roc_auc: 0.83, f1: 0.84
    Best parameters, cross validation metrics, and the model have been saved to Experiment Tracking


3.4 Random Forest:
~~~~~~~~~~~~~~~~~~

We use the `Scikit-Learn Random
Forest <https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html>`__
model.

.. code:: ipython3

    with project.setup_mlflow(managed_folder=experiments_managed_folder) as mlflow:
        mlflow.set_experiment(experiment_name)
    
        with mlflow.start_run(run_name="Random Forest"):
            
            # Find best parameters and cross evaluate the model on the best parameters
            rfc = RandomForestClassifier(random_state = 42)
            cv = 5
            params = {'n_estimators': [100,200,300],
                      'max_depth' : [5,6,7],
                      'criterion' :['gini', 'entropy']}
            scoring = ['accuracy', 'precision', 'recall', 'roc_auc', 'f1']
            print("Searching for best parameters...")
            rfc_best_params = model_training.find_best_parameters(X, y, rfc, params, cv=cv)
            print(f"Best parameters: {rfc_best_params}")
            
            # Set the best hyper parameters
            rfc.set_params(**rfc_best_params)
    
            # Cross evaluate the model on the best hyper parameters
            rfc_metrics_results = model_training.cross_validate_scores(X, y, rfc, cv=cv, scoring=scoring)
            print(f'Average values for evaluation metrics after cross validation: {", ".join(f"{key}: {round(value, 2)}" for key, value in rfc_metrics_results.items())}')
            
            # Train the model using the best parameters
            rfc.fit(X,y)
            
            # Log the experiment results 
            mlflow.log_params(rfc_best_params)
            mlflow.log_metrics(rfc_metrics_results)
            mlflow.sklearn.log_model(rfc, artifact_path="model")
            print("Best parameters, cross validation metrics, and the model have been saved to Experiment Tracking")


.. parsed-literal::

    Searching for best parameters...
    Best parameters: {'criterion': 'gini', 'max_depth': 7, 'n_estimators': 200}
    Average values for evaluation metrics after cross validation: accuracy: 0.87, precision: 0.86, recall: 0.91, roc_auc: 0.92, f1: 0.88
    Best parameters, cross validation metrics, and the model have been saved to Experiment Tracking


4. Explore the results
----------------------

All done! We can now look at the results & compare our different models
by going to the Experiment Tracking page (on the top bar, hover over the
circle icon, and select **Experiment Tracking**.
