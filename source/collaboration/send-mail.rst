Send Emails to a contact list
##############################

Dataiku provides a recipe to send mails to a list of contacts.

.. contents::
	:local:

Overview
==========

From a dataset containing a column of emails addresses, 1 mail per row will be sent. The email is customizable using :ref:`templating-ref`, and can be enriched with data contained within each row in the contacts dataset. It can also include other datasets as CSV or Excel attachments.

.. note::

	This capability is provided by the "Send emails" plugin, which you need to install. Please see :doc:`/plugins/installing`.

	This plugin is :doc:`Not supported </troubleshooting/support-tiers>`


Send Mail recipe settings
=============================

In most settings, you have 2 main choices:

* Getting the value from a column
* Use a custom value directly in the form

**Channel**: 

* Recommended: An existing Dataiku channel configured for sending email
* “Manually define SMTP” to configure a mail server directly

**Sender**

This field does not appear if the channel already has a sender.

* Use a dataset column
* Use a custom value

**Recipient**

The column to use with the email to send to. Addresses can be in the form: ``Name <local@domain.com>`` or just ``local@domain.com``

**Subject**

If you use a custom value, the subject supports templating. You can use column names from the contact dataset, like ``Hello {{ Name }} - Some news about {{ category }}``.


Email Content
===============

Email Body
-------------------

* Use a dataset column
* Use a custom value: in HTML or plain text (:ref:`templating <templating-ref>` is supported in both cases)


Attachments format
-------------------
Choose whether to include the attachment datasets as CSV or Excel files. Each dataset will be included as a separate attachment (be careful about the file size).

**Conditional formatting**: If checked, rules defined on your dataset will also be applied to:

* **HTML email bodies**: Conditional formatting is applied directly to the email content. Leverage directly the JINJA syntax ``{{ attachments.my_dataset.html_table }}``
* **Excel attachments**: The formatting you've set up will be applied to your Excel file attachments


.. _templating-ref:

Templating
============
`JINJA templating <https://jinja.palletsprojects.com/en/3.1.x/>`_ is supported. For the body and the subject, you can use:

* Global or local :ref:`Dataiku variables <variable-ref>`
* Any :ref:`column value <column-ref>`

For the body, you can also insert:

* An attachment as an :ref:`HTML table <html-ref>`
* Any data from an :ref:`attachment <custom-rendering-ref>`

.. _variable-ref:

Dataiku variables
-----------------
The pattern ``${dataiku_variable}`` injects a :doc:`Dataiku variable </variables/index>`, for instance one set at the project level.

.. _column-ref:

Contacts dataset column values
---------------------------------
The pattern ``{{ my_column_name }}`` references a dataset column. Its value for the current row of the contacts dataset will replace it.

.. _html-ref:

Basic HTML table of an attachment dataset
-----------------------------------------
You can inject a dataset as an inline HTML table in the mail body. Only the first 50 rows will be included:
``{{ attachments.my_dataset.html_table }}``

The dataset must be an input dataset of the recipe.
If the dataset has been shared from another project, you must include the project key:
``{{ attachments.other_project_key.my_dataset.html_table }}``. This will include all the columns from that dataset.

The inline HTML table can be customized using CSS.

.. _custom-rendering-ref:

Custom rendering of attachment datasets
---------------------------------------
The full JINJA templating syntax is exposed for the first 50 rows of each attachment dataset using ``attachments.my_dataset.data``

.. code-block:: jinja

   {% for row in attachments.my_dataset.data %}
   <div>{{ row.my_column }}<div>
   {% endfor %}


Output dataset
=================
The output dataset will be a copy of the contacts dataset with two additional columns:

* ``sendmail_status`` - SUCCESS or FAILED, depending on the status
* ``sendmail_error`` - ordinarily empty, but if there is a failure, populated with an error message from the attempt to send the email

