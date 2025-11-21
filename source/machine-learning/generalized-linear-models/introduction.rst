Introduction
##############

Generalized Linear Models (GLMs) are a generalization of Ordinary Linear Regression. GLMs allow:

* The response variable to be chosen from any exponential distribution (not only Gaussian).
* The relationship between the linear model and the response variable to be defined by any link function (not only the identity function).

These models provide flexibility in modeling dependencies between regressors and the response variable. GLMs are widely used in the Insurance industry to address specific modeling needs. The GLM implementation uses the `glum` package. Regression Splines rely on `patsy`.

.. contents:: :depth: 1
	:local:

Prerequisites and limitations
===============================

The GLM plugin is available through the plugin store and requires Dataiku V14+. When downloading the plugin, you will be prompted to create a code environment using Python 3.8, 3.9, or 3.10.

To use Generalized Linear Model Regression and Classification algorithms in visual ML, a specific code environment must be selected in the runtime environment. An exception is raised if not. This code environment must include the required visual ML packages and the `glum` package.

.. note::
	If you use the integrated visual GLM interface, you do not need to set up a specific code environment, it will be enforced as the plugin code environment.

How to set up
-------------

1. Create a Python 3.8, 3.9 or 3.10 code environment in **Administration > Code Envs > New Env**.
2. Go to **Packages to install**.
3. Click on **Add set of packages**.
4. Add the Visual Machine Learning packages.
5. Add the `glum` package: `glum==2.6.0`
6. Click on **Save and Update**.
7. Go back to the **Runtime Environment**.
8. Select the environment that has been created.

Once set up, the plugin components listed on the plugin page can be used in your Dataiku projects.