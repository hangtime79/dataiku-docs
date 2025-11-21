Excel
#####################

Dataiku DSS handles Excel spreadsheets saved in XLS and XLSX format, and automatically detects them.

It will also detect which of the sheets in the file might contain data, and on which row the column headers could be.

Sheets selection
=================

You can also manually configure which sheet(s) to include. You can either choose to include:

* **All**: to include all sheets. Useful if the Excel can change over time and include new sheets in the future
* **By name**: to include specific sheets based on their exact names
* **By indices**: to include specific sheets based on their positions. To include multiple sheets separate their indices with commas (ex: ``1,2,4``, ``1,5``), use ranges (ex: ``5-7``, ``2-``, ``-5``) or a mix of both (ex: ``1,2,5-7``).  
* **By pattern**: to include specific sheets whose names match a regular expression pattern (ex: ``[0-9]{4}`` or ``sales-.*``). All sheets where the pattern are found is selected. If you want to ensure that only sheets that perfectly match the pattern are included, use ``^`` and ``$``.

When creating a dataset with multiple sheets, all sheets are expected to have the same schema (same number of columns and same column names)

When uploading an Excel file containing multiple sheets, you can either create a single dataset for multiple sheets or one dataset per sheet. For more advanced capabilities when importing multiple excel sheets, you can checkout the `Excel sheet importer plugin <https://www.dataiku.com/product/plugins/excel-sheet-importer>`_. 

Cells selection by lines
========================

* **Skip first lines**: Dataiku DSS automatically detects the first row of the dataset, but you can also choose to start from a different row. You can also choose to include or exclude a number of rows starting from the first row of the dataset by modifying the "Skip first lines" parameter.

* **Parse next line as column headers**: If selected, Dataiku DSS will use the next line as column names. If not, Dataiku DSS will use the default column names (**0-indexed** e.g. ``col_0``, ``col_1``, etc.).

* **Skip next lines**: Select this if you have a formatted header in your Excel file that you want to exclude from the dataset.

Cells selection by ranges
=========================
Use this mode to import a specific portion of the spreadsheet.

.. caution::
	Switching to "By range" will override the "Skip first lines" and "Skip next lines" options and "Parse next line as column headers".

* **Cell range**: Specify the starting and ending cell references (e.g. ``A1:D10``).

	* **Row only**: Specify a range of rows to import (e.g. ``1:10``). This will import all columns for the specified rows.
	* **Column only**: Specify a range of columns to import (e.g. ``A:D``). This will import all rows for the specified columns.
	* **Cell only**: Specify a specific cell to import (e.g. ``A1``). This will import only the specified cell.
	* **Sheet references**: Specify a specific sheet and range to import from (e.g. ``Sheet1!A1:D10``). You can combine multiple ranges in a single import by separating them with commas (e.g. ``Sheet1!A1:D10,Sheet2!A1:D10``). This allows you to import data from multiple sheets in a single import.

Exporting
==========

Dataiku DSS offers built-in capabilities to export a dataset into an Excel spreadsheet.

If some columns have been configured with conditional formatting "color by rules", DSS allows to color the cells accordingly when exporting the dataset to Excel. Please note that while cells are colored in the exported Excel files, rules themselves are not exported.

To export a dataset into an existing Excel files acting as a template, see :doc:`excel/excel-templater`

.. toctree::

	excel/excel-templater
