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
