The Javascript API
#########################

.. contents::
    :local:

The Dataiku Javascript API allows you to write custom Web apps that can read from the Dataiku datasets.

Fetching dataset data
-----------------------

.. js:function:: dataiku.fetch(datasetName, [options], success, failure)

    Returns a DataFrame object with the contents of a dataset

    :param string datasetName: Name of the dataset. Can be in either of two formats

        * projectKey.datasetName
        * datasetName. In this case, the default project will be searched

    :param dict options: Options for the call. Valid keys are:

            * apiKey: forced API key for this dataset. By default, dataiku.apiKey is used
            * partitions: array of partition ids to fetch. By default, all partitions are fetched.
            * sampling: sampling method to apply. By default, the first 20000 records are retrieved. See below for the available sampling methods.
            * filter: formula for filtering which rows are returned.
            * limit : maximum number of rows to be retrieved, used by "head", "random", "random-column" and "sort-column".
            * ratio : define the max row count as a ratio (between 0 and 1) of the dataset's total row count, used by "head", "random", "random-column" and "sort-column".
            * ascending : sort in ascending order the selected column of the "sort-column" sampling, defaults to true.

    :param function(dataframe) success:
        Gets called in case of success with a Dataframe object

    :param function(error) failure:
        Gets called in case of error

The DataFrame object
-----------------------

.. js:class:: DataFrame

    Object representing a set of rows from a dataset.

    DataFrame objects are created by dataiku.fetch

    Interaction with the rows in a DataFrame can be made either:

        * As "record" objects, which map each column name to value
        * As "row" arrays. Each row array contains one entry per column

    Using row arrays requires a bit more code and using getColumnIdx, but generally provides
    better performance.

.. js:function:: DataFrame.getNbRows()

    :returns: the number of rows in the dataframe

.. js:function:: DataFrame.getRow(rowIdx)

    :returns: an array representing the row with a given row idx

.. js:function:: DataFrame.getColumnNames()

    :returns: an array of column names

.. js:function:: DataFrame.getRows()

    :returns: an array of dataframe rows. Each element of the array is what getRow would return

.. js:function:: DataFrame.getRecord(rowIdx)

    :returns: a record object for the row with a given row idx. The keys of the object are the names of the columns

.. js:function:: DataFrame.getColumnValues(name)

    :param string name: Name of the column

    :returns: an array containing all values of the column <name>

.. js:function:: DataFrame.getColumnIdx(name)

    Returns the columnIdx of the column bearing the name name. This idx can be used to lookup in the array returned by getRow.

    Returns -1 if the column name is not found.

    :param string name: Name of the column
    :returns: the columnIdx of the column or -1

.. js:function:: DataFrame.mapRows(f)

    Applies a function to each row

    :param function(row) f: Function to apply to each row array
    :returns: the array [ f(row[0]), f(row[1]), ... , f(row[N-1]) ]

.. js:function:: DataFrame.mapRecords(f)

    Applies a function to each record array

    :param function(record) f: Function to apply to each record object

    :returns: the array [ f(record[0]), f(record[1]), ... , f(record[N-1]) ]


.. js:function:: dataiku.setAPIKey(apiKey)

    Sets the API key to use. This should generally be the first thing called

.. js:function:: dataiku.setDefaultProjectKey(projectKey)

    Sets the "search path" for projects. This is used to resolve dataset names given as
    "datasetName" instead of "projectKey.datasetName".

Sampling
----------

Returning a whole dataset as a JS object is generally not possible due to memory reasons. The API allows you to sample the rows of the dataset, with option keys.

The **sampling** key contains the sampling method to use

For more details on the sampling methods, see :doc:`/preparation/sampling`

.. note::

    The default sampling is **head(20000)**: by default, only the first 20K rows are returned

sampling = 'head'
%%%%%%%%%%%%%%%%%%

Returns the first rows of the dataset

.. code-block:: js

    /* Returns the first 15 000 lines */
    {
        sampling : 'head',
        limit : 15000
    }

sampling = 'random'
%%%%%%%%%%%%%%%%%%%

Returns either a number of rows, randomly picked, or a ratio of the dataset

.. code-block:: js

    /* Returns 10% of the dataset */
    {
        sampling : 'random',
        ratio: 0.1
    }

.. code-block:: js

    /* Returns 15000 rows, randomly sampled */
    {
        sampling : 'random',
        limit : 15000
    }

sampling = 'full'
%%%%%%%%%%%%%%%%%%

No sampling, returns all


sampling = 'random-column'
%%%%%%%%%%%%%%%%%%%%%%%%%%%%

Returns a number of rows based on the values of a column

.. code-block:: js

    /* Returns 15000 rows, randomly sampled among the values of column 'user_id' */
    {
        sampling : 'random-column',
        sampling_column : 'user_id',
        limit : 15000
    }


sampling = 'sort-column'
%%%%%%%%%%%%%%%%%%%%%%%%%%%%

Returns the first rows of the dataset after sorting by a column

.. code-block:: js

    /* Returns the 15000 rows with largest values for column 'amount' */
    {
        sampling : 'sort-column',
        sampling_column : 'amount',
        limit : 15000,
        ascending : false
    }

Partitions selection
----------------------

In the ``partitions`` key, you can pass in a JS array of partition identifiers

.. code-block:: js

    /* Only returns data from two partitions */
    {
       partitions : ["2014-01-02", "2014-02-04"]
    }

Columns selection
----------------------

In the ``columns`` key, you can pass in a JS array of column names. Only these columns are returned

.. code-block:: js

    /* Only returns two columns from the dataset */
    {
      columns : ["type", "price"]
    }

Rows filtering
----------------------

In the ``filter`` key, you can pass a custom formula to filter the returned rows

.. code-block:: js

    /* Only returns rows matching condition */
    {
        filter : "type == 'event' && price > 2000"
    }
