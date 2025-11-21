Dynamic recipe repeat
#####################

Any export or download recipe can be configured to be repeating. Such a recipe
takes a secondary "parameters" dataset as a setting and "runs" as many times as
there are rows in the parameters dataset. Each time a repeating recipe runs,
variables are expanded in certain fields of the recipe settings based on the
current row of the parameters dataset.

Export recipe
=============

Variables can be used in the **Filter** and the **File name** sections of the
recipe settings.

Example use case
----------------

There is a dataset containing movies with their corresponding distributors and
the revenues they generated. In order to create dedicated report files per
distributor, each containing only the movies for the given distributor, you can
build a Flow like this:

* Have a dataset
* Create a distinct recipe in order to get unique values which can then be used
  for variable expansion to generate and filter the report
* Create an export recipe, enable the repeating feature picking the output
  dataset of the distinct recipe as the repeating parameters dataset
* The filtering formula could be something like this:
  ::

      val('distributor') == '${distributor}'
* The output file name should also contain the variable to avoid overwriting
  the same file over and over

Download recipe
===============

Variables are expanded in the value used for the **URL** setting of the recipe.

Example use case
----------------

In order to download multiple files based on a dataset containing their partial
URLs, you can build a Flow like this:

* Create an editable dataset containing, for instance, DSS version numbers
* Create a download recipe, enable the repeating feature picking the editable
  dataset as the repeating parameters dataset
* The URL format could be something like this:
  ::

      https://cdn.downloads.dataiku.com/public/dss/${version}/dataiku-dss-${version}.tar.gz

Configuring
===========

To enable a repeating recipe:

* Go to the Advanced tab of the recipe editor
* Within the **Dynamic recipe repeat** section, make sure **Enable** is checked
  and a dataset is selected in the **Parameters dataset** dropdown

Once enabled, you’ll notice a repeat icon on the recipe in the Flow.

By default a variable is created for each column of the parameters dataset
however it is also possible to create a mapping of column names to variable
names. Only the variables specified by the mapping will then be created. This
is useful to avoid variable shadowing.
