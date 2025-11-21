```{eval-rst}
:orphan:
```

# Hint for writing tutorials with Markdown syntax

## Comment
In case you need, you can comment a line with
```markdown
% This is a comment.
```

## References

### Internal link
If you need to reference a header/figure/code in your document,
first create a target in your document by using the following:
```markdown
(target)=
#### Header example
```

(target)=
#### Header example

Then reference it with:

| Link                             | Code                                    |
|----------------------------------|-----------------------------------------|
| {ref}`target`                    | ```{ref}`target` ```                    | 
| {ref}`Alternative text <target>` | ```{ref}`Alternative text <target>` ``` |
| [](target)                       | ```[](target) ```                       |
| [Alternative text](target)       | ```[Alternative text](target)```        |

For figures and code, you can also use the configurable options.

### HTML Link

| Link                                             | Code                                                     |
|--------------------------------------------------|----------------------------------------------------------|
| <https://doc.dataiku.com>                        | ``` <https://doc.dataiku.com> ```                        |
| [product documentation](https://doc.dataiku.com) | ``` [product documentation](https://doc.dataiku.com) ``` | 


### Link to an existing doc

| Link                                                  | Code                                                         |
|-------------------------------------------------------|--------------------------------------------------------------|
| {doc}`/getting-started/index`                         | ``` {doc}`/getting-started/index` ```                        |
| {doc}`With alternative text </getting-started/index>` | ```{doc}`With alternative text </getting-started/index>` ``` |

### Link to Refdoc

| Link                                     | Code                                            |
|------------------------------------------|-------------------------------------------------|
| {doc}`refdoc:code_recipes/python`        | ```{doc}`refdoc:code_recipes/python` ```        |
| {doc}`here <refdoc:code_recipes/python>` | ```{doc}`here <refdoc:code_recipes/python>` ``` |

## Figure and Code
If you want to number your figure or code, you need to do it manually.
We do not use automatic numbering as automatic numbering will be for the whole documentation without resetting the numbering by the document.

### Figures
* A simple figure without any configuration is obtained by using the following: ``` ![dku-diagram.png](/getting-started/intro-value/assets/dku-diagram.png){.image-popup} ```

  ![dku-diagram.png](/getting-started/intro-value/assets/dku-diagram.png){.image-popup}

* more advanced figure with configuration options
  ```{figure} /getting-started/intro-value/assets/dku-diagram.png
  :name: contributing_template_md_label
  :width: 100px
    
  Figure 1: Here goes the caption
  ```
  
  This is obtained by using the following:
  ```markdown

        ```{figure} /getting-started/intro-value/assets/dku-diagram.png
        :name: contributing_template_md_label
        :width: 100px
    
        Figure 1: Here goes the caption
        ```

  ```
  then you can refer to the figure by using the `:name:` defined in the figure block, like an internal link.

### Codes

* Inline-code: `example = True`
* Syntax highlighting for long code
  ```python
  import dataiku
  
  client = dataiku.api_client()
  ```
  
  ```markdown

        ```python
        import dataiku
  
        client = dataiku.api_client()
        ```
  ```
* Configurable code block
  ```{code-block} python
  :name: contributing_template_md_code_sample
  :caption: Code 1 -- Code sample
  :linenos:
  :emphasize-lines: 1,3
  
  import dataiku
  
  client = dataiku.api_client()
  ```
  This code sample can be referenced with the internal link reference syntax and is obtained with the following:

  ```markdown
        ```{code-block} python
        :name: contributing_template_md_code_sample
        :caption: Code 1 -- Code sample
        :linenos:
        :emphasize-lines: 1,3
  
        import dataiku
  
        client = dataiku.api_client()
        ```
  ```
* You can also use the `literalinclude` code syntax
  ```markdown
        ```{literalinclude} /tutorials/devtools/project-libs-unit-tests/prepare.py
        :language: python
        :caption: Code 2 -- Included code
        :name: contributing_template_md_code_included
        :emphasize-lines: 1-7
        :linenos:
        ```
  ```
  ```{literalinclude} /tutorials/devtools/project-libs-unit-tests/assets/prepare.py
  :language: python
  :caption: Code 2 -- Included code
  :name: contributing_template_md_code_included
  :emphasize-lines: 1-7
  :linenos:
  ```

* You can also just include a function
  ```{literalinclude} /tutorials/devtools/project-libs-unit-tests/assets/prepare.py
  :language: python
  :caption: Code 3 -- Included code (partial inclusion)
  :name: contributing_template_md_code_included_partial
  :emphasize-lines: 2-12
  :pyobject: with_temp_fahrenheit
  ```
  ```text
          ```{literalinclude} /tutorials/devtools/project-libs-unit-tests/prepare.py
          :language: python
          :caption: Code 3 -- Included code (partial inclusion)
          :name: contributing_template_md_code_included_partial
          :emphasize-lines: 2-12
          :pyobject: with_temp_fahrenheit           
          ```
  ```
## Tables
For simple tables, use the Markdown syntax.

| Link                             | Code                                    |
|----------------------------------|-----------------------------------------|
| {ref}`target`                    | ```{ref}`target` ```                    | 
| {ref}`Alternative text <target>` | ```{ref}`Alternative text <target>` ``` |

is obtained with the following code:
```markdown
| Link                             | Code                                    |
|----------------------------------|-----------------------------------------|
| {ref}`target`                    | ```{ref}`target` ```                    | 
| {ref}`Alternative text <target>` | ```{ref}`Alternative text <target>` ``` |

```

You can right-align a column with `---:` or center with `:---:`.
If you need a more advanced table, you have to fall back to the `rst` syntax:

```{eval-rst}
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
```

```text
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
```

Or with `list-table` (which works also with code)

```{eval-rst}
.. list-table:: Title
  :name: contributing_template_md_table
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

```

```text
.. list-table:: Title
  :name: contributing_template_md_table
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
```

## Admonitions
You can use all admonitions defined in Sphinx
(`topic`, `admonition`, `attention`, `caution`, `danger`, `error`,
`hint`, `important`, `note`, `seealso`, `tip`,  and `warning`).
These admonitions are renderer like the following:

```{topic} topic_title
Lorem ipsum dolor sit amet consectetur adipisicing elit. Accusamus, sunt voluptatum tenetur libero nulla esse
veritatis accusantium earum commodi hic voluptatem officia culpa optio atque. Quaerat sed quibusdam ratione nam. 
```

```{admonition} admonition_title
Lorem ipsum dolor sit amet consectetur adipisicing elit. Accusamus, sunt voluptatum tenetur libero nulla esse
veritatis accusantium earum commodi hic voluptatem officia culpa optio atque. Quaerat sed quibusdam ratione nam. 
```

```{attention}
Lorem ipsum dolor sit amet consectetur adipisicing elit. Accusamus, sunt voluptatum tenetur libero nulla esse
veritatis accusantium earum commodi hic voluptatem officia culpa optio atque. Quaerat sed quibusdam ratione nam. 
```

```{caution}
Lorem ipsum dolor sit amet consectetur adipisicing elit. Accusamus, sunt voluptatum tenetur libero nulla esse
veritatis accusantium earum commodi hic voluptatem officia culpa optio atque. Quaerat sed quibusdam ratione nam. 
```

```{danger}
Lorem ipsum dolor sit amet consectetur adipisicing elit. Accusamus, sunt voluptatum tenetur libero nulla esse
veritatis accusantium earum commodi hic voluptatem officia culpa optio atque. Quaerat sed quibusdam ratione nam. 
```
```{error}
Lorem ipsum dolor sit amet consectetur adipisicing elit. Accusamus, sunt voluptatum tenetur libero nulla esse
veritatis accusantium earum commodi hic voluptatem officia culpa optio atque. Quaerat sed quibusdam ratione nam. 
```
```{hint}
Lorem ipsum dolor sit amet consectetur adipisicing elit. Accusamus, sunt voluptatum tenetur libero nulla esse
veritatis accusantium earum commodi hic voluptatem officia culpa optio atque. Quaerat sed quibusdam ratione nam. 
```
```{important}
Lorem ipsum dolor sit amet consectetur adipisicing elit. Accusamus, sunt voluptatum tenetur libero nulla esse
veritatis accusantium earum commodi hic voluptatem officia culpa optio atque. Quaerat sed quibusdam ratione nam. 
```
```{note}
Lorem ipsum dolor sit amet consectetur adipisicing elit. Accusamus, sunt voluptatum tenetur libero nulla esse
veritatis accusantium earum commodi hic voluptatem officia culpa optio atque. Quaerat sed quibusdam ratione nam. 
```
```{seealso}
Lorem ipsum dolor sit amet consectetur adipisicing elit. Accusamus, sunt voluptatum tenetur libero nulla esse
veritatis accusantium earum commodi hic voluptatem officia culpa optio atque. Quaerat sed quibusdam ratione nam. 
```
```{tip}
Lorem ipsum dolor sit amet consectetur adipisicing elit. Accusamus, sunt voluptatum tenetur libero nulla esse
veritatis accusantium earum commodi hic voluptatem officia culpa optio atque. Quaerat sed quibusdam ratione nam. 
```

```{warning}
Lorem ipsum dolor sit amet consectetur adipisicing elit. Accusamus, sunt voluptatum tenetur libero nulla esse
veritatis accusantium earum commodi hic voluptatem officia culpa optio atque. Quaerat sed quibusdam ratione nam. 
```

## Mathematics and formula

Sphinx uses $\LaTeX$ notation to render the formula.
You can use the `$` sign to delimitate an inline equation.
For example, this inline equation $e=mc^2$ is rendered with ```$e=mc^2$``` or ```{math}`e=mc^2` ```.

You can also have equations block with the `$$` symbol:

$$
\begin{aligned}
  a & = b\\
  a^2 & = ab\\
  a^2 - b^2 & = ab - b^2\\
  (a - b)(a + b) & = b(a - b)\\
\end{aligned}
$$
```text
  $$
  \begin{aligned}
    a & = b\\
    a^2 & = ab\\
    a^2 - b^2 & = ab - b^2\\
    (a - b)(a + b) & = b(a - b)\\
  \end{aligned}
  $$
```

And with the ``` {math} ``` for numbering, see [](contributing_template_md_math_division_by_0) 

```{math}
:label: contributing_template_md_math_division_by_0
\begin{aligned}
  x^2 - x^2 & = x^2 - x^2\\
  x (x - x) & = (x + x) (x - x)\\
\end{aligned}
```
```text
    ```{math}
    :label: contributing_template_md_math_absurd2
    
    \begin{aligned}
      x^2 - x^2 & = x^2 - x^2\\
      x (x - x) & = (x + x) (x - x)\\
    \end{aligned}
    ```
```