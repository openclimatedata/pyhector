# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__), "../pyhector"))
from _version import get_versions  # isort:skip # append path before


# -- Project information -----------------------------------------------------

project = "pyhector"
copyright = "2017, Sven Willner, Robert Gieseke"
author = "Sven Willner, Robert Gieseke"
version = get_versions()["version"]  # The short X.Y version
release = version  # The full version, including alpha/beta/rc tags


# -- General configuration ---------------------------------------------------

exclude_patterns = ["build", "Thumbs.db", ".DS_Store"]
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.coverage",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
]
language = "en"
master_doc = "index"
needs_sphinx = "1.8"
pygments_style = "sphinx"
source_suffix = ".rst"  # ['.rst', '.md']
templates_path = ["templates"]


def skip_init(app, what, name, obj, skip, options):
    if name == "__init__":
        return False
    return skip


def setup(app):
    app.connect("autodoc-skip-member", skip_init)


# -- Options for HTML output -------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_static_path = ["static"]
html_context = {
    "display_github": False,
    "github_user": "openclimatedata",
    "github_repo": "pyhector",
    "github_version": "master",
    "conf_py_path": "/docs/",
}


# -- Options for HTMLHelp output ---------------------------------------------

htmlhelp_basename = "pyhectordoc"


# -- Options for LaTeX output ------------------------------------------------

latex_elements = {}
# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (
        master_doc,
        "pyhector.tex",
        "pyhector Documentation",
        "Sven Willner, Robert Gieseke",
        "manual",
    )
]


# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [(master_doc, "pyhector", "pyhector Documentation", [author], 1)]


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        master_doc,
        "pyhector",
        "pyhector Documentation",
        author,
        "pyhector",
        "Python interface for the simple global climate carbon-cycle model Hector.",
        "Miscellaneous",
    )
]


# -- Extension configuration -------------------------------------------------

autodoc_default_options = {
    "inherited-members": None,
    "members": None,
    "private-members": None,
    "show-inheritance": None,
    "undoc-members": None,
}
coverage_write_headline = False  # do not write headlines.
intersphinx_mapping = {
    "numpy": ("https://docs.scipy.org/doc/numpy", None),
    "python": ("https://docs.python.org/3", None),
}
napoleon_google_docstring = False
napoleon_numpy_docstring = True
