:orphan:

Hint for writing tutorials with ReStructured Text syntax
********************************************************

Every title should be fully underlined.

Comment
#######

In case you need, you can comment on a line or a block with

.. code-block::

    .. This is a comment.

    ..
        This is a
        block comment.


References
##########


Internal link
^^^^^^^^^^^^^

If you need to reference a header/figure/code in your document,
first, create a target in your document by using the following:

.. code-block::

    .. _contributing_template_rst_link:

    Header example
    --------------


.. _contributing_template_rst_link:

Header example
--------------

Then reference it with:

.. list-table::
    :widths: 1 2
    :header-rows: 1

    * - Link
      - Code
    * - :ref:`contributing_template_rst_link`
      - .. code-block::
            :class: no-copybutton

            :ref:`contributing_template_rst_link`
    * - :ref:`Alternative text<contributing_template_rst_link>`
      - .. code-block::
            :class: no-copybutton

            :ref:`Alternative text<contributing_template_rst_link>`

HTML Link
^^^^^^^^^

.. list-table::
    :widths: 1 2
    :header-rows: 1

    * - Link
      - Code
    * - `<https://doc.dataiku.com/>`_
      - .. code-block::
            :class: no-copybutton

            `<https://doc.dataiku.com/>`_
    * - `Product documentation <https://doc.dataiku.com/>`_
      - .. code-block::
            :class: no-copybutton

            `Product documentation <https://doc.dataiku.com/>`_



Link to an existing doc
^^^^^^^^^^^^^^^^^^^^^^^
.. list-table::
    :widths: 1 2
    :header-rows: 1

    * - Link
      - Code
    * - :doc:`/getting-started/index`
      - .. code-block:: none
            :class: no-copybutton

            :doc:`/getting-started/index`

    * - :doc:`With alternative text </getting-started/index>`
      - .. code-block:: none
            :class: no-copybutton

            :doc:`With alternative text </getting-started/index>`


Link to Refdoc
^^^^^^^^^^^^^^

.. list-table::
    :widths: 1 2
    :header-rows: 1

    *   - Link
        - Code
    *   - :doc:`refdoc:code_recipes/python`
        - .. code-block::
            :class: no-copybutton

            :doc:`refdoc:code_recipes/python`

    *   - :doc:`here <refdoc:code_recipes/python>`
        - .. code-block::
            :class: no-copybutton

            :doc:`here <refdoc:code_recipes/python>`


Figure and Code
###############

If you want to number your figure or code, you need to do it manually.
We do not use automatic numbering as automatic numbering will be for the whole documentation without resetting the numbering by the document.

Figures
^^^^^^^

* A simple figure without any configuration is obtained by using the following: ``.. image:: /getting-started/intro-value/assets/dku-diagram.png``

  .. image:: /getting-started/intro-value/assets/dku-diagram.png

* More advanced figure with configuration options

  .. figure:: /getting-started/intro-value/assets/dku-diagram.png
      :name: contributing_template_rst_label
      :width: 100px

      Figure 1: Here goes the caption


  This is obtained by using the following:

  .. code-block:: rst

      .. figure:: /getting-started/intro-value/assets/dku-diagram.png
          :name: contributing_template_rst_label
          :width: 100px

          Figure 1: Here goes the caption


  then you can refer to the figure by using the ``:name:`` defined in the figure block, like an internal link.

Codes
^^^^^


* Inline-code: ``example = True``
* Syntax highlighting for long code

  .. code-block:: python

      import dataiku

      client = dataiku.api_client()

  obtain by using the following:

  .. code-block:: rst

      .. code-block:: python

          import dataiku

          client = dataiku.api_client()

* Configurable code block

  .. code-block:: python
      :name: contributing_template_rst_code_sample
      :caption: Code 1 -- Code sample
      :linenos:
      :emphasize-lines: 1,3

      import dataiku
    
      client = dataiku.api_client()

  This code sample can be referenced with the internal link reference syntax and is obtained with the following:

  .. code-block:: rst

      .. code-block:: python
          :name: contributing_template_rst_code_sample
          :caption: Code 1 -- Code sample
          :linenos:
          :emphasize-lines: 1,3
    
          import dataiku
        
          client = dataiku.api_client()

* You can also use the ``literalinclude`` code syntax

  .. code-block:: rst

      .. literalinclude:: /tutorials/devtools/project-libs-unit-tests/assets/prepare.py
          :language: python
          :caption: Code 2 -- Included code
          :name: contributing_template_rst_code_included
          :emphasize-lines: 1-7
          :linenos:
  
  which provides:

  .. literalinclude:: /tutorials/devtools/project-libs-unit-tests/assets/prepare.py
      :language: python
      :caption: Code 2 -- Included code
      :name: contributing_template_rst_code_included
      :emphasize-lines: 1-7
      :linenos:

* You can also just include a function

  .. literalinclude:: /tutorials/devtools/project-libs-unit-tests/assets/prepare.py
      :language: python
      :caption: Code 3 -- Included code (partial inclusion)
      :name: contributing_template_rst_code_included_partial
      :emphasize-lines: 2-12
      :pyobject: with_temp_fahrenheit

  obtained by using the following:

  .. code-block:: rst

      .. literalinclude:: /tutorials/devtools/project-libs-unit-tests/prepare.py
          :language: python
          :caption: Code 3 -- Included code (partial inclusion)
          :name: contributing_template_rst_code_included_partial
          :emphasize-lines: 2-12
          :pyobject: with_temp_fahrenheit

Tables
######

You can use the ReStructured Text table format, but be very precise when aligning the cells in your editor.

+------------------------+------------+----------+----------+
| Header row, column 1   | Header 2   | Header 3 | Header 4 |
| (header rows optional) |            |          |          |
+========================+============+==========+==========+
| body row 1, column 1   | column 2   | column 3 | column 4 |
+------------------------+------------+----------+----------+
| body row 2             | Cells may span columns.          |
+------------------------+------------+---------------------+
| body row 3             | Cells may  | - Table cells       |
+------------------------+ span rows. | - contain           |
| body row 4             |            | - body elements.    |
+------------------------+------------+----------+----------+
| body row 5             | Cells may also be     |          |
|                        | empty: ``-->``        |          |
+------------------------+-----------------------+----------+

This table is obtained by using the following:

.. code-block:: rst


    +------------------------+------------+----------+----------+
    | Header row, column 1   | Header 2   | Header 3 | Header 4 |
    | (header rows optional) |            |          |          |
    +========================+============+==========+==========+
    | body row 1, column 1   | column 2   | column 3 | column 4 |
    +------------------------+------------+----------+----------+
    | body row 2             | Cells may span columns.          |
    +------------------------+------------+---------------------+
    | body row 3             | Cells may  | - Table cells       |
    +------------------------+ span rows. | - contain           |
    | body row 4             |            | - body elements.    |
    +------------------------+------------+----------+----------+
    | body row 5             | Cells may also be     |          |
    |                        | empty: ``-->``        |          |
    +------------------------+-----------------------+----------+


The ``list-table`` environment is easier to set up, and works also with code

.. list-table:: Title
  :name: contributing_template_rst_table
  :widths: 4 1 3
  :header-rows: 1

  * - Heading row 1, column 1
    - Heading row 1, column 2
    - Heading row 1, column 3
  * - .. code-block:: python

        import dataiku

        client = dataiku.api_client()

    -
    - Row 1, column 3
  * - Row 2, column 1
    - Row 2, column 2
    - Row 2, column 3


.. code-block:: rst

    .. list-table:: Title
      :name: contributing_template_rst_table
      :widths: 4 1 3
      :header-rows: 1

      * - Heading row 1, column 1
        - Heading row 1, column 2
        - Heading row 1, column 3
      * - .. code-block:: python

            import dataiku

            client = dataiku.api_client()

        -
        - Row 1, column 3
      * - Row 2, column 1
        - Row 2, column 2
        - Row 2, column 3

If you want to display a CSV file, you can use the ``csv-table`` environment.

Admonitions
###########
 
You can use all admonitions defined in Sphinx
(``topic``, ``admonition``, ``attention``, ``caution``, ``danger``, ``error``,
``hint``, ``important``, ``note``, ``seealso``, ``tip``,  and ``warning``).

These admonitions are renderer like the following:

.. topic:: topic_title

    Lorem ipsum dolor sit amet consectetur adipisicing elit. Accusamus, sunt voluptatum tenetur libero nulla esse
    veritatis accusantium earum commodi hic voluptatem officia culpa optio atque. Quaerat sed quibusdam ratione nam.

.. admonition:: admonition_title

    Lorem ipsum dolor sit amet consectetur adipisicing elit. Accusamus, sunt voluptatum tenetur libero nulla esse
    veritatis accusantium earum commodi hic voluptatem officia culpa optio atque. Quaerat sed quibusdam ratione nam.

.. attention::
    Lorem ipsum dolor sit amet consectetur adipisicing elit. Accusamus, sunt voluptatum tenetur libero nulla esse
    veritatis accusantium earum commodi hic voluptatem officia culpa optio atque. Quaerat sed quibusdam ratione nam.

.. caution::
    Lorem ipsum dolor sit amet consectetur adipisicing elit. Accusamus, sunt voluptatum tenetur libero nulla esse
    veritatis accusantium earum commodi hic voluptatem officia culpa optio atque. Quaerat sed quibusdam ratione nam.


.. danger::
    Lorem ipsum dolor sit amet consectetur adipisicing elit. Accusamus, sunt voluptatum tenetur libero nulla esse
    veritatis accusantium earum commodi hic voluptatem officia culpa optio atque. Quaerat sed quibusdam ratione nam.

.. error::
    Lorem ipsum dolor sit amet consectetur adipisicing elit. Accusamus, sunt voluptatum tenetur libero nulla esse
    veritatis accusantium earum commodi hic voluptatem officia culpa optio atque. Quaerat sed quibusdam ratione nam.

.. hint::
    Lorem ipsum dolor sit amet consectetur adipisicing elit. Accusamus, sunt voluptatum tenetur libero nulla esse
    veritatis accusantium earum commodi hic voluptatem officia culpa optio atque. Quaerat sed quibusdam ratione nam.

.. important::
    Lorem ipsum dolor sit amet consectetur adipisicing elit. Accusamus, sunt voluptatum tenetur libero nulla esse
    veritatis accusantium earum commodi hic voluptatem officia culpa optio atque. Quaerat sed quibusdam ratione nam.

.. note::
    Lorem ipsum dolor sit amet consectetur adipisicing elit. Accusamus, sunt voluptatum tenetur libero nulla esse
    veritatis accusantium earum commodi hic voluptatem officia culpa optio atque. Quaerat sed quibusdam ratione nam.

.. seealso::
    Lorem ipsum dolor sit amet consectetur adipisicing elit. Accusamus, sunt voluptatum tenetur libero nulla esse
    veritatis accusantium earum commodi hic voluptatem officia culpa optio atque. Quaerat sed quibusdam ratione nam.

.. tip::
    Lorem ipsum dolor sit amet consectetur adipisicing elit. Accusamus, sunt voluptatum tenetur libero nulla esse
    veritatis accusantium earum commodi hic voluptatem officia culpa optio atque. Quaerat sed quibusdam ratione nam.

.. warning::
    Lorem ipsum dolor sit amet consectetur adipisicing elit. Accusamus, sunt voluptatum tenetur libero nulla esse
    veritatis accusantium earum commodi hic voluptatem officia culpa optio atque. Quaerat sed quibusdam ratione nam.

And there all obtain with the same schema:

.. code-block:: rst

    .. admonition_type:: admonition_title (for topic and admonition only)

        Lorem ipsum dolor sit amet consectetur adipisicing elit. Accusamus, sunt voluptatum tenetur libero nulla esse
        veritatis accusantium earum commodi hic voluptatem officia culpa optio atque. Quaerat sed quibusdam ratione nam.


Mathematics and formula
#######################


Sphinx uses :math:`\LaTeX` notation to render the formula.

For example, this inline equation :math:`e=mc^2` is rendered with ``:math:`e=mc^2```.

You can also have an equation block:

.. math::

    \begin{aligned}
      a              & = b\\
      a^2            & = ab\\
      a^2 - b^2      & = ab - b^2\\
      (a - b)(a + b) & = b(a - b)\\
    \end{aligned}

Obtained by using the following:

.. code-block:: rst

    .. math::

        \begin{aligned}
          a              & = b\\
          a^2            & = ab\\
          a^2 - b^2      & = ab - b^2\\
          (a - b)(a + b) & = b(a - b)\\
        \end{aligned}

And if you use a ``:label:``, the equation will be numbered, and can be referenced
with ``:eq:`contributing_template_rst_math_division_by_0``` which is rendered like this:
:eq:`contributing_template_rst_math_division_by_0`. You can not use alternative text.

.. math::
    :label: contributing_template_rst_math_division_by_0

    \begin{aligned}
      x^2 - x^2 & = x^2 - x^2\\
      x (x - x) & = (x + x) (x - x)\\
    \end{aligned}

Numbering is obtained by using the following:

.. code-block:: rst

    .. math::
        :label: contributing_template_rst_math_division_by_0

        \begin{aligned}
          x^2 - x^2 & = x^2 - x^2\\
          x (x - x) & = (x + x) (x - x)\\
        \end{aligned}
