Predefined notebooks
#####################

Code notebooks, especially Python and R notebooks are very useful for interactive exploratory analysis, especially for kinds of analysis that are not directly available in DSS visual analysis functionalities.

DSS provides a template mechanism when creating Python or R notebooks. This helps you get started very quickly with an analysis, while still giving you the full freedom to modify the notebook to your own needs, or to go further.

This provides additional interactive analysis capabilities with very little to no code that you have to write.

DSS comes with 8 prebuilt notebooks for analyzing datasets:

* Simple statistical analysis

  * Distribution analysis and statistical tests on a single numerical population
  * Distribution analysis and statistical tests on multiple population groups
  * Correlations between variables

* Dimensionality reduction

  * PCA
  * High-dimensionality data visualization using t-SNE

* Time series

  * Time series visualization and analytics
  * Time series forecasting

* Topics modeling using NMF and LDA

Creating a notebook from a prebuilt template
==============================================

From a dataset's page or in the Flow, in the Actions menu, click on the Lab icon. Choose Notebooks > Predefined and choose the notebook to create.

Read carefully the instructions at the beginning of the notebook. Some notebooks are totally unattended, but for some notebooks, you'll need to setup a few parameters. For example, on the distribution analysis notebook, you need to chose the variable to analyze.

Creating your own prebuilt templates
=====================================

You can create your own notebook templates that you or other users of your DSS instance can reuse. The templates that you create can also be distributed as a plugin.

* Write your notebook in Jupyter (Python or R)
* Download a copy as .ipynb of your notebook
* Create a plugin as explained in :doc:`/plugins/index`
* Click on the "New Component" button and select "Notebook Template"
* Choose the language your notebook is written in and whether you want your template to be accessible
  when creating a notebook from a dataset, or from the "New notebook" button in the notebooks list
* Upon creating the "Notebook Template" component, DSS will take you to a code editor with pre-filled
  notebook content
* Paste the content of your notebook in the editor in place of the pre-filled content
