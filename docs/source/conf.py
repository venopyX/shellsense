"""
Configuration file for the Sphinx documentation builder.
"""

import os
import sys
sys.path.insert(0, os.path.abspath('../..'))

# Project information
project = 'ShellSense'
copyright = '2024, venopyx'
author = 'venopyx'
version = '1.0'
release = '1.0'

# General configuration
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
]

templates_path = ['_templates']
exclude_patterns = []

# HTML output options
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# Intersphinx configuration
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
}
