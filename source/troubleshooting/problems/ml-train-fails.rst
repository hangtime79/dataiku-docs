A ML model training fails
##########################

When the training of a machine learning fails, go to the page of the failed model. The error message is displayed. 

Depending on the cases, the error message itself can contain enough information to understand the issue, or you may need to get the logs, which you can access by clicking the "Read the logs" link.

MemoryError (In-memory training only)
=========================================

A common error is the "MemoryError" which indicates that the Python process running the training encountered an out of memory situation, due to exhaustion of the machine's memory.

For machine learning, a preprocessing is applied to your input dataset, which can strongly increase the memory size required compared to the original size of the data.

For example, with "dummy-encoding" processing, a single categorical column can be transformed to hundreds of numerical columns. To know how many columns were created as part of the preprocessing, you can check in the logs for the "shape" messages in the logs.

To reduce memory requirements, you can:

* Reduce the dataset sample used for machine learning
* Reduce the maximum number of columns created by dummy-encoding
* Switch dummy-encoding to impact-encoding (which creates a single output column)
* For text features, avoid using "Hashing" if the algorithm doesn't support sparse inputs (you get a warning in that case)

Process died (killed - maybe out of memory)
=============================================

The process that was running the machine learning was killed, either by a system administrator or the kernel.
A common cause is that the machine's memory was exhausted.

When using Python training, please see above for tips on managing memory usage.
