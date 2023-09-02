# Copyright (C) 2019 Dantali0n
# SPDX-License-Identifier: Apache-2.0

import os
import sys

from radloggerpy import __version__ as version
from radloggerpy import __package_name__ as package_name
from radloggerpy import __package_folder__ as package_folder

sys.path.insert(0, os.path.abspath('../..'))
# -- General configuration ----------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinxcontrib.apidoc',  # Source code documentation from sphinx docstrings
    "sphinx_rtd_theme",
    'oslo_config.sphinxext',  # Generate config documentation using sample
    'oslo_config.sphinxconfiggen',  # Generate sample config upon docs build
    'cliff.sphinxext'  # Cliff automatic cli documentation
    #'sphinx.ext.intersphinx'
]

config_generator_config_file = [(
    f"../../etc/{package_folder}/{package_folder}-config-generator.conf",
    f"_static/{package_folder}")]
# config_generator_config_file = f"../../etc/{package_folder}/{package_folder}-config-generator.conf"
sample_config_basename = f"_static/{package_folder}"

# Do not ignore cliff autoprogram commands
autoprogram_cliff_ignored = []

apidoc_module_dir = f"../../{package_folder}"
apidoc_output_dir = 'source_documentation'
apidoc_excluded_paths = ['tests', 'hacking']
apidoc_separate_modules = True
apidoc_toc_file = False
# This should include private methods but does not work
# https://github.com/sphinx-contrib/apidoc/issues/14
apidoc_extra_args = ['--private']

# The suffix of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = package_name
copyright = u'2019, Dantali0n'

# openstackdocstheme options
repository_name = f"Dantali0n/{package_folder}"
bug_project = 'none'
bug_tag = ''
html_last_updated_fmt = '%Y-%m-%d %H:%M'

# If true, '()' will be appended to :func: etc. cross-reference text.
add_function_parentheses = True

release = version
version = version

modindex_common_prefix = [f"{package_folder}."]

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
add_module_names = True

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# -- Options for HTML output --------------------------------------------------

# The theme to use for HTML and HTML Help pages.  Major themes that come with
# Sphinx are currently 'default' and 'sphinxdoc'.
# html_theme_path = ["."]
# html_theme = '_theme'
# html_static_path = ['static']
html_theme = "sphinx_rtd_theme"

html_theme_options = {
    "sticky_navigation": True,
    "collapse_navigation": False,
    'includehidden': False,
}

html_static_path = ['static']

html_css_files = [
    'css/custom.css',
]

# Output file base name for HTML help builder.
htmlhelp_basename = '%sdoc' % project

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass
# [howto/manual]).
latex_documents = [
    ('index',
     '%s.tex' % project,
     u'%s Documentation' % project,
     f"{package_name}", 'manual'),
]

# Example configuration for intersphinx: refer to the Python standard library.
#intersphinx_mapping = {'http://docs.python.org/': None}
