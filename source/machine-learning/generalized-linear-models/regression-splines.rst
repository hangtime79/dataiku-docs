Regression Splines
###################

Regression splines is a feature engineering technique that allows for defining the relationship between a feature and the response. The recipe computes the spline basis variables that can then be used as features of the model. Regression splines basis variables can be computed through a recipe or as a Prepare step in a Prepare recipe.

Custom Recipe
=================

In the Regression Splines custom recipe, you need to specify:

* The column name on which the splines be computed, it should be a numerical column.
* The eventual knots of the splines, these are the points at which parts of the splines intersect.
* The degree of the polynomial that is used to build the spline.
* The prefix of the new columns that will be created. There will be as many new columns as the sum of number of knots and degrees.

Prepare Step
=================

In the Regression Splines Prepare step, you need to specify:

* The column name on which the splines be computed, it should be a numerical column.
* The degree of the polynomial that is used to build the spline.
* The minimum and maximum values of the column. You must set the lower and upper bounds of the spline. The processing fails if data points fall under the lower bound or over the upper bound.
* The eventual knots of the splines, these are the points at which parts of the splines intersect.

The new columns that will be created have the following format: `<column_name>_Spline_<i>` where `<column_name>` is the input column name you set and `<i>` is the index of the spline basis variable.