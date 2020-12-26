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

import os.path

from oslo_log import log
from radloggerpy import config

import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_utils import database_exists

from radloggerpy._i18n import _
from radloggerpy.database import create_database as cd

LOG = log.getLogger(__name__)
CONF = config.CONF

"""
Ensure all models their tables and relationships are loaded before sessions
are created. Otherwise SQLAlchemy will have troubling finding
unimported relationshios.
"""
RUNTIME_TABLES = cd._list_tables()


def create_session():
    """Create a session using the appropriate configuration

    :return: Returns an sqlalchemy session or None if a error occurred
    :rtype: Instance of :py:class: 'orm.Session'
    """
    file = CONF.database.filename

    try:
        sess = orm.sessionmaker(bind=create_engine(file))
        return sess()
    except Exception as e:
        LOG.error(_("Failed to create session due to exception: %s") % e)

    return None


def close_lingering_sessions():
    """Closes all lingering sqlalchemy sessions"""
    orm.session.close_all_sessions()


def create_engine(database_name):
    """Create the database engine with appropriate parameters

    This method should be used whenever sqlalchemy.create_engine is to be
    called. It ensures the same parameters are used across the application.

    :parameter database_name: base name of the database without sqlite://
    :type database_name: str
    :return: sqlalchemy engine instance
    :rtype: Instance of :py:class: 'sqlalchemy.engine.Engine`
    """

    return sqlalchemy.create_engine(f"sqlite:///{database_name}")


def check_database_missing():
    """Check if the database is missing, used for first time init

    :return: True if the database does not exist False if it does
    """
    file = CONF.database.filename

    LOG.info(_("Checking if database: %s exists") % file)

    if not os.path.isfile(file):
        LOG.warning(_("Database file does not exist in configured path"))
        return True

    try:
        engine = create_engine(file)
        if not database_exists(engine.url):
            return True
    except Exception as e:
        LOG.warning(e)
        return True

    return False


def create_database():
    """Create the database using sqlalchemy, used for first time init """
    file = CONF.database.filename

    try:
        LOG.info(_("Creating database"))
        engine = create_engine(file)
        LOG.info(_("Creating database tables"))
        cd.create_database_tables(engine)
    except Exception as e:
        LOG.error(_("Failed to create database due to error: %s") % e)
        raise e
