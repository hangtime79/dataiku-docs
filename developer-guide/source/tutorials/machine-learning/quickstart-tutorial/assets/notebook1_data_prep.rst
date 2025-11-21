Step 1: Prepare the input dataset for ML modeling
=================================================

The project is based on the `Heart Failure Prediction
Dataset <https://www.kaggle.com/datasets/fedesoriano/heart-failure-prediction>`__.

This first notebook:

-  Performs a quick exploratory analysis of the input dataset: it looks
   at the structure of the dataset and the distribution of the values in
   the different categorical and continuous columns.

-  Uses the functions from the project Python library to clean & prepare
   the input dataset before Machine Learning modeling. We will first
   clean categorical and continuous columns, then split the dataset into
   a train set and a test set.

Finally, we will transform this notebook into a Python recipe in the
project Flow that will output the new train and test datasets.

*Tip*: `Project
libraries <https://doc.dataiku.com/dss/latest/python/reusing-code.html#sharing-python-code-within-a-project>`__
allow you to build shared code repositories. They can be synchronized
with an external Git repository.

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
    import matplotlib.pyplot as plt
    import seaborn as sns
    import math
    from utils import data_processing
    from sklearn.preprocessing import RobustScaler
    from sklearn.model_selection import train_test_split


.. code:: ipython3

    import warnings
    warnings.filterwarnings('ignore')

1. Import the data
------------------

Let’s use the Dataiku Python API to import the input dataset. This piece
of code allows retrieving data in the same manner, no matter where the
dataset is stored (local filesystem, SQL database, Cloud data lakes,
etc.)

.. code:: ipython3

    dataset_heart_measures = dataiku.Dataset("heart_measures")
    df = dataset_heart_measures.get_dataframe(limit=100000)

2. A quick audit of the dataset
-------------------------------

2.1 Compute the shape of the dataset
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: ipython3

    print(f'The shape of the dataset is {df.shape}')


.. parsed-literal::

    The shape of the dataset is (918, 12)


2.2 Look at a preview of the first rows of the dataset
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: ipython3

    df.head()




.. raw:: html

    
                <button style="display:none" 
                class="btn btn-default ipython-export-btn" 
                id="btn-df-b45ee201-f785-46bb-9113-65b38a82bfb9" 
                onclick="_export_df('b45ee201-f785-46bb-9113-65b38a82bfb9')">
                    Export dataframe
                </button>
    
                <script>
    
                    function _check_export_df_possible(dfid,yes_fn,no_fn) {
                        console.log('Checking dataframe exportability...')
                        if(!IPython || !IPython.notebook || !IPython.notebook.kernel || !IPython.notebook.kernel) {
                            console.log('Export is not possible (IPython kernel is not available)')
                            if(no_fn) {
                                no_fn();
                            }
                        } else {
                            var pythonCode = 'from dataiku.notebook.export import IPythonExporter;IPythonExporter._check_export_stdout("'+dfid+'")';
                            IPython.notebook.kernel.execute(pythonCode,{iopub: {output: function(resp) {
                                console.info("Exportability response", resp);
                                var size = /^([0-9]+)x([0-9]+)$/.exec(resp.content.data || resp.content.text)
                                if(!size) {
                                    console.log('Export is not possible (dataframe is not in-memory anymore)')
                                    if(no_fn) {
                                        no_fn();
                                    }
                                } else {
                                    console.log('Export is possible')
                                    if(yes_fn) {
                                        yes_fn(1*size[1],1*size[2]);
                                    }
                                }
                            }}});
                        }
                    }
    
                    function _export_df(dfid) {
    
                        var btn = $('#btn-df-'+dfid);
                        var btns = $('.ipython-export-btn');
    
                        _check_export_df_possible(dfid,function() {
    
                            window.parent.openExportModalFromIPython('Pandas dataframe',function(data) {
                                btns.prop('disabled',true);
                                btn.text('Exporting...');
                                var command = 'from dataiku.notebook.export import IPythonExporter;IPythonExporter._run_export("'+dfid+'","'+data.exportId+'")';
                                var callback = {iopub:{output: function(resp) {
                                    console.info("CB resp:", resp);
                                    _check_export_df_possible(dfid,function(rows, cols) {
                                        $('#btn-df-'+dfid)
                                            .css('display','inline-block')
                                            .text('Export this dataframe ('+rows+' rows, '+cols+' cols)')
                                            .prop('disabled',false);
                                    },function() {
                                        $('#btn-df-'+dfid).css('display','none');
                                    });
                                }}};
                                IPython.notebook.kernel.execute(command,callback,{silent:false}); // yes, silent now defaults to true. figures.
                            });
    
                        }, function(){
                                alert('Unable to export : the Dataframe object is not loaded in memory');
                                btn.css('display','none');
                        });
    
                    }
    
                    (function(dfid) {
    
                        var retryCount = 10;
    
                        function is_valid_websock(s) {
                            return s && s.readyState==1;
                        }
    
                        function check_conn() {
    
                            if(typeof(IPython) === "undefined" || !IPython || !IPython.notebook) {
                                // Don't even try to go further
                                return;
                            }
    
                            // Check if IPython is ready
                            console.info("Checking conn ...")
                            if(IPython.notebook.kernel
                            && IPython.notebook.kernel
                            && is_valid_websock(IPython.notebook.kernel.ws)
                            ) {
    
                                _check_export_df_possible(dfid,function(rows, cols) {
                                    $('#btn-df-'+dfid).css('display','inline-block');
                                    $('#btn-df-'+dfid).text('Export this dataframe ('+rows+' rows, '+cols+' cols)');
                                });
    
                            } else {
                                console.info("Conditions are not ok", IPython.notebook.kernel);
    
                                // Retry later
    
                                if(retryCount>0) {
                                    setTimeout(check_conn,500);
                                    retryCount--;
                                }
    
                            }
                        };
    
                        setTimeout(check_conn,100);
    
                    })("b45ee201-f785-46bb-9113-65b38a82bfb9");
    
                </script>
    
            <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>Age</th>
          <th>Sex</th>
          <th>ChestPainType</th>
          <th>RestingBP</th>
          <th>Cholesterol</th>
          <th>FastingBS</th>
          <th>RestingECG</th>
          <th>MaxHR</th>
          <th>ExerciseAngina</th>
          <th>Oldpeak</th>
          <th>ST_Slope</th>
          <th>HeartDisease</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>40</td>
          <td>M</td>
          <td>ATA</td>
          <td>140</td>
          <td>289</td>
          <td>0</td>
          <td>Normal</td>
          <td>172</td>
          <td>N</td>
          <td>0.0</td>
          <td>Up</td>
          <td>0</td>
        </tr>
        <tr>
          <th>1</th>
          <td>49</td>
          <td>F</td>
          <td>NAP</td>
          <td>160</td>
          <td>180</td>
          <td>0</td>
          <td>Normal</td>
          <td>156</td>
          <td>N</td>
          <td>1.0</td>
          <td>Flat</td>
          <td>1</td>
        </tr>
        <tr>
          <th>2</th>
          <td>37</td>
          <td>M</td>
          <td>ATA</td>
          <td>130</td>
          <td>283</td>
          <td>0</td>
          <td>ST</td>
          <td>98</td>
          <td>N</td>
          <td>0.0</td>
          <td>Up</td>
          <td>0</td>
        </tr>
        <tr>
          <th>3</th>
          <td>48</td>
          <td>F</td>
          <td>ASY</td>
          <td>138</td>
          <td>214</td>
          <td>0</td>
          <td>Normal</td>
          <td>108</td>
          <td>Y</td>
          <td>1.5</td>
          <td>Flat</td>
          <td>1</td>
        </tr>
        <tr>
          <th>4</th>
          <td>54</td>
          <td>M</td>
          <td>NAP</td>
          <td>150</td>
          <td>195</td>
          <td>0</td>
          <td>Normal</td>
          <td>122</td>
          <td>N</td>
          <td>0.0</td>
          <td>Up</td>
          <td>0</td>
        </tr>
      </tbody>
    </table>
    </div>



2.3 Inspect missing values & number of distinct values (cardinality) for each column
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: ipython3

    pdu.audit(df)




.. raw:: html

    
                <button style="display:none" 
                class="btn btn-default ipython-export-btn" 
                id="btn-df-04e0a739-23bd-48c4-a1e7-4a54ba0f2d60" 
                onclick="_export_df('04e0a739-23bd-48c4-a1e7-4a54ba0f2d60')">
                    Export dataframe
                </button>
    
                <script>
    
                    function _check_export_df_possible(dfid,yes_fn,no_fn) {
                        console.log('Checking dataframe exportability...')
                        if(!IPython || !IPython.notebook || !IPython.notebook.kernel || !IPython.notebook.kernel) {
                            console.log('Export is not possible (IPython kernel is not available)')
                            if(no_fn) {
                                no_fn();
                            }
                        } else {
                            var pythonCode = 'from dataiku.notebook.export import IPythonExporter;IPythonExporter._check_export_stdout("'+dfid+'")';
                            IPython.notebook.kernel.execute(pythonCode,{iopub: {output: function(resp) {
                                console.info("Exportability response", resp);
                                var size = /^([0-9]+)x([0-9]+)$/.exec(resp.content.data || resp.content.text)
                                if(!size) {
                                    console.log('Export is not possible (dataframe is not in-memory anymore)')
                                    if(no_fn) {
                                        no_fn();
                                    }
                                } else {
                                    console.log('Export is possible')
                                    if(yes_fn) {
                                        yes_fn(1*size[1],1*size[2]);
                                    }
                                }
                            }}});
                        }
                    }
    
                    function _export_df(dfid) {
    
                        var btn = $('#btn-df-'+dfid);
                        var btns = $('.ipython-export-btn');
    
                        _check_export_df_possible(dfid,function() {
    
                            window.parent.openExportModalFromIPython('Pandas dataframe',function(data) {
                                btns.prop('disabled',true);
                                btn.text('Exporting...');
                                var command = 'from dataiku.notebook.export import IPythonExporter;IPythonExporter._run_export("'+dfid+'","'+data.exportId+'")';
                                var callback = {iopub:{output: function(resp) {
                                    console.info("CB resp:", resp);
                                    _check_export_df_possible(dfid,function(rows, cols) {
                                        $('#btn-df-'+dfid)
                                            .css('display','inline-block')
                                            .text('Export this dataframe ('+rows+' rows, '+cols+' cols)')
                                            .prop('disabled',false);
                                    },function() {
                                        $('#btn-df-'+dfid).css('display','none');
                                    });
                                }}};
                                IPython.notebook.kernel.execute(command,callback,{silent:false}); // yes, silent now defaults to true. figures.
                            });
    
                        }, function(){
                                alert('Unable to export : the Dataframe object is not loaded in memory');
                                btn.css('display','none');
                        });
    
                    }
    
                    (function(dfid) {
    
                        var retryCount = 10;
    
                        function is_valid_websock(s) {
                            return s && s.readyState==1;
                        }
    
                        function check_conn() {
    
                            if(typeof(IPython) === "undefined" || !IPython || !IPython.notebook) {
                                // Don't even try to go further
                                return;
                            }
    
                            // Check if IPython is ready
                            console.info("Checking conn ...")
                            if(IPython.notebook.kernel
                            && IPython.notebook.kernel
                            && is_valid_websock(IPython.notebook.kernel.ws)
                            ) {
    
                                _check_export_df_possible(dfid,function(rows, cols) {
                                    $('#btn-df-'+dfid).css('display','inline-block');
                                    $('#btn-df-'+dfid).text('Export this dataframe ('+rows+' rows, '+cols+' cols)');
                                });
    
                            } else {
                                console.info("Conditions are not ok", IPython.notebook.kernel);
    
                                // Retry later
    
                                if(retryCount>0) {
                                    setTimeout(check_conn,500);
                                    retryCount--;
                                }
    
                            }
                        };
    
                        setTimeout(check_conn,100);
    
                    })("04e0a739-23bd-48c4-a1e7-4a54ba0f2d60");
    
                </script>
    
            <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>_a_variable</th>
          <th>_b_data_type</th>
          <th>_c_cardinality</th>
          <th>_d_missings</th>
          <th>_e_sample_values</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>Age</td>
          <td>int64</td>
          <td>50</td>
          <td>0</td>
          <td>[40, 49]</td>
        </tr>
        <tr>
          <th>1</th>
          <td>Sex</td>
          <td>object</td>
          <td>2</td>
          <td>0</td>
          <td>[M, F]</td>
        </tr>
        <tr>
          <th>2</th>
          <td>ChestPainType</td>
          <td>object</td>
          <td>4</td>
          <td>0</td>
          <td>[ATA, NAP]</td>
        </tr>
        <tr>
          <th>3</th>
          <td>RestingBP</td>
          <td>int64</td>
          <td>67</td>
          <td>0</td>
          <td>[140, 160]</td>
        </tr>
        <tr>
          <th>4</th>
          <td>Cholesterol</td>
          <td>int64</td>
          <td>222</td>
          <td>0</td>
          <td>[289, 180]</td>
        </tr>
        <tr>
          <th>5</th>
          <td>FastingBS</td>
          <td>int64</td>
          <td>2</td>
          <td>0</td>
          <td>[0, 1]</td>
        </tr>
        <tr>
          <th>6</th>
          <td>RestingECG</td>
          <td>object</td>
          <td>3</td>
          <td>0</td>
          <td>[Normal, ST]</td>
        </tr>
        <tr>
          <th>7</th>
          <td>MaxHR</td>
          <td>int64</td>
          <td>119</td>
          <td>0</td>
          <td>[172, 156]</td>
        </tr>
        <tr>
          <th>8</th>
          <td>ExerciseAngina</td>
          <td>object</td>
          <td>2</td>
          <td>0</td>
          <td>[N, Y]</td>
        </tr>
        <tr>
          <th>9</th>
          <td>Oldpeak</td>
          <td>float64</td>
          <td>53</td>
          <td>0</td>
          <td>[0.0, 1.0]</td>
        </tr>
        <tr>
          <th>10</th>
          <td>ST_Slope</td>
          <td>object</td>
          <td>3</td>
          <td>0</td>
          <td>[Up, Flat]</td>
        </tr>
        <tr>
          <th>11</th>
          <td>HeartDisease</td>
          <td>int64</td>
          <td>2</td>
          <td>0</td>
          <td>[0, 1]</td>
        </tr>
      </tbody>
    </table>
    </div>



3. Exploratory data analysis
----------------------------

3.1 Define categorical & continuous columns
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: ipython3

    categorical_cols = ['Sex','ChestPainType', 'FastingBS', 'RestingECG', 'ExerciseAngina', 'ST_Slope']
    continuous_cols = ['Age', 'RestingBP', 'Cholesterol', 'MaxHR', 'Oldpeak']

3.2 Look at the distibution of continuous features
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: ipython3

    nb_cols=2
    fig = plt.figure(figsize=(8,6))
    fig.suptitle('Distribution of continuous features', fontsize=11)
    gs = fig.add_gridspec(math.ceil(len(continuous_cols)/nb_cols),nb_cols)
    gs.update(wspace=0.3, hspace=0.4)
    for i, col in enumerate(continuous_cols):
        ax = fig.add_subplot(gs[math.floor(i/nb_cols),i%nb_cols])
        sns.histplot(x=df[col], ax=ax)



.. image:: /tutorials/machine-learning/quickstart-tutorial/assets/output_22_0.png


3.3 Look at the distribution of categorical columns
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: ipython3

    nb_cols=2
    fig = plt.figure(figsize=(8,6))
    fig.suptitle('Distribution of categorical features', fontsize=11)
    gs = fig.add_gridspec(math.ceil(len(categorical_cols)/nb_cols),nb_cols)
    gs.update(wspace=0.3, hspace=0.4)
    for i, col in enumerate(categorical_cols):
        ax = fig.add_subplot(gs[math.floor(i/nb_cols),i%nb_cols])
        plot = sns.countplot(x=df[col], palette="colorblind")



.. image:: /tutorials/machine-learning/quickstart-tutorial/assets/output_24_0.png


3.4 Look at the distribution of target variable
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: ipython3

    target = "HeartDisease"
    fig = plt.figure(figsize=(4,2.5))
    fig.suptitle('Distribution of heart disease', fontsize=11, y=1.11)
    plot = sns.countplot(x=df[target], palette="colorblind")



.. image:: /tutorials/machine-learning/quickstart-tutorial/assets/output_26_0.png


*Tip:* To ease collaboration, all the insights you create from Jupyter
Notebooks can be shared with other users by publishing them on
dashboards. See the
`documentation <https://doc.dataiku.com/dss/latest/dashboards/insights/jupyter-notebook.html>`__
for more information.

4. Prepare data
---------------

4.1 Clean categorical columns
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: ipython3

    # Transform string values from categorical columns into int, using the functions from the project libraries
    df_cleaned = data_processing.transform_heart_categorical_measures(df, "ChestPainType", "RestingECG", 
                                                                      "ExerciseAngina", "ST_Slope", "Sex")
    
    df_cleaned.head()




.. raw:: html

    
                <button style="display:none" 
                class="btn btn-default ipython-export-btn" 
                id="btn-df-d757d1ee-7b4c-4c59-934d-a32ea0e550b9" 
                onclick="_export_df('d757d1ee-7b4c-4c59-934d-a32ea0e550b9')">
                    Export dataframe
                </button>
    
                <script>
    
                    function _check_export_df_possible(dfid,yes_fn,no_fn) {
                        console.log('Checking dataframe exportability...')
                        if(!IPython || !IPython.notebook || !IPython.notebook.kernel || !IPython.notebook.kernel) {
                            console.log('Export is not possible (IPython kernel is not available)')
                            if(no_fn) {
                                no_fn();
                            }
                        } else {
                            var pythonCode = 'from dataiku.notebook.export import IPythonExporter;IPythonExporter._check_export_stdout("'+dfid+'")';
                            IPython.notebook.kernel.execute(pythonCode,{iopub: {output: function(resp) {
                                console.info("Exportability response", resp);
                                var size = /^([0-9]+)x([0-9]+)$/.exec(resp.content.data || resp.content.text)
                                if(!size) {
                                    console.log('Export is not possible (dataframe is not in-memory anymore)')
                                    if(no_fn) {
                                        no_fn();
                                    }
                                } else {
                                    console.log('Export is possible')
                                    if(yes_fn) {
                                        yes_fn(1*size[1],1*size[2]);
                                    }
                                }
                            }}});
                        }
                    }
    
                    function _export_df(dfid) {
    
                        var btn = $('#btn-df-'+dfid);
                        var btns = $('.ipython-export-btn');
    
                        _check_export_df_possible(dfid,function() {
    
                            window.parent.openExportModalFromIPython('Pandas dataframe',function(data) {
                                btns.prop('disabled',true);
                                btn.text('Exporting...');
                                var command = 'from dataiku.notebook.export import IPythonExporter;IPythonExporter._run_export("'+dfid+'","'+data.exportId+'")';
                                var callback = {iopub:{output: function(resp) {
                                    console.info("CB resp:", resp);
                                    _check_export_df_possible(dfid,function(rows, cols) {
                                        $('#btn-df-'+dfid)
                                            .css('display','inline-block')
                                            .text('Export this dataframe ('+rows+' rows, '+cols+' cols)')
                                            .prop('disabled',false);
                                    },function() {
                                        $('#btn-df-'+dfid).css('display','none');
                                    });
                                }}};
                                IPython.notebook.kernel.execute(command,callback,{silent:false}); // yes, silent now defaults to true. figures.
                            });
    
                        }, function(){
                                alert('Unable to export : the Dataframe object is not loaded in memory');
                                btn.css('display','none');
                        });
    
                    }
    
                    (function(dfid) {
    
                        var retryCount = 10;
    
                        function is_valid_websock(s) {
                            return s && s.readyState==1;
                        }
    
                        function check_conn() {
    
                            if(typeof(IPython) === "undefined" || !IPython || !IPython.notebook) {
                                // Don't even try to go further
                                return;
                            }
    
                            // Check if IPython is ready
                            console.info("Checking conn ...")
                            if(IPython.notebook.kernel
                            && IPython.notebook.kernel
                            && is_valid_websock(IPython.notebook.kernel.ws)
                            ) {
    
                                _check_export_df_possible(dfid,function(rows, cols) {
                                    $('#btn-df-'+dfid).css('display','inline-block');
                                    $('#btn-df-'+dfid).text('Export this dataframe ('+rows+' rows, '+cols+' cols)');
                                });
    
                            } else {
                                console.info("Conditions are not ok", IPython.notebook.kernel);
    
                                // Retry later
    
                                if(retryCount>0) {
                                    setTimeout(check_conn,500);
                                    retryCount--;
                                }
    
                            }
                        };
    
                        setTimeout(check_conn,100);
    
                    })("d757d1ee-7b4c-4c59-934d-a32ea0e550b9");
    
                </script>
    
            <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }
    
        .dataframe tbody tr th {
            vertical-align: top;
        }
    
        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>Age</th>
          <th>Sex</th>
          <th>ChestPainType</th>
          <th>RestingBP</th>
          <th>Cholesterol</th>
          <th>FastingBS</th>
          <th>RestingECG</th>
          <th>MaxHR</th>
          <th>ExerciseAngina</th>
          <th>Oldpeak</th>
          <th>ST_Slope</th>
          <th>HeartDisease</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>40</td>
          <td>0</td>
          <td>2</td>
          <td>140</td>
          <td>289</td>
          <td>0</td>
          <td>0</td>
          <td>172</td>
          <td>0</td>
          <td>0.0</td>
          <td>2</td>
          <td>0</td>
        </tr>
        <tr>
          <th>1</th>
          <td>49</td>
          <td>1</td>
          <td>3</td>
          <td>160</td>
          <td>180</td>
          <td>0</td>
          <td>0</td>
          <td>156</td>
          <td>0</td>
          <td>1.0</td>
          <td>1</td>
          <td>1</td>
        </tr>
        <tr>
          <th>2</th>
          <td>37</td>
          <td>0</td>
          <td>2</td>
          <td>130</td>
          <td>283</td>
          <td>0</td>
          <td>1</td>
          <td>98</td>
          <td>0</td>
          <td>0.0</td>
          <td>2</td>
          <td>0</td>
        </tr>
        <tr>
          <th>3</th>
          <td>48</td>
          <td>1</td>
          <td>4</td>
          <td>138</td>
          <td>214</td>
          <td>0</td>
          <td>0</td>
          <td>108</td>
          <td>1</td>
          <td>1.5</td>
          <td>1</td>
          <td>1</td>
        </tr>
        <tr>
          <th>4</th>
          <td>54</td>
          <td>0</td>
          <td>3</td>
          <td>150</td>
          <td>195</td>
          <td>0</td>
          <td>0</td>
          <td>122</td>
          <td>0</td>
          <td>0.0</td>
          <td>2</td>
          <td>0</td>
        </tr>
      </tbody>
    </table>
    </div>



4.2 Transform categorical columns into dummies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: ipython3

    df_cleaned = pd.get_dummies(df_cleaned, columns = categorical_cols, drop_first = True)
    
    print("Shape after dummies transformation: " + str(df_cleaned.shape))


.. parsed-literal::

    Shape after dummies transformation: (918, 16)


4.3 Scale continuous columns
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let’s use the Scikit-Learn Robust Scaler to scale continuous features

.. code:: ipython3

    scaler = RobustScaler()
    df_cleaned[continuous_cols] = scaler.fit_transform(df_cleaned[continuous_cols])

5. Split the dataset into train and test
----------------------------------------

Let’s now split the dataset into a train set that will be used for
experimenting and training the Machine Learning models and test set that
will be used to evaluate the deployed model.

.. code:: ipython3

    heart_measures_train_df, heart_measures_test_df = train_test_split(df_cleaned, test_size=0.2, stratify=df_cleaned.HeartDisease)

6. Next: use this notebook to create a new step in the project workflow
-----------------------------------------------------------------------

Now that our notebook is up and running, we can use it to create the
first step of our pipeline in the Flow:

-  Click on the **+ Create Recipe** button at the top right of the
   screen.

-  Select the **Python recipe** option.

-  Choose the ``heart_measures`` dataset as the input dataset and create
   two output datasets: ``heart_measures_train`` and
   ``heart_measures_test``.

-  Click on the **Create recipe** button.

-  At the end of the recipe script, replace the last four rows of code
   with:

.. code:: python

    heart_measures_train = dataiku.Dataset("heart_measures_train")
    heart_measures_train.write_with_schema(heart_measures_train_df)
    heart_measured_test = dataiku.Dataset("heart_measures_test")
    heart_measured_test.write_with_schema(heart_measures_test_df)

-  Run the recipe

Great! We can now go on the Flow, we’ll see an orange circle that
represents your first step (we call it a **Recipe**) and two output
datasets.
