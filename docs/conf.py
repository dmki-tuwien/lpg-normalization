# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# Import the parent directory
import os
import sys
sys.path.insert(0, os.path.abspath('..'))



# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'PG-Norm: Native Property Graph Normal Forms'
copyright = '2026, Johannes Schrott'
author = 'Johannes Schrott'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx_mdinclude',
    'sphinx_paramlinks'
]

autodoc_default_options = {
    # Does now show base classes otherwise... why such bad defaults?
    # But with this it does show useless bases like `object`. What is one to do?
   'show-inheritance': True,
}
autodoc_typehints = "both"
intersphinx_mapping = {'python': ('https://docs.python.org/3.14', None),
                       'neo4j': ('https://neo4j.com/docs/api/python-driver/current/', None)}


templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_book_theme'
html_static_path = ['_static']
html_theme_options = {
    "repository_provider": "github",
    "repository_url": "https://github.com/dmki-tuwien/lpg-normalization",
    "use_repository_button": True,
}

source_suffix = ['.rst', '.md']