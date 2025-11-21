ERR_RECIPE_SPLIT_INVALID_COMPUTED_COLUMNS: Invalid computed column
##################################################################

There is a computed column on that Split recipe that has a name conflict.
The split recipe need unique names for all input and computed columns,
case-insensitive.

The name conflict can happen:

* between computed columns
* between a computed column and an input column
* between input columns (on a case-sensitive dataset, there might be
  2 columns where case is the only difference)


Remediation
===========

Check the names of the computed columns and input columns,
keeping in mind the case-insensitivity.
