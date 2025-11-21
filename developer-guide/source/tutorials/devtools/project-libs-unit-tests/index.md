# Running unit tests on project libraries 

Dataiku's project libraries allow you to centralize your code and easily call it from various places such as recipes or notebooks. However, as your project's code base grows,
you may want to assess its robustness by *testing* it.

In this tutorial, you will create and run simple unit tests on transformations applied to a dataset. 

## Prerequisites

* Dataiku >= 11.0
* Access to a project with the following permissions:
    * Read project content
    * Run scenarios
* Access to a code environment with the following packages:
    * `pytest==7.2.2`

## Preparing the code and the data

In the Dataiku web interface, create a dataset from the [UCI Bike Sharing dataset](https://archive.ics.uci.edu/ml/machine-learning-databases/00275/Bike-Sharing-Dataset.zip) 
available online. There are two files in the archive to download: use only the `hour.csv` file to create a dataset in Dataiku and name it `BikeSharingData`.

Then, in your project library create a new directory called `bike_sharing` under `lib/python/`, and add two files to it:

* `__init__.py` and leave it empty
* `prepare.py`

The `prepare.py` file will contain the logic of our data transformation packaged into functions. There will be two of them:

* `with_temp_fahrenheit()` will de-normalize the temperature data from the "temp" column and then convert it from Celsius to 
Fahrenheit degrees.

* `with_datetime()`will combine the date and hour data from the "dteday" and "hr" columns into a single "datetime" column in the ISO 8601 format.

Here is the code for those functions:

```{eval-rst}
.. literalinclude:: ./assets/prepare.py
  :language: python
  :caption: prepare.py
```

You can now create a Python recipe taking `BikeSharingData` as input and a new output dataset called `BikeSharingData_prepared`.
In that recipe, apply the transformations previously mentioned using pandas' useful `pipe()` function: 

```{eval-rst}
.. literalinclude:: ./assets/recipe.py
  :language: python
  :caption: recipe.py
```

If you inspect the output dataset, you should see the newly-created columns. 

## Writing the tests

Your Flow is now operational, but what if you wanted to ensure that your code meets expected behavior and errors can be caught earlier
in the development process? To address those issues, you are going to write unit tests for the `with_temp_fahrenheit()` and 
`with_datetime()` functions.

In a nutshell, unit tests are assertions where you verify that atomic parts of your source code operate correctly. In our case,
we'll focus on testing data transformations by submitting sample input values to the function for which we know the outcome, and comparing 
the result of the function with that outcome. 

To run these tests, you will rely on the `pytest` package, a popular testing framework. You'll first need to set it up so that it doesn't
make tests fail because of deprecation warnings, which can sometimes occur but should not be blocking. For that, go back to your project
library and inside the `bike_sharing` tutorial create a new file called `pytest.ini` with the following content: 

```{literalinclude} ./assets/pytest.ini
  :caption: pytest.ini
```

Next, still in the `bike_sharing` directory, create the file containing the code for your tests. Following the pytest conventions, 
it should be prefixed with `test_`, so call it `test_prepare.py`. 

You'll need to define sample data to run our tests on; the easiest way is to define a 1-record pandas DataFrame following the same schema
as the `BikeSharingData` dataset: 

```{literalinclude} ./assets/test_prepare.py 
  :caption: test_prepare.py 
  :lines: 8-26
```

Now let's think a bit about how to test our functions. 

### Temperature conversion

For `with_temp_fahrenheit()`, suppose we start with a normalized temperature of 1.0, which should translate into the upper boundary
set as 39.0 by the [dataset documentation](https://archive.ics.uci.edu/ml/datasets/bike+sharing+dataset). 
The [Celsius-to-Fahrenheit](https://en.wikipedia.org/wiki/Fahrenheit) conversion formula is simple: multiply by 1.8, then add 32.0, so 
39.0 degrees Celsius equal $1.8 \times 39.0 + 32.0 = 102.2$ degrees Fahrenheit. 

In practice, it translates into the following code: 

```{literalinclude} ./assets/test_prepare.py
  :caption: test_prepare.py 
  :lines: 28-31 
```

### Date formatting

For `with_datetime()`, we'll refer to the [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) norm: if the date is `2023-01-01` and the hour
is `13`, then the resulting ISO 8601 date should be `2023-01-01T13:00:00`

Note that the time is assumed to be local to keep thing simple, so there is no time zone designator in the formatted date.

In practice, it translates into the following code: 

```{literalinclude} ./assets/test_prepare.py
  :caption: test_prepare.py 
  :lines: 33-37
```

The entire content of your `test_prepare.py` file should now look like this: 

```{literalinclude} ./assets/test_prepare.py 
  :caption: test_prepare.py 
```

Our tests are now ready! The only thing that is missing is scheduling their execution.

## Running tests 

There are several ways to schedule the execution of your tests, from a purely manual approach to running a full-fledged CI pipeline. In this 
tutorial you will take a simple approach by regrouping the execution of the tests and the build of the `BikeSharingData_prepared` into a Dataiku
scenario. Concretely, that scenario will build the dataset only if all tests pass: this way, you are able to guard against unintended behavior
in your data transformation effectively. 

Go to **Scenario > New Scenario > Sequence of steps**, call your scenario "Test and build" then click on **Create**. Then go to 
**Steps > Add step > Execute Python code**, and in the "Script" field enter the following code: 

```{eval-rst}
.. literalinclude :: ./assets/step.py
  :caption: step.py
  :language: python
```

If you are already familiar with pytest, you probably run your tests directly in a terminal with the `pytest` command. The same
result is achieved here by calling the `pytest.main()` function within your Python code. Note that it requires the absolute path of your 
project library directory to retrieve the test code and configuration files stored here in the `lib_path` variable. 

Don't forget that you will need to run this code with the code environment that contains the pytest package! For that, select it in the 
**Environment** dropdown list. 

The only thing missing now is to build your dataset: go to **Add step > Build/Train**, then click on *Add dataset to build* and 
select `BikeSharingData_prepared`. 

Your scenario is now complete! You can check if it works properly by clicking on **Run**: it will launch a manual run that should 
run successfully. 
If you want to inspect the pytest output, go to **Last runs**, select the desired run then next to "Custom Python" click on "View step log." 

## Wrapping up 

Congratulations, you have written your first unit tests in Dataiku! In this tutorial, you have defined functions and unit tests for 
data processing, embedded them into project libraries then automated the test executions using a scenario. 

You can now extend that logic and write tests to check the data itself,
[this tutorial](../../data-engineering/data-quality-sql/index) has a few examples on how to implement data quality checks.

