# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('../_ext'))


# -- Add `dataiku` and `dataikuapi` in sys.path for sphinx.ext.autodoc
#dip_dir = os.environ.get("DKUINSTALLDIR", "")
#if not dip_dir:
#    raise ValueError("DKUINSTALLDIR is not defined")
# -- Add pyspark to import dataiku.spark properly
#spark_dir = os.environ.get("SPARKDIR", "")
#if not spark_dir:
#    raise ValueError("SPARKDIR is not defined")
#sys.path.append(f"{dip_dir}/src/main/python")
#sys.path.append(f"{dip_dir}/lambda/src/main/python")
#sys.path.append(f"{spark_dir}/python")

# -- Project information -----------------------------------------------------

project = 'Developer Guide'
copyright = '2025, Dataiku'
author = 'Dataiku'
html_baseurl = "https://developer.dataiku.com/latest/"
# The full version, including alpha/beta/rc tags
release = '0.1'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "myst_parser",
    "sphinx_design",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinxcontrib.mermaid",
    'sphinxcontrib.jquery',
    "sphinxext.opengraph",
    "sphinx_copybutton",
    "sphinx_reredirects",
    "sphinx_tabs.tabs",
    "sphinx_tippy"
]

intersphinx_mapping = {'refdoc': ('https://doc.dataiku.com/dss/latest/', ('../../build/html/objects.inv', None)),
                       'kb': ('https://knowledge.dataiku.com/latest/', None)}


# Add MyST-specific extensions
myst_enable_extensions = [
    "amsmath",
    "attrs_inline",
    "attrs_block",
    "colon_fence",
    "deflist",
    "dollarmath",
    "fieldlist",
    "html_admonition",
    "html_image",
    "linkify",
    "replacements",
    "smartquotes",
    "strikethrough",
    "substitution",
    "tasklist"]

myst_linkify_fuzzy_links = False
mathjax_path = "https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-AMS-MML_HTMLorMML"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["api-reference/python/hidden_index.rst",
                    "tutorials/machine-learning/others/azure-ml-in-notebook-kb",
                    "tutorials/webapps/bokeh/display-image-kb",
                    "tutorials/genai/nlp/gpt-lc-chroma-rag",
                    "tutorials/data-engineering/pyspark",
                    "tutorials/devtools/shared-code",
                    "tutorials/devtools/code-studio",
                    "tutorials/genai/nlp/byom-few-shot"]

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'furo'
html_title = 'Dataiku Developer Guide'
ogp_site_name = 'Dataiku Developer Guide'
ogp_social_cards = {
    "enable": False
}
ogp_canonical_url = 'https://developer.dataiku.com/latest/'
ogp_site_url = 'https://developer.dataiku.com/latest/'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['../_static']

# Custom CSS files
html_css_files = [
    "css/font-awesome.min.css",
    "css/developer-guide.css",
    "css/learn-menu.css",
    "css/navbar.css",
#    "css/color-gse.css",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['../_templates']

# Use Dataiku favicon (same as refdoc and KB)
html_favicon = "https://www.dataiku.com/static/img/favicon.png"

# Additional options
html_theme_options = {
    # Hide title from the left-side menu
    "sidebar_hide_name": True,
    "navigation_with_keys": True,
}

html_sidebars = {
    "**": [
        "sidebar/scroll-start.html",
        "search.html",
        "sidebar/navigation.html",
        "sidebar/scroll-end.html"
    ]
}


html_js_files = [
    "js/devguide.js",
    "js/opals.js"
]


# -- Sphinx-tabs configuration -----------------------------------------------
sphinx_tabs_disable_tab_closing = True

# -- Sphinx-tippy configuration -----------------------------------------------
tippy_anchor_parent_selector = "div.article-container"

tippy_enable_wikitips = False
tippy_enable_doitips = False
enable_on_the_same_page = False

tippy_skip_anchor_classes = (
    "headerlink",
    "sd-stretched-link"
)

tippy_props = {
    "interactive": True,
    "placement": "top",
    "delay": "[300, 300]"
}

tippy_add_class = "dg-overview"


# -- Options for autodoc output ----------------------------------------------
autodoc_member_order = 'bysource'
#autodoc_member_order = ['alphabetical', 'bysource']
autodoc_default_flags = [ "members", "undoc-members" ]
autodoc_default_options = {"members": None, "undoc-members": None}
# For mocking external required packages
autodoc_mock_imports = ['pyspark', 'langchain', 'langchain_core', 'pydantic', 'snowflake', 'databricks', 'bigframes', 'google']

# -- Options for numfig (not used, as numeration is not correct for now) -----
numfig = False
numfig_format = {'figure': 'Fig. %s: ', 'table': 'Tab. %s: ', 'code-block': 'Code %s: '}

# -- Option for pygment style ------------------------------------------------------------------------------------------
#
# possible options: ['abap', 'algol', 'algol_nu', 'arduino', 'autumn', 'bw', 'borland', 'colorful', 'default',
#                    'dracula', 'emacs', 'friendly_grayscale', 'friendly', 'fruity', 'github-dark', 'gruvbox-dark',
#                    'gruvbox-light', 'igor', 'inkpot', 'lightbulb', 'lilypond', 'lovelace', 'manni', 'material',
#                    'monokai', 'murphy', 'native', 'nord-darker', 'nord', 'one-dark', 'paraiso-dark',
#                    'paraiso-light', 'pastie', 'perldoc', 'rainbow_dash', 'rrt', 'sas', 'solarized-dark',
#                    'solarized-light', 'sphinx', 'staroffice', 'stata-dark', 'stata-light', 'tango', 'trac',
#                    'vim', 'vs', 'xcode', 'zenburn']
#
# For the light mode
# pygments_style = "pastie"
# For the dark mode
# pygments_dark_style

## Redirection of old pages to new ones

redirects = {
    "getting-started/outside-usage": "../tutorials/devtools/python-client/index.html",
    "getting-started/inside-usage":  "../tutorials/devtools/python-client/index.html",
    "getting-started/introduction-python-apis": "../getting-started/dataiku-python-apis/index.html",
    "tutorials/genai/agent/index.html": "../agents-and-tools/agent/index.html",
    "tutorials/genai/image-generation/poster-movies/index": "../../multimodal/images-and-text/images-generation/index.html",
    "tutorials/genai/techniques-and-tools/index": "../agents-and-tools/index.html",
    "tutorials/genai/techniques-and-tools/json-output/index": "../../agents-and-tools/json-output/index.html",
    "tutorials/genai/techniques-and-tools/visual-agent/index": "../../agents-and-tools/visual-agent/index.html",
    "tutorials/genai/techniques-and-tools/agent/index": "../../agents-and-tools/agent/index.html",
    "tutorials/genai/techniques-and-tools/auto-prompt/index": "../../agents-and-tools/auto-prompt/index.html",
    "tutorials/genai/techniques-and-tools/code-agent/index": "../../agents-and-tools/code-agent/index.html",
    "tutorials/genai/techniques-and-tools/llm-agentic/index": "../../agents-and-tools/llm-agentic/index.html",
    "tutorials/genai/techniques-and-tools/llm-agentic/webapps/index": "../../../agents-and-tools/llm-agentic/webapps/index.html",
    "tutorials/genai/techniques-and-tools/llm-agentic/tools/index": "../../../agents-and-tools/llm-agentic/tools/index.html",
    "tutorials/genai/techniques-and-tools/llm-agentic/agents/index": "../../../agents-and-tools/llm-agentic/agents/index.html",
    "getting-started/quickstart-tutorial/index":"../../tutorials/machine-learning/quickstart-tutorial/index.html",
    "getting-started/quickstart-tutorial/step1_data_preparation":"../../tutorials/machine-learning/quickstart-tutorial/step1_data_preparation.html",
    "getting-started/quickstart-tutorial/step2_ml_experiment":"../../tutorials/machine-learning/quickstart-tutorial/step2_ml_experiment.html",
    "getting-started/quickstart-tutorial/step3_ml_deploy_and_eval":"../../tutorials/machine-learning/quickstart-tutorial/step3_ml_deploy_and_eval.html",
    "getting-started/environment-setup/index": "../getting-started/index.html",
}

# This function helps to add redirects for files that were in a renamed folder.
# Once the new redirects defined, you just need to add them in the redirects dict right above.
# An example of usage is given right after the function definition.
def add_redirects_after_renaming(origin_path:str, origin_segment:str, target_segment:str) -> dict:
    """
    Return a dictionnary with new entry for each existing rst or md file in origin_path path.
    From the source path of that file, the redirection will replace origin_segment with target_segment.
    For example:
    - origin_path: "tutorials/genai/techniques-and-tools"
    - origin_segment: "techniques-and-tools"
    - target_segment: "agents-and-tools"
    If there was a file named "tutorials/genai/techniques-and-tools/code-agent/index.rst",
    the redirection returned will be:
    -> {"techniques-and-tools/code-agent/index": "agents-and-tools/code-agent/index.html"}
    """
    # Get the folder of the current executed file to locate the files to process
    current_folder = os.path.dirname(os.path.abspath(__file__))
    # Compose the source path
    source_path = os.path.join(current_folder, origin_path)
    redirects = {}
    # Walk through the source_path directory and its subdirectories
    for dirpath, _, filenames in os.walk(source_path):
        for filename in filenames:
            if filename.endswith((".rst",".md")):
                relative_path = os.path.relpath(os.path.join(dirpath, filename), start=source_path)
                # Remove the file extension
                relative_path = os.path.splitext(relative_path)[0]
                source_redirect = f"{origin_path}/{relative_path}"
                depth = len(relative_path.split('/')) * '../'
                target_redirect = f"{depth}{target_segment}/{relative_path}.html"
                redirects[source_redirect] = target_redirect
    
    return redirects

# Example of usage:
# Let's say you renamed the folder "techniques-and-tools" to "agents-and-tools"
# and you want to add redirects for all the files in "tutorials/genai/techniques-and-tools"
# The function will generate a dictionary with the new redirects.
# You can then copy/paste them from the logs to the redirects dictionary above.

# print(add_redirects_after_renaming(
#         origin_path="tutorials/genai/techniques-and-tools",
#         origin_segment="techniques-and-tools",
#         target_segment="agents-and-tools"
#     )
# )
