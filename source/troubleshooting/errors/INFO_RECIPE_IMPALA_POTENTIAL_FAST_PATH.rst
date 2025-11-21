INFO_RECIPE_IMPALA_POTENTIAL_FAST_PATH: Potential Impala fast path configuration
##################################################################################

The SQL query results are streamed from an input connection through DSS to the output dataset which may be slow.

Remediation
===========

If your recipe is not impacted by the known :ref:`Impala limitations <impala_limitations>`, go to the ``Advanced`` settings
and uncheck the ``Stream mode`` option.