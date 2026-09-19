import os
import sys

sys.path.insert(0, os.path.abspath("../../src"))

project = 'Khers Engine'
copyright = '2026, hojat72elect'
author = 'hojat72elect'
release = '0.1.1'

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]

templates_path = ['_templates']
exclude_patterns = []

html_theme = 'alabaster'
html_static_path = ['_static']
