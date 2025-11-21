Input and output formats
########################

DSS provides support for common input/output formats used by cloud vendors:

.. contents::
    :local:

.. warning:: Many input formats do not offer a way to provide column names. For those formats, endpoints rely on the field order. Please be extra careful to ensure that the order of your dataset columns matches what the endpoint expects.

Amazon SageMaker
----------------

Supported input formats
~~~~~~~~~~~~~~~~~~~~~~~

* ``INPUT_SAGEMAKER_CSV``: SageMaker - CSV

  .. code-block::

    # Sample input dataframe:
    Pclass   Age  SibSp  Parch   Fare
    200     22.0      1      0   7.2500
    200     38.0      1      0   71.2833

    # Corresponding request body:
    200,22.0,1,0,7.25
    200,38.0,1,0,71.2833

* ``INPUT_SAGEMAKER_JSON``: SageMaker - JSON

  .. code-block::

    # Sample input dataframe:
    col_1  col_2  col_3
     3      49     13
     2      68     30

    # Corresponding request body:
    {
      "instances": [
        {
          "features": [
            3,
            49,
            13
          ]
        },
        {
          "features": [
            2,
            68,
            30
          ]
        }
      ]
    }

* ``INPUT_SAGEMAKER_JSON_EXTENDED``: SageMaker - JSON (Extended)

  .. code-block::

    # Sample input dataframe:
    col_1  col_2  col_3
     3      49     13
     2      68     30

    # Corresponding request body:
    {
      "instances": [
        {
          "data": {
            "features": {
              "values": [
                3,
                49,
                13
              ]
            }
          }
        },
        {
          "data": {
            "features": {
              "values": [
                2,
                68,
                30
              ]
            }
          }
        }
      ]
    }

* ``INPUT_SAGEMAKER_JSONLINES``: SageMaker - JSONLINES

  .. code-block::

    # Sample input dataframe:
    col_1  col_2  col_3
     3      49     13
     2      68     30

    # Corresponding request body (one JSON-formatted record per row):
    {"features": [3, 49, 13]}
    {"features": [2, 68, 30]}

* ``INPUT_DEPLOY_ANYWHERE_ROW_ORIENTED_JSON``: Deploy Anywhere - Row oriented JSON

  .. code-block::

    # Sample input dataframe:
    col_1  col_2  col_3
     3      49     13
     2      68     30

    # Corresponding request body:
    {
      "items": [
        {
          "features": {
            "col_1": 3,
            "col_2": 49,
            "col_3": 13
          }
        },
        {
          "features": {
            "col_1": 2,
            "col_2": 68,
            "col_3": 30
          }
        }
      ]
    }

Supported output formats
~~~~~~~~~~~~~~~~~~~~~~~~

* ``OUTPUT_SAGEMAKER_CSV``: SageMaker - CSV

  .. code-block::

    # Sample response, binary prediction, 2 rows:
    0
    1

    # Sample response, binary prediction, with probabilities, 2 rows:
    0,"[0.9992051720619202, 0.0007948523852974176]"
    1,"[0.0008897185325622559, 0.9991102814674377]"

* ``OUTPUT_SAGEMAKER_ARRAY_AS_STRING``: SageMaker - Array as string

  .. code-block::

    # Sample response, binary prediction, 2 rows:
    [0,1]

    # Sample response, binary prediction, no leading square brackets, 2 rows:
    0,1


* ``OUTPUT_SAGEMAKER_JSON``: SageMaker - JSON

  .. code-block::

    # Sample response, multiclass prediction (4 classes) with probabilities, 2 rows:
    {
      "predictions": [
        {
          "score": [
            0.2609631419181824,
            0.24818938970565796,
            0.19304637610912323,
            0.29780113697052
          ],
          "predicted_label": 3
        },
        {
          "score": [
            0.29569414258003235,
            0.23015224933624268,
            0.19619841873645782,
            0.27795517444610596
          ],
          "predicted_label": 0
        }
      ]
    }

* ``OUTPUT_SAGEMAKER_JSONLINES``: SageMaker - JSONLINES

  .. code-block::

    # Sample response, multiclass prediction (4 classes) with probabilities, 2 rows:
    {"score": [0.2609631419181824, 0.24818938970565796, 0.19304637610912323, 0.29780113697052], "predicted_label": 3}
    {"score": [0.29569414258003235, 0.23015224933624268, 0.19619841873645782, 0.27795517444610596], "predicted_label": 0}

* ``OUTPUT_DEPLOY_ANYWHERE_JSON``: Deploy Anywhere - JSON

  .. code-block::

    # Sample response, multiclass prediction (4 classes) with probabilities, 2 rows:
    {
      "results": [
        {
          "probas": {
            "0": 0.2609631419181824,
            "1": 0.24818938970565796,
            "2": 0.19304637610912323,
            "3": 0.29780113697052
          },
          "prediction": "3"
        },
        {
          "probas": {
            "0": 0.29569414258003235,
            "1": 0.23015224933624268,
            "2": 0.19619841873645782,
            "3": 0.27795517444610596
          },
          "prediction": "0"
        }
      ]
    }

Azure Machine Learning
----------------------

Supported input formats
~~~~~~~~~~~~~~~~~~~~~~~

* ``INPUT_AZUREML_JSON_INPUTDATA``: Azure ML - JSON (input_data)

  .. code-block::

    # Sample input dataframe:
    Pclass   Age  SibSp  Parch   Fare
    200     22.0      1      0   7.2500
    200     38.0      1      0   71.2833


    # Corresponding request body:
    {
      "input_data": [
        [
          200,
          22,
          1,
          0,
          7.25
        ],
        [
          200,
          38,
          1,
          0,
          71.2833
        ]
      ]
    }

* ``INPUT_AZUREML_JSON_INPUTDATA_DATA``: Azure ML - JSON (input_data with data and columns)

  .. code-block::

    # Sample input dataframe:
    x1_var  x2_var  x3_var
     12      74      19
     15      64      8

    # Corresponding request body:
    {
      "input_data": {
        "columns": [
          "x1_var",
          "x2_var",
          "x3_var"
        ],
        "data": [
          [
            12,
            74,
            19
          ],
          [
            15,
            64,
            8
          ]
        ]
      }
    }

* ``INPUT_AZUREML_JSON_WRITER``: Azure ML - JSON (Inputs/data)

  .. code-block::

    # Sample input dataframe:
    Pclass   Age  SibSp  Parch   Fare
    200     22.0      1      0   7.2500
    200     38.0      1      0   71.2833

    # Corresponding request body:
    {
      "Inputs": {
        "data": [
          {
            "Pclass": 200,
            "Age": 22,
            "SibSp": 1,
            "Parch": 0,
            "Fare": 7.25
          },
          {
            "Pclass": 200,
            "Age": 38,
            "SibSp": 1,
            "Parch": 0,
            "Fare": 71.2833
          }
        ]
      },
      "GlobalParameters": {
        "method": "predict_proba"
      }
    }

* ``INPUT_DEPLOY_ANYWHERE_ROW_ORIENTED_JSON``: Deploy Anywhere - Row oriented JSON

  .. code-block::

    # Sample input dataframe:
    col_1  col_2  col_3
     3      49     13
     2      68     30

    # Corresponding request body:
    {
      "items": [
        {
          "features": {
            "col_1": 3,
            "col_2": 49,
            "col_3": 13
          }
        },
        {
          "features": {
            "col_1": 2,
            "col_2": 68,
            "col_3": 30
          }
        }
      ]
    }

Supported output formats
~~~~~~~~~~~~~~~~~~~~~~~~

* ``OUTPUT_AZUREML_JSON_OBJECT``: Azure ML - JSON (Object)

  .. code-block::

    # Sample response, binary prediction, 2 rows:
    {
      "Results": [
        [
          0.9611595387201834,
          0.03884045978970049
        ],
        [
          0.04262458780881131,
          0.9573754121911887
        ]
      ]
    }

* ``OUTPUT_AZUREML_JSON_ARRAY``: Azure ML - JSON (Array)

  .. code-block::

    # Sample response, regression, 2 rows:
    [273.7416544596354, 279.99419962565105]

* ``OUTPUT_DEPLOY_ANYWHERE_JSON``: Deploy Anywhere - JSON

  .. code-block::

    # Sample response, multiclass prediction (4 classes) with probabilities, 2 rows:
    {
      "results": [
        {
          "probas": {
            "0": 0.2609631419181824,
            "1": 0.24818938970565796,
            "2": 0.19304637610912323,
            "3": 0.29780113697052
          },
          "prediction": "3"
        },
        {
          "probas": {
            "0": 0.29569414258003235,
            "1": 0.23015224933624268,
            "2": 0.19619841873645782,
            "3": 0.27795517444610596
          },
          "prediction": "0"
        }
      ]
    }

Google Vertex AI
----------------------

Supported input formats
~~~~~~~~~~~~~~~~~~~~~~~

* ``INPUT_VERTEX_DEFAULT``: Vertex - default

  .. code-block::

    # Sample input dataframe:
    Pclass   Age  SibSp  Parch   Fare
    200     22.0      1      0   7.2500
    200     38.0      1      0   71.2833

    # Corresponding request body:
    {
      "instances": [
        {
          "Pclass": "200",
          "Age": "22.0",
          "SibSp": "1",
          "Parch": "0",
          "Fare": "7.25"
        },
        {
          "Pclass": "200",
          "Age": "22.0",
          "SibSp": "1",
          "Parch": "0",
          "Fare": "7.25"
        }
      ]
    }

Supported output formats
~~~~~~~~~~~~~~~~~~~~~~~~

* ``OUTPUT_VERTEX_DEFAULT``: Vertex - default

  .. code-block::

    # Sample response, binary prediction, 2 rows
    [
      {
        "classes": [
          "0",
          "1"
        ],
        "scores": [
          0.8098086714744568,
          0.190191388130188
        ]
      },
      {
        "classes": [
          "0",
          "1"
        ],
        "scores": [
          0.8098086714744568,
          0.190191388130188
        ]
      }
    ]


Databricks
----------------------

Supported input formats
~~~~~~~~~~~~~~~~~~~~~~~

* ``INPUT_RECORD_ORIENTED_JSON``: Databricks - Record oriented JSON

  .. code-block::

    # Sample input dataframe:
    Pclass   Age  SibSp  Parch   Fare
    200     22.0      1      0   7.2500
    200     38.0      1      0   71.2833

    # Corresponding request body:
    {
        "dataframe_records": [
            {
                "Pclass": 200,
                "Age": 22.0,
                "SibSp": 1,
                "Parch": 0,
                "Fare": 7.25
            },
            {
                "Pclass": 200,
                "Age": 38.0,
                "SibSp": 1,
                "Parch": 0,
                "Fare": 71.2833
            }
        ]
    }

* ``INPUT_SPLIT_ORIENTED_JSON``: Databricks - Split oriented JSON

  .. code-block::

    # Sample input dataframe:
    Pclass   Age  SibSp  Parch   Fare
    200     22.0      1      0   7.2500
    200     38.0      1      0   71.2833

    # Corresponding request body:
    {
        "dataframe_split": [{
            "index": [0, 1],
            "columns": ["Pclass", "Age", "SibSp", "Parch", "Fare"],
            "data": [[200, 22.0, 1, 0, 7.25], [200, 38.0, 1, 0, 71.2833]]
        }]
    }

* ``INPUT_TF_INPUTS_JSON``: Databricks - TF Inputs JSON

  .. code-block::

    # Sample input dataframe:
    Pclass   Age  SibSp  Parch   Fare
    200     22.0      1      0   7.2500
    200     38.0      1      0   71.2833

    # Corresponding request body:
    {
        "inputs": {
            "Pclass": [200, 200],
            "Age": [22.0, 38.0],
            "SibSp": [1, 1],
            "Parch": [0, 0],
            "Fare": [7.25, 71.2833]
        }
    }

* ``INPUT_TF_INSTANCES_JSON``: Databricks - TF Instances JSON

  .. code-block::

    # Sample input dataframe:
    Pclass   Age  SibSp  Parch   Fare
    200     22.0      1      0   7.2500
    200     38.0      1      0   71.2833

    # Corresponding request body:
    {
        "instances": [
            {
                "Pclass": 200,
                "Age": 22.0,
                "SibSp": 1,
                "Parch": 0,
                "Fare": 7.25
            },
            {
                "Pclass": 200,
                "Age": 38.0,
                "SibSp": 1,
                "Parch": 0,
                "Fare": 71.2833
            }
        ]
    }

* ``INPUT_DATABRICKS_CSV``: Databricks - CSV

  .. code-block::

    # Sample input dataframe:
    Pclass   Age  SibSp  Parch   Fare
    200     22.0      1      0   7.2500
    200     38.0      1      0   71.2833

    # Corresponding request body:
    200,22.0,1,0,7.25
    200,38.0,1,0,71.2833

Supported output formats
~~~~~~~~~~~~~~~~~~~~~~~~

* ``OUTPUT_DATABRICKS_JSON``: Databricks - JSON

  .. code-block::

    # Sample response, binary prediction without probabilities, 2 rows:
    {
        "predictions": [0, 1]
    }


    # Sample response, binary prediction with probabilities, 2 rows:
    {
        "predictions": [0, 1],
        "probability": [[0.9611595387201834, 0.03884045978970049], [0.04262458780881131, 0.9573754121911887]]
    }

    # or:
    {
        "predictions": [0, 1],
        "probabilities": [[0.9611595387201834, 0.03884045978970049], [0.04262458780881131, 0.9573754121911887]]
    }

    # or:
    {
        "predictions": [[0.9611595387201834, 0.03884045978970049], [0.04262458780881131, 0.9573754121911887]]
    }
