# -*- encoding: utf-8 -*-
# Copyright (c) 2019 Dantali0n
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import importlib
import os
import pkgutil

from radloggerpy.database.declarative_base import base

# relative directory for models from this file
models_rel_directory = '/models'

# absolute path to models for imports
model_absolute_path = 'radloggerpy.database.models.'


def create_database_tables(engine):
    """Creates the database table using the specified engine"""
    tables = _list_tables()
    base.metadata.create_all(bind=engine, tables=tables)


def _list_tables():
    """Collection of all the sqlalchemy model __table__ objects

    :return: A Collection of ``__table__`` objects from sqlalchemy models.
    """
    tables = list()
    model_names = _list_model_names()
    imported_modules = _import_models(model_names)
    for module in imported_modules:
        # Access the modules class and subsequent __table__
        tables.append(getattr(module[0], module[1]).__table__)
    return tables


def _list_model_names():
    """Gather collection of model names from models modules

    :return: A collection of module names iterated from the models directory
    """
    model_names = []

    # import everything from models directory relative to this file
    package_path = os.path.dirname(
        os.path.abspath(__file__)) + models_rel_directory

    # iterate over all module files and append their names to the list
    for __, modname, ispkg in pkgutil.iter_modules(path=[package_path]):
        model_names.append(modname)
    return model_names


def _import_models(module_names):
    """Gather collection of tuples with modules and associated classes

    :return: A collection of tuples with the module and its associated class
    """
    imported_modules = []

    # for every module names import it and check that it has a class similar
    # to the name of the module. Example: if the file is named account it will
    # look for the Account class. If the file is called account_types it will
    # look for the AccountTypes class.
    for modname in module_names:
        # Capitalize first letters and subsequently remove all underscores.
        class_name = modname.title().replace('_', '')
        mod = importlib.import_module(model_absolute_path + modname)
        if not hasattr(mod, class_name):
            msg = "The module '" + model_absolute_path + ".%s' should have a" \
                  "'%s' class similar to the module name." % \
                  (modname, class_name)
            raise AttributeError(msg)
        else:
            imported_modules.append((mod, class_name))
    return imported_modules
