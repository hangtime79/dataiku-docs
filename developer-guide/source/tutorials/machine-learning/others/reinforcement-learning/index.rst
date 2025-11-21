Using Reinforcement Learning for Hyperparameter Tuning
******************************************************

Introduction
############

In modern machine learning tasks, choosing the best hyperparameters for a model to perform well is essential.
In this tutorial, we use a reinforcement learning approach to automatically tune the hyperparameters
of a random forest classifier.
We simulate a dataset and use a simple Q-learning algorithm to search for the best combination.
This approach combines global exploration with local fine-tuning (called "exploitation")
to avoid getting stuck in a local optimum.


Prerequisites
#############

* Dataiku 13.3
* Python 3.9
* A code environment with the following packages:
  
  .. code-block:: python

    numpy
    scikit-learn


Importing the required packages
###############################

We first import all the libraries needed for this tutorial.

.. literalinclude:: ./assets/notebook.py
    :language: python
    :lines: 1-5

Preparing the dataset
#####################

We simulate a dataset for a classification task (binary by default) with 1000 samples and 20 features.
The data is then split into training and validation sets.

.. literalinclude:: ./assets/notebook.py
    :language: python
    :lines: 7-8

Defining the hyperparameter space
#################################

We define the options for the number of estimators and the maximum tree depth.
These arrays represent our search space.

.. literalinclude:: ./assets/notebook.py
    :language: python
    :lines: 10-11

Initializing the Q table and reinforcement learning parameters
##############################################################

We create a Q table filled with zeros.
The table dimensions correspond to the number of options in each hyperparameter.
We also set reinforcement learning parameters like epsilon, alpha, gamma, and the number of episodes.

.. literalinclude:: ./assets/notebook.py
    :language: python
    :lines: 13-18

Run reinforcement learning for hyperparameter Tuning
####################################################

We run a loop over several episodes and inner steps.
In each step, we select a new state by either exploring (choosing random hyperparameters)
or exploiting (choosing the best combination seen so far).
Then, we train a random forest classifier with the selected hyperparameters
and compute its accuracy on the validation set.
This accuracy serves as our reward for updating the Q table.

.. note:: 
    Using both episodes & inner steps is a way to restart the learning process from different initial conditions.
    Like the exploitation/exploration balance, it allows for global exploration
    and local fine-tuning and helps avoid getting stuck in local optima.

.. literalinclude:: ./assets/notebook.py
    :language: python
    :lines: 20-52

Retrieving the best hyperparameters
###################################

After the learning loop,
we find the best hyperparameter combination by taking the indexes of the maximum values in our Q-table.

.. literalinclude:: ./assets/notebook.py
    :language: python
    :lines: 54-59

Training the final model on the full dataset
#############################################
We train the random forest classifier on the full dataset using the best hyperparameters obtained from the reinforcement learning process.

.. literalinclude:: ./assets/notebook.py
    :language: python
    :lines: 61-

Wrapping up
###########

In this tutorial, we applied a reinforcement learning approach to tuning the hyperparameters of a random forest classifier. The Q learning algorithm helped us explore the hyperparameter space and gradually fine-tune the selection using the validation accuracy as the reward. This method can help avoid the common pitfalls of manual tuning and finding a balanced solution between exploration and exploitation.
As a next step, you can follow :doc:`this tutorial </tutorials/machine-learning/model-import/scikit-pipeline/index>`
to import your trained model into a Dataiku Saved Model.

Here is the complete code of this tutorial:


.. dropdown:: :download:`notebook.py<./assets/notebook.py>`
    :open:

    .. literalinclude:: ./assets/notebook.py
        :language: python
