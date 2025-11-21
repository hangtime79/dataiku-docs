Vector variables
#####################

The **Vector handling** and **Missing values** methods, and their related controls, specify how a vector variable is handled.

- **Unfold (create one column per element)** creates one column per element in the vector values. The vectors in the column should only contain numerical values and all be of the same length, otherwise the handling will fail.


Missing values
----------------

There are a few choices for handling missing values in vector features.

- **Impute...** replaces missing values with the specified value.  This should be used for **randomly missing** data that are missing due to random noise.
- **Drop rows** discards rows with missing values from the model building.  *Avoid discarding rows, unless missing data is extremely rare*.
- **Fail if missing values found**
