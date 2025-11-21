Evaluation Metrics
##################

For Object detection, the model will maximize the F1 score by default, which is a weighted average of the precision and recall. Depending on your use case, you may want to optimize for either recall or precision:

  * Maximizing the recall will train the model to predict marginally likely objects, which is useful in cases where your classes of interest are under-represented in your training data.
  * Maximizing the precision will predict only the most likely objects, which is useful in cases where your classes of interest are well-represented in your training data.

For Image classification the model will maximize the ROC AUC score by default but other multiclass metrics are available: Precision, Recall, F1 score, Accuracy, Log Loss and Average Precision.
