# Copyright (C) 2019 Dantali0n
# SPDX-License-Identifier: Apache-2.0


from radloggerpy.common.dynamic_import import import_modules
from radloggerpy.common.dynamic_import import list_module_names
from radloggerpy.database.declarative_base import base
from radloggerpy.database import models


def create_database_tables(engine):
    """Creates the database table using the specified engine"""
    tables = _list_tables()
    base.metadata.create_all(bind=engine, tables=tables)


def _list_tables():
    """Collection of all the sqlalchemy model __table__ objects

    :return: A Collection of ``__table__`` objects from sqlalchemy models.
    """
    tables = list()

    modules = list()
    # create module_name and expected class tuples from list_module_names
    # if the module file is account_types the expected class is AccountTypes.
    for module_name in list_module_names(models.__path__[0]):
        modules.append((module_name, module_name.title().replace("_", "")))

    imported_modules = import_modules(modules, models.__name__, fetch_attribute=True)
    for module, attribute in imported_modules:
        # Access the modules class and subsequent __table__
        tables.append(getattr(module, attribute).__table__)
    return tables
