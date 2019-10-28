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

import os.path

from oslo_log import log
from radloggerpy import config

import sqlalchemy
from sqlalchemy_utils import create_database
from sqlalchemy_utils import database_exists

from radloggerpy._i18n import _

LOG = log.getLogger(__name__)
CONF = config.CONF


class DatabaseManager(object):

    def __init__(self):
        pass

    @staticmethod
    def create_engine(database_name):
        """Create the database engine with appropriate parameters

        This method should be used whenever sqlalchemy.create_engine is to be
        called. It ensures the same parameters are used across the application.

        :parameter database_name: base name of the database without sqlite://
        :type database_name: str
        :return: sqlalchemy engine instance
        :rtype: Instance of :py:class: 'sqlalchemy.engine.Engine`
        """

        return sqlalchemy.create_engine("sqlite:///{0}".format(database_name))

    @staticmethod
    def check_database_missing():
        """Check if the database is missing

        :return: True if the database does not exist False if it does
        """
        file = CONF.database.filename

        LOG.info(_("Checking if database: %s exists") % file)

        if not os.path.isfile(file):
            LOG.warning(_("Database file does not exist in configured path"))
            return True

        try:
            engine = DatabaseManager.create_engine(file)
            if not database_exists(engine.url):
                return True
        except Exception as e:
            LOG.warning(e)
            return True

        return False

    @staticmethod
    def create_database():
        """Create the database using sqlalchemy utils"""
        file = CONF.database.filename

        try:
            LOG.info(_("Creating database"))
            engine = DatabaseManager.create_engine(file)
            DatabaseManager.create_engine(engine.url)
            create_database(engine.url)
        except Exception as e:
            LOG.error(_("Failed to create database due to error: %s") % e)
