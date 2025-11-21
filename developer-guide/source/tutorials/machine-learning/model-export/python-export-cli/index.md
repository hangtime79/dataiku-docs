# Wrapping an exported model in a CLI tool 

## Prerequisites

* Dataiku >= 11.1.0 
* A Project in which you already deployed a Saved Model version trained on the [Bank Marketing Dataset](https://archive.ics.uci.edu/ml/datasets/bank+marketing)

## Introduction

The Python export feature packages a Saved Model version into a reusable artifact requiring only Python when used outside of Dataiku. It covers use-cases where you may not be able to deploy the model as an [API service endpoint](https://doc.dataiku.com/dss/latest/apinode/introduction.html#exposing-predictive-models) or if you don't need the overhead of using HTTP to request predictions.

In this tutorial you will see how an exported model can be packaged into a simple command-line interface (CLI) to score data stored in CSV files. 

## Dataset and model

This tutorial is based on a model trained on the [Bank Marketing Dataset](https://archive.ics.uci.edu/ml/datasets/bank+marketing) to predict whether a given client will subscribe a term deposit. According to the prerequisites, you should already have it available in your Flow as a Saved Model version. 

Following the [steps described in the documentation](https://doc.dataiku.com/dss/latest/machine-learning/models-export.html#export-to-python), export the Saved Model version as a Python function. After this step you should have downloaded a zip archive. 

Unzip the archive, you should get the following files: 

* `model.zip`: the actual trained model artifact,
* `sample.py`: a starter code sample with a simple example to score a few data points,
* `requirements.txt`: a list of packages to install before running the scoring code.

In `sample.py`, the provided code assumes that the input data points are already available as plain list of Python dictionaries, but it would be even more convenient to handle input files directly and execute *batch scoring*. That is precisely what you will implement in the next section.

## Implementing the CLI 

In this section you will create an additional script called `score.py` that takes a CSV file and an exported model as inputs and produces an enriched output file with the prediction results. The script will essentially be a CLI tool that shall accept 4 arguments:

* the path to the input file,
* the path to the exported model to use for scoring,
* the desired path for the generated output file,
* an optional flag to generate the predicted probabilities for each class.

In the rest of the tutorial you will use the export directory as main working directory. 

Start by creating a new Python virtual environment and install the dependencies listed in the `requirements.txt` file.

```bash
python -m venv scoring-env
source scoring-env/bin/activate
pip install -r requirements.txt
```
Install additional packages needed to run the script:

* [*pandas*](https://pandas.pydata.org/) to apply the scoring operation on an entire DataFrame
* [*click*](https://click.palletsprojects.com/) to parse arguments passed to the CLI

```bash

pip install click pandas

```

Once your dependencies are ready, create a new file called `score.py` with the following code: 

```{literalinclude} score.py

```

Let's look closer at this code! First, you can see that the `score()` function is decorated with multiple `@click.option` decorators: this is how the `click` package lists the different options and arguments passed to the command line. Each option has:

* a name, both in short and long form (e.g. `-i` and `--input-file`) that will serve as identifier when parsing the command sent by the user,
* a type, essentially to help with error handling: for example, `click.Path(exists=True)` will explicitly tell the user if the target file doesn't exist on the specified path,
* a helper text, to provide a concise description of the argument when calling the CLI with the `--help` flag.

Based on the options, the code creates a pandas DataFrame from the input file, either generating a prediction or the class probabilities, and then writes the result on an output file.

```{note}

Several assumptions have been made to simplify the code, in particular there is no specific handling of CSV parsing options like custom delimiters, quoting or headers. However, using `sep=None` and `engine='python'` in `pd.read_csv()` forces pandas to infer the delimiter and thus prevents the users of having to explicitly declare one.
```

You can now call your CLI as follows: 

```bash

# Output predictions
python score.py -i my_input.csv -o my_output.csv -m model.zip 

# Output probabilities
python score.py -i my_input.csv -o my_output.csv -m model.zip --proba
```

To get help and details about the available options, use the `--help` flag. 

```bash
python score.py --help 

#Usage: scoring.py [OPTIONS]
#
#  Scoring CLI: computes predictions from CSV file records using a trained
#  model exported from Dataiku.

#Options:
#  -i, --input-file PATH       Path to tne input file
#  -o, --output-file FILENAME  Path to the generated output file
#  -m, --model-file PATH       Path to the model to use for predictions
#  --proba                     Add predicted proba column for each class
#  --help                      Show this message and exit.

```

## Wrapping up


From this simple starting point you can now swap the Bank Marketing model export with your very own use-case. There are also a few ways to expand the capabilities of your CLI, e.g. by:

* providing a list of input CSV files or an input folder to score multiple files in one go,
* implementing an "evaluation mode": if the input CSV file contains the ground truth, you can use it to evaluate the model's performance metrics after computing the predictions,
* leveraging Dataiku's public API to programmatically export the latest model version before running the prediction.

For more details on the export capabilities of Dataiku, you can read the corresponding section of the [reference documentation](https://doc.dataiku.com/dss/latest/machine-learning/models-export.html).
