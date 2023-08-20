# Copyright (C) 2019 Dantali0n
# SPDX-License-Identifier: Apache-2.0

import importlib
import pkgutil

from oslo_log import log
from radloggerpy import config

LOG = log.getLogger(__name__)
CONF = config.CONF

"""Collection of methods which detect and import modules for a directory"""


def list_module_names(package_path, excludes=[]):
    """Gather a collection of modules from the specified path with excludes

    :param package_path: Absolute path to 'package' directory.
    :param excludes: Collection of strings excluded if found in package_path
    :return: Collection of modules represented as strings.
    """
    module_names = []
    for __, modname, ispkg in pkgutil.iter_modules(path=[package_path]):
        if modname in excludes or ispkg:
            LOG.debug(
                "Exclude {} in list_module_names from {}".format(modname, package_path)
            )
        else:
            module_names.append(modname)
    return module_names


def import_modules(modules, path, attribute=None, fetch_attribute=False):
    """Import and return modules from a path if they have a given attribute

    :param modules: Collection of modules to import or collection of tuples
                    containing (module, attribute).
    :param path: import path to get modules from
    :param attribute: attribute to filter modules by or None if tuples are used
    :param fetch_attribute: True to create module, attribute tuples, False to
                            only return modules
    :exception AttributeError: When attribute does not exist for a given module
    :exception ImportError: If path + module does not exist
    :return: Collection of imported modules or collection of
             (module, attribute) tuples when fetch_attribute is True.
    """
    imported_modules = []

    # If attribute is not set modules should be collection of tuples
    if not attribute:
        module_filters = modules
    else:
        # Generate a list of tuples were each module_name is associated with
        # the specified attribute.
        module_filters = list()
        for module_name in modules:
            module_filters.append((module_name, attribute))

    for modname, attrib in module_filters:
        mod = importlib.import_module(path + "." + modname)
        if not hasattr(mod, attrib):
            msg = "The module '%s.%s' should have a '%s' " "attribute." % (
                path,
                modname,
                attrib,
            )
            raise AttributeError(msg)
        elif fetch_attribute:
            imported_modules.append((mod, attrib))
        else:
            imported_modules.append(mod)
    return imported_modules
