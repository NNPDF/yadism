#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import os
import pathlib

here = pathlib.Path(__file__).parent

# -- Project information -----------------------------------------------------

project = "yadism"
copyright = "2019-2024, the NNPDF team"  # pylint: disable=redefined-builtin
author = "NNPDF team"

# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.mathjax",
    "sphinx.ext.ifconfig",
    "sphinx.ext.viewcode",
    # To generate section headings,
    # particularly in markdown. See
    # https://recommonmark.readthedocs.io/en/latest/#linking-to-headings-in-other-files
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.napoleon",
    "sphinx.ext.graphviz",
    "sphinxcontrib.bibtex",
    "sphinxcontrib.details.directive",
    "sphinx_rtd_theme",
    "nbsphinx",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# Markdown configuration

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
source_suffix = {
    ".rst": "restructuredtext",
    ".txt": "markdown",
    ".md": "markdown",
}

autosectionlabel_prefix_document = True
# Allow to embed rst syntax in  markdown files.
enable_eval_rst = True

# The master toctree document.
master_doc = "index"
bibtex_bibfiles = ["refs.bib"]

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["shared/*"]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = None

# A string to be included at the beginning of all files
shared = pathlib.Path(__file__).absolute().parent / "shared"
rst_prolog = "\n".join([open(x).read() for x in os.scandir(shared)])

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

html_logo = "../_assets/logo/logo-docs.png"
html_favicon = "../_assets/logo/logo-favicon-32x32.png"

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
html_theme_options = {
    # "canonical_url": "",
    # "analytics_id": "UA-XXXXXXX-1",  #  Provided by Google in your dashboard
    "logo_only": True,
    "display_version": True,
    # "prev_next_buttons_location": "bottom",
    # "style_external_links": False,
    # "vcs_pageview_mode": "",
    # "style_nav_header_background": "white",
    # # Toc options
    # "collapse_navigation": True,
    # "sticky_navigation": True,
    # "navigation_depth": 4,
    # "includehidden": True,
    # "titles_only": False,
}

html_show_sourcelink = True

# set variables for template system
html_context = {
    # breadcrumbs
    "github_host": "github.com",
    "github_user": "NNPDF",
    "github_repo": "yadism",
    "github_version": "master",
    "conf_py_path": "/docs/sphinx/source/",
    "source_suffix": ".rst",
    "display_github": True,
    # footer:
    "show_copyright": False,
    "show_sphinx": False,
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ["_static"]

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
# html_sidebars = {}

# -- Options for HTML mathjax ------------------------------------------------
mathjax_path = "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"

mathjax_options = {
    "config": "TeX-AMS-MML_HTMLorMML",
    # "integrity": "sha256-QGbnX1xmeSwuEoIuUL3sa4ybs3Egp921kZfRsb87N+Q=",
}

mathjax3_config = {
    "extensions": ["tex2jax.js"],
    "jax": ["input/TeX", "output/HTML-CSS"],
    "loader": {"load": ["[tex]/color", "[tex]/physics"]},
    "tex": {
        "packages": {"[+]": ["base", "color", "physics"]},
    },
}

# -- Options for HTML output -------------------------------------------------

napoleon_google_docstring = False
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = True
napoleon_use_param = True
napoleon_use_rtype = True

# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = "yadismDocumentationdoc"


# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',
    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',
    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',
    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (
        master_doc,
        "yadismDocumentation.tex",
        "yadism Documentation",
        "NNPDF team",
        "manual",
    ),
]


# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (
        master_doc,
        "yadism-documentation",
        "yadism Documentation",
        [author],
        1,
    )
]


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        master_doc,
        "yadismDocumentation",
        "yadism Documentation",
        author,
        "yadismDocumentation",
        "One line description of project.",
        "Miscellaneous",
    ),
]


# -- Options for Epub output -------------------------------------------------

# Bibliographic Dublin Core info.
epub_title = project

# The unique identifier of the text. This can be a ISBN number
# or the project homepage.
#
# epub_identifier = ''

# A unique identification for the text.
#
# epub_uid = ''

# A list of files that should not be packed into the epub file.
epub_exclude_files = ["search.html"]


# -- Extension configuration -------------------------------------------------

# -- Options for autodc extension --------------------------------------------
autodoc_default_options = {
    # "members": "var1, var2",
    # "member-order": "bysource",
    "special-members": True,
    "private-members": True,
    # "inherited-members": True,
    # "undoc-members": True,
    "exclude-members": "__weakref__, __init__, __dict__, __module__"
    ", __abstractmethods__",
}

autoclass_content = "class"

# -- Options for intersphinx extension ---------------------------------------

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "scipy": ("https://docs.scipy.org/doc/scipy", None),
    "numpy": ("https://numpy.org/doc/stable", None),
    "pandas": ("https://pandas.pydata.org/docs/", None),
}


# -- Options for todo extension ----------------------------------------------

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True

# -- Options for edit on github extension ------------------------------------
# https://gist.github.com/mgedmin/6052926
edit_on_github_project = "NNPDF/yadism"
edit_on_github_branch = "master"


# https://github.com/readthedocs/readthedocs.org/issues/1139#issuecomment-312626491
def run_apidoc(_):
    import sys

    from sphinx.ext.apidoc import main

    sys.path.append(str(here.parent))
    # 'yadism'
    docs_dest = here / "modules"
    package = here.parents[1] / "src" / "yadism"
    main(["--module-first", "-o", str(docs_dest), str(package)])
    (docs_dest / "modules.rst").unlink()
    # 'yadmark'
    docs_dest = here / "dev-tools" / "yadmark"
    package = here.parents[1] / "src" / "yadmark"
    main(["--module-first", "-o", str(docs_dest), str(package)])
    (docs_dest / "modules.rst").unlink()
    # 'yadmark'
    docs_dest = here / "ui" / "yadbox"
    package = here.parents[1] / "src" / "yadbox"
    main(["--module-first", "-o", str(docs_dest), str(package)])
    (docs_dest / "modules.rst").unlink()


# Adapted this from
# https://github.com/readthedocs/recommonmark/blob/ddd56e7717e9745f11300059e4268e204138a6b1/docs/conf.py
# app setup hook
def setup(app):
    app.add_config_value(
        "recommonmark_config",
        {
            #'url_resolver': lambda url: github_doc_root + url,
            "enable_eval_rst": True,
        },
        True,
    )
    app.connect("builder-inited", run_apidoc)
