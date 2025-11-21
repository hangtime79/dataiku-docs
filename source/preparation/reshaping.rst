Reshaping
##########

Reshaping processors are used to change the « shape » (rows/columns) of the data.

DSS provides the following reshaping processors

.. contents::
	:local:

Split and Fold
================

The :doc:`processors/split-fold` processor creates new lines by splitting the values of a column.

.. include:: processors/snippets/_split-fold-example.rst

More details are available in the :doc:`reference <processors/split-fold>`


.. _fold-multiple-label:

Fold multiple columns
=======================

The :doc:`processors/fold-columns-by-name` processor takes values from multiple columns and transforms them to one line per column.

.. include:: processors/snippets/_fold-columns-by-name-example.rst

More details are available in the :doc:`reference <processors/fold-columns-by-name>`


Fold multiple columns by pattern
================================

This processor is a variant of :ref:`fold-multiple-label`, where the columns to fold are specified by a pattern instead of a list. The processor only creates lines for non-empty columns.

.. include:: processors/snippets/_fold-columns-by-pattern-example.rst

More details are available in the :doc:`reference <processors/fold-columns-by-pattern>`


Unfold
=========

This processor transforms cell values into binary columns.

.. include:: processors/snippets/_unfold-example-and-warning.rst

More details are available in the :doc:`reference <processors/unfold>`


Unfold an array
===============

This processor transforms array values into occurrence columns.

.. include:: processors/snippets/_unfold-array-example-and-warning.rst

More details are available in the :doc:`reference <processors/unfold-array>`


Split and Unfold
=================

This processor splits multiple values in a cell and transforms them into columns.

.. include:: processors/snippets/_split-unfold-example-and-warning.rst

More details are available in the :doc:`reference <processors/split-unfold>`

Triggered Unfold
================

This processor is used to reassemble several rows when a specific value is encountered. It is useful for analysis of "interaction sessions" (a series of events with a specific event marking the beginning of a new interaction session). For example, while analyzing the logs of a web game, the "start game" event would be the beginning event.


More details are available in the :doc:`reference <processors/triggered-unfold>`
