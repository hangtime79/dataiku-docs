Text extraction
################

Dataiku can extract text from several document types:

* PDF
* DOCX
* HTML
* Metadata

The Text extraction recipe takes as input a folder of various file types (pdf, docx, html, etc) and outputs a dataset with three columns: filename, extracted text and error messages when it failed to extract any text.

For some input formats, it is possible to extract text in chunks, with an extra metadata column containing section info. This will output one row by unit of document. A unit can be a page in a PDF file or a section in a DOCX, HTML, Markdown, etc. These metadata can either be in plain text or JSON format.


.. note::

	This capability is provided by the "Text extraction and OCR" plugin, which you need to install. Please see :doc:`/plugins/installing`.

	This plugin is :doc:`Not supported </troubleshooting/support-tiers>`



Please see our `OCR plugin page <https://www.dataiku.com/product/plugins/tesseract-ocr/>`_ for detailed instructions