User-defined meanings
#######################

In addition to the standard meanings, you can define custom meanings in DSS. Examples could include:

* "Customer ID as expressed in the CRM system"
* "Internal department code"
* "Answer to a poll question" (1: strongly agree to 5: strongly disagree, -1: no answer)

Like regular meanings, user-defined meanings can be assigned to several columns. They complement the description on a given column. For example, in a dataset, you could have two columns with "Internal department code" meaning: the initial_department and the current_department columns. Each column could also have a description that indicates when each is filled.

Custom meanings can serve two purposes:

* For documentation. When you set the meaning of a column, DSS shows the details (label and description) everywhere where it's relevant. This way, when you edit a recipe, you have a quick reference available of the meaning of this column.

* For validation. User-defined meanings can optionally define a list of valid values or a pattern. The data exploration screen then displays the usual valid/invalid displays, and you can use the "Remove invalid" processor in data preparation

User defined meanings can be generated from "Meanings" section in the administration dropdown.

Kinds of user-defined meanings
===============================

There are 4 kinds for user-defined meanings

Declarative
------------

No validation is performed for this meaning, and it cannot be automatically detected. This meaning is used for documentation purposes only.

Values list
------------

In this mode, you specify the list of possible values for this meaning. When this meaning is forced, DSS will validate that the value is one of the possible values.

You can specify a normalization mode to indicate whether the match to the possible values should be done exactly, ignoring case, or ignoring accents.

Values mapping
---------------


In this mode, you specify a mapping of possible values for this meaning. For each possible value, a "value in storage" (key) and a "label" are given. When this meaning is forced, DSS will validate that the value is one of the possible values (either in storage or as label).

The main goal of this kind is to handle columns that contain info like "0", "1", "-9" meaning "no", "yes" and "no answer".
The mapping allows you to map these "internal" values to "human-readable" ones.

This kind of user-defined meanings goes with a specific Data preparation processor which handles these replacements.

You can specify a normalization mode to indicate whether the match to the possible keys should be done exactly, ignoring case, or ignoring accents.

Pattern
--------

In this mode, you specify a pattern (as a Java-compatible regular expression) that the values must match. The pattern can be evaluated case-sensitive or case-insensitive.

Autodetecting user-defined meanings
=====================================

User-defined meanings are normally not automatically detected. If you force them, they will be validated, but DSS will never suggest them.

It is possible to auto-detect meanings that are of kind:

* Values list
* Values mapping
* Pattern

.. warning::

	It is not recommended to enable auto-detection. Enabling auto-detection on a user-defined meaning can cause built-in meanings not to be recognized anymore, and can cause notable slowdowns in DSS usage.