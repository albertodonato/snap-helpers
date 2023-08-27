from datetime import datetime
import sys
import os
# Add the directory containing the project tree so that the autodocs extension
# can find the code.
sys.path.insert(0, os.path.abspath(".."))
# Import the base module.
import snaphelpers

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information


project = "snap-helpers"
copyright = "{}, Alberto Donato".format(datetime.today().year)
author = "Alberto Donato"
release = snaphelpers.__version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
    'sphinx_rtd_theme',
]

templates_path = ["_templates"]
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
