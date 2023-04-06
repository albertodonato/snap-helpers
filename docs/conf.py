# -*- coding: utf-8 -*-
#
# snap-helpers documentation build configuration file.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#

from datetime import datetime
import os
import sys

# Add the directory containing the project tree so that the autodocs extension
# can find the code.
sys.path.insert(0, os.path.abspath(".."))
# Import the base module.
import snaphelpers

# -- General configuration ------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix of source filenames.
source_suffix = ".rst"

# The master toctree document.
master_doc = "index"

# General information about the project.
project = "snap-helpers"
copyright = "{}, Alberto Donato".format(datetime.today().year)

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
release = str(snaphelpers.__version__)
# The full version, including alpha/beta/rc tags.
version = release

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#  today = ''
# Else, today_fmt is used as the format for a strftime call.
#  today_fmt = '%B %d, %Y'

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.
html_theme = "default"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
# html_use_opensearch = ''

# Output file base name for HTML help builder.
htmlhelp_basename = "snaphelpersdoc"


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    ('index', 'snaphelpers', 'snap-helpers Documentation', ['Alberto Donato'], 1)
]

# If true, show URL addresses after external links.
#  man_show_urls = False

napoleon_use_param = True
