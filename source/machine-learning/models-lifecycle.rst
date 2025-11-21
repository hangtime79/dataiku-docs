Models lifecycle
##################

Using machine learning in DSS is a process in two steps:

* The models are designed, trained, explored and selected in the **Lab**

* Once you are satisfied with your model, you **Deploy** it from the lab to the Flow, where it appears as a **Saved model**

A Saved model is deployed together with a **Training recipe** that allows you to retrain the saved models, with the same model settings, but possibly with new training data.

A Saved Model on the Flow can be used:

* For real-time APIs, using the :doc:`API node </apinode/index>`
* By a **Scoring recipe**, in order to perform prediction (or clustering) on a non-labelled dataset
