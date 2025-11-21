Performance Drift
###################

Performance Drift is in a sense the "most straightforward" kind of drift analysis. It analyses whether the actual performance of the model changes.

However, having ground truth / labels is naturally required for Performance Drift, which is not always possible. See :doc:`/mlops/model-evaluations/automating` for a discussion on this.

When Ground truth is not available, :doc:`input-data-drift` and :doc:`prediction-drift` can provide insights into whether you have a concept drift.