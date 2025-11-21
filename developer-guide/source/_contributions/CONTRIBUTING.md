```{eval-rst}
:orphan:
```
# Contributing to the developer guide

This file provides guidelines and instructions on how you can efficiently contribute to Dataiku's Developer Guide.


## Choosing the file type

* You can contribute with content written either in Markdown (`*.md`) or reStructuredText (`*.rst`).
  * You should use [this template](template-md) for Markdown, obtained with [Code 1](contributing_template_md_code), and we provide a [quick reminder syntax](hints-md)
  * You should use [this template](template-rst) for ReStructured Text, obtained with [Code 2](contributing_template_rst_code), and we provide a [quick reminder syntax](hints-rst).

```{literalinclude} template-md.md
:name: contributing_template_md_code
:caption: Code 1 -- template for Mardown
:lines: 5-
```

```{literalinclude} template-rst.rst
:name: contributing_template_rst_code
:caption: Code 2 -- template for ReStructured Text
:lines: 3-
```

## Tutorial outline

All tutorials follow the same structure described below.

### Title

When choosing a **title**, remember that the target audience will look for buzzwords, so don't be shy and use them! 
A good template would look like this:

```
Using {{`cool_tools`}} for {{`fancy_use_case`}}.
```

Examples: 
- Using *Langchain agents* and *vector stores* to *implement a chain-of-thought pattern for sentiment classification*.
- Using *Streamlit* and *custom CSS components* to *deploy a scalable chat-based assistant web app in Kubernetes*.

### Introduction (without an explicit header)

The introduction should be a short paragraph between the title and the prerequisites section, *without a header*. 
Its role is to:

* Explain the functional problem that the user may be facing.
* Say that Dataiku provides a solution with features X/Y/Z.
* Describe how that solution will be implemented while laying out the tutorial outline.

### Prerequisites 

* Dataiku version (preferably the latest supported minor version). If needed, add a disclaimer if the tutorial won't work on Dataiku Cloud.
* Code environment specs:
    * Python version:  default to **3.9** (as of July 2023), don't use <= 3.7.
    * Packages: List only **pinned versions** for each additional package needed:
        - ❌ `torch` or `torch >= 2.0`
        - ✅ `torch` (tested with version `2.0.1`)
    * Resources init script (if needed): add the full code in a dropdown box (closed by default).
* User permissions at the connection and project level
* Project's expected initial state (e.g. with specific datasets, settings, etc.) if it's not empty 
  when starting the tutorial. *You should preferably start all your tutorials with an empty project.*  

### Steps (multiple sections)

Lay out the different steps of your tutorial and separate each "logical piece" into sections.

```{admonition} About getting and preparing the data
:class: caution

* Please double-check that the download links for the starter datasets are valid! Otherwise, it will stop the
  readers dead in their tracks.

* Suppose the data has to be filtered/split/prepared/etc. before getting to the main part of the tutorial, **don't
forget to lay down those steps in detail for the reader!** In particular, avoid vague statements like 
"create a small subset of dataset X" or "clean dataset Y." Instead, explain step-by-step with the relevant code 
how to do all of that to the reader. 

```


### Conclusion

* Wrap up and list a few calls to action for the reader's next steps (e.g., specific parts of the API reference 
  documentation or similar tutorials)
* Please provide a full recap of what was done and complete versions of the code samples to facilitate
    their reuse. The code samples should be in dropdown boxes (closed by default).

## Generic style guide

* All tutorials **must** undergo a Grammarly correction before being submitted for review.
* "You" vs. "we":
  you can use whichever you want but remain consistent (i.e., don't mix them too much)
  and make sure that the reading experience is not altered
  (the reviewer should be careful about that). 
* The tutorial text should be formatted according to the rules
  defined in the 
  [Technical writing style guide](https://docs.google.com/document/d/1ab4IR3QgNrOIUkx1K5NSFBRsoNoLx_fDHyR1UMCQq8s)
  and [UI naming convention deck](https://docs.google.com/presentation/d/1Ti3MYxAqhhNihLmVDQgjTN7bnxZ1Mf-r8Lpt77QWtjo). 
  For any ambiguous case, ask the tech writers for help. 

## File structure

The common file structure for all tutorials is as follows:
```
dss-doc/
|_developer-guide/
  |_tutorials/
  |  |_topic/
  |  |  |_common/
  |  |  |  |_some_image.png
  |  |  |  |_some_code.py
  |  |  |_my_tutorial/
  |  |  |  |_assets/
  |  |  |  |  |_image.png
  |  |  |  |  |_code.py
  |  |  |  |_index.md (or .rst)
  |  |_index.md    
```
or alternatively:
```
dss-doc/
|_developer-guide/
  |_tutorials/
  |  |_topic/
  |  |  |_sub_topic
  |  |  |  |_common/
  |  |  |  |  |_some_image.png
  |  |  |  |  |_some_code.py
  |  |  |  |_my_tutorial/
  |  |  |  |  |_assets/
  |  |  |  |  |  |_image.png
  |  |  |  |  |  |_code.py
  |  |  |  |  |_index.md (or .rst)
  |  |  |_index.md
  |  |_index.md    
```


Where:
* `_topic`: represents the global topic of the tutorial (e.g., `webapps`, `devtools`)
* `_sub_topic`: if needed, the subtopics of the tutorial (e.g., `dash`, `streamlit`)
* `_common`: a directory containing globally shared codes/resources/pages for the topic.
* `_my_tutorial`: the tutorial you are writing.

You must reproduce the same file structure if your tutorial is about a new topic.
Before creating a new topic or subtopic, you must ask the developer advocate teams (`#rd-team-dev-advocacy`).

Remember to add your topic to the corresponding `index` files.
The tutorial should be added to the two related index files if you write for a subtopic.

## Hints and tips for contributing

Here, you will find a quick recap of the different typographies you should use.
This can be found in the additional links provided before.
But for simplicity, we give a small list of frequently asked tips. 

### Font weight
* Use the regular font for referring to a homepage (Design or project) and the "Top navigation bar."
  * E.g., `On the project homepage, click on the **Go to Flow** button`
* Use **bold** font for referring to **Menus** or **Actions**
  * E.g., `In the top navigation bar, choose **More options > Security > Permissions**`
* Use **bold** and ** > ** to indicate a sequence of clicks
  * E.g.: `From the top navigation bar click ** Code > Webapps > +New webapp > Code webapp > Dash > An empty Dash app**`.
    Of course, this example is extreme, and a long path should be avoided as much as possible.

### Component names and capitalization
* The `···` icon in the top navigation bar is  "More options."
* The grid icon on the left of the top navigation bar is called the "Application menu."
* The convention is always using Dataiku and never using DSS in Academy and KB. This comes from product marketing's 
  naming conventions, but we adopt the same wherever possible. Valid exceptions: Dataiku DSS remains in the product UI or API. 
* For capitalization, please refer to [2023-01 Naming Conventions in Dataiku](https://docs.google.com/presentation/d/1irV_U4ODBNPRypLEnyFVSGq4hjv_dnAI6v0tVaRoKqQ), 
  but in a global view, we capitalize product names, services, and solution names.
  We do not capitalize most components, except industry norms (MLOps, API, ...) and unique names within Dataiku
  (Fleet Manage, the Flow, ...)

### References and other technical topics
When you define references or labels, they don't have a "scope" per se (e.g. at the tutorial or category level), instead, they are enforced across the whole developer guide. This is why when naming references/labels you must "namespace" them and make sure they won't collide with identically-named items located elsewhere.

As references change from Markdown to reStructuredText,
you will find a section describing using references in the corresponding template.  

### Code
Code should be typed (if it doesn't obfuscate the code), and keep types as simple as possible.
For non-trivial functions and classes, docstrings are strongly encouraged.

## Before opening your PR for review


* Check your grammar and spelling with Grammarly.
* Check if your prerequisites are relevant and accurate, particularly for the used version.
* Check that your links (internal and external) point to the right place. `make linkcheck` is particularly useful for this.
* If you use numbering, check that the ordering of your figures/code is relevant.
* Make a clean build of the doc (`make clean && make html`), and fix any _new_ warnings that you may have generated.
* If you use images, you should compress them.

```{admonition} Making it easier for the reviewer
:class: Tip

Before even submitting feedback on the tutorial content, the reviewer **must be able to fully reproduce the expected outcome
by starting from scratch**! To avoid unnecessary back-and-forth discussions during the review process, please make sure that
your tutorial is "runnable" before requesting the review.
```
