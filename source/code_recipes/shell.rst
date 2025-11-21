Shell recipes
#############

.. contents::
	:local:


In order to automate certain operations, DSS provides a "Shell" recipe which executes a script in the shell.

Parameters to the script
========================

No parameter to the script can be passed on the command line, but DSS sets up a handful of environment variables prior to running the script:

* Usual flow variables : input and output partitioning info :doc:`/partitions/variables`
* for each input and output dataset : identifier, and when relevant, filesystem path or jdbc url. Variables named ``DKU_INPUT...`` and ``DKU_OUTPUT...`` correspond to the inputs and outputs respectively. The (zero-based) index of the input or output in the list of inputs or outputs to the recipe is passed in the environment variable name. For example, ``DKU_INPUT_1_DATASET_ID`` will contain the identifier of the second input to the recipe

The list of all variables given by DSS to the script is accessible in the "Variables" tab next to the script pane.


Piping a dataset in and out
===========================

DSS allows for one of the input datasets to be piped in the script, via the standard input. This dataset can be selected in the dropdown over the code pane. The data is sent as tab-separated CSV.

Likewise, DSS allows for the standard output of the script to be piped out into one output dataset, again selected with the dropdown over the code pane.
This functionality can be used for example to report information in the script and have this information stored in a dataset in DSS.
The data is expected as tab-separated CSV.
When "auto-infer schema" is checked,
the schema of the piped out dataset will be overwritten with columns inferred from the first line of the script output.


Executed binary
===============

By default, the script is run on the standard ``sh`` binary. A different binary can be set on the "Advanced" tab, or using a shebang.


Examples
========

* Simple shell recipe that contains an input dataset. This recipe will run the equivalent of the command ``grep -i pattern {input dataset}`` 

  .. code-block:: bash 

        grep -i pattern
    
* Shell script recipe that uses a variable ``date_variable`` with the value ``2017/01/01`` and an input dataset. This will run the equivalent of the command ``grep pattern {input dataset} | grep 2017/01/01``. 

  .. code-block:: bash 

      grep pattern | grep $DKU_CUSTOM_VARIABLES_date_variable

  Note that available variables can be found in the lefthand panel beside the recipe. 


* Shell script recipe that executes an external command:

  .. code-block:: bash 

      sh /home/dataiku/shell-script.sh
