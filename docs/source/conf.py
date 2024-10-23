# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information


import os
import sys
import django

# Poner la ruta del proyecto Django
sys.path.insert(0, os.path.abspath('C:/Users/Antonio/Documents/Django-Comercio'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'tienda.settings'
django.setup()

project = 'DjangoComercio'
copyright = '2024, Cabanero11'
author = 'Cabanero11'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = []


# Incluir las extensiones necesarias
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary', 
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'piccolo_theme'
html_static_path = ['_static']
