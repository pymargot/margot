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

import recommonmark
from recommonmark.transform import AutoStructify
from recommonmark.parser import CommonMarkParser

import margot

# before pulling hair out, see: https://pypi.org/project/sphinxcontrib-apidoc/
# and also: https://samnicholls.net/2016/06/15/how-to-sphinx-readthedocs/
sys.path.insert(0, os.path.abspath('..'))



# -- Project information -----------------------------------------------------

project = 'margot'
copyright = '2020, Rich Atkinson'
author = 'Rich Atkinson'

# The full version, including alpha/beta/rc tags
release = margot.__version__
version = margot.__version__

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'nbsphinx',
    'recommonmark',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', '**/migrations', '.vscode', 'data']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

autoclass_content = "both"
master_doc = 'index'
autodoc_member_order = 'bysource'


# Markdown support -----------------------------------------------------------

github_doc_root = 'https://github.com/atkinson/margot/tree/master/docs'

def setup(app):
    app.add_config_value('recommonmark_config', {
            'url_resolver': lambda url: github_doc_root + url,
            'auto_toc_tree_section': 'Contents',
            'enable_eval_rst': True,
            }, True)
    app.add_transform(AutoStructify)