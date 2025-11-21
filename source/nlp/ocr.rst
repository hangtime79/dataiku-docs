OCR (Optical Character recognition)
#####################################


OCR is the process of recognizing, parsing and extracting text from images.

Dataiku leverages two open source OCR engines:

* The `Tesseract library <https://tesseract-ocr.github.io/>`_ to perform OCR in `100 languages <https://tesseract-ocr.github.io/tessdoc/Data-Files/>`_
* The EasyOCR library

It is an offline capability, meaning that it does not leverage a 3rd party API.

.. note::

	This capability is provided by the "Text extraction and OCR" plugin, which you need to install. Please see :doc:`/plugins/installing`.

	This plugin is :doc:`Not supported </troubleshooting/support-tiers>`



Please see our `OCR plugin page <https://www.dataiku.com/product/plugins/tesseract-ocr/>`_ for detailed instructions