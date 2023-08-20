# Copyright 2016 OpenStack Foundation
# Copyright (C) 2023 Dantali0n
# SPDX-License-Identifier: Apache-2.0

"""
This is the single point of entry to generate the sample configuration
file for Watcher. It collects all the necessary info from the other modules
in this package. It is assumed that:

* every other module in this package has a 'list_opts' function which
  return a dict where
  * the keys are strings which are the group names
  * the value of each key is a list of config options for that group
* the watcher.conf package doesn't have further packages with config options
* this module is only used in the context of sample file generation
"""

import os

from radloggerpy.common.dynamic_import import import_modules
from radloggerpy.common.dynamic_import import list_module_names

LIST_OPTS_FUNC_NAME = "list_opts"


def list_opts():
    """Grouped list of all the radloggerpy-specific configuration options

    :return: A list of ``(group, [opt_1, opt_2])`` tuple pairs, where ``group``
             is either a group name as a string or an OptGroup object.
    """
    opts = list()
    package_path = os.path.dirname(os.path.abspath(__file__))
    module_names = list_module_names(package_path, ["opts"])
    imported_modules = import_modules(
        module_names, "radloggerpy.config", LIST_OPTS_FUNC_NAME
    )
    for mod in imported_modules:
        opts.extend(mod.list_opts())
    return opts
