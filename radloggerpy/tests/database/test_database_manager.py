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

import os
from unittest import mock


from oslo_log import log
from sqlalchemy import orm

from radloggerpy import config

from radloggerpy.database import create_database as cd
from radloggerpy.database import database_manager as dbm
from radloggerpy.tests import base

LOG = log.getLogger(__name__)
CONF = config.CONF


class TestDatabaseManager(base.TestCase):

    def setUp(self):
        super(TestDatabaseManager, self).setUp()

        self.p_file = mock.patch.object(
            os.path, 'isfile',
            new_callable=mock.PropertyMock)
        self.m_isfile = self.p_file.start()
        self.addCleanup(self.p_file.stop)

        self.p_database = mock.patch.object(
            dbm, 'database_exists',
            new_callable=mock.PropertyMock)
        self.m_database = self.p_database.start()
        self.addCleanup(self.p_database.stop)

    def test_create_engine(self):
        engine = dbm.create_engine("test.sqlite")

        self.assertEqual("sqlite:///test.sqlite", '%s' % engine.url)

    @mock.patch.object(dbm, 'create_engine')
    def test_create_session(self, m_engine):
        m_engine.return_value = "sqlite:///test.sqlite"

        session = dbm.create_session()

        m_engine.assert_called_once()
        self.assertIsInstance(session, orm.Session)
        self.assertEqual("sqlite:///test.sqlite", session.bind)

    @mock.patch.object(dbm, 'LOG')
    @mock.patch.object(dbm, 'create_engine')
    def test_create_session_error(self, m_engine, m_log):
        m_engine.side_effect = Exception()

        session = dbm.create_session()

        m_engine.assert_called_once()
        m_log.error.assert_called_once()
        self.assertIsNone(None, session)

    def test_check_database_missing(self):
        self.m_isfile.return_value = False

        self.assertTrue(dbm.check_database_missing())

    def test_check_database_exists(self):
        self.m_isfile.return_value = True
        self.m_database.return_value = True

        self.assertFalse(dbm.check_database_missing())

    def test_check_database_missing_exists(self):
        self.m_isfile.return_value = True
        self.m_database.return_value = False

        self.assertTrue(dbm.check_database_missing())

    @mock.patch.object(dbm, 'LOG')
    def test_check_database_missing_error(self, m_log):
        self.m_isfile.return_value = True
        self.m_database.side_effect = Exception()

        self.assertTrue(dbm.check_database_missing())
        m_log.warning.assert_called_once()

    @mock.patch.object(dbm, 'create_engine')
    @mock.patch.object(cd, 'create_database_tables')
    def test_create_database(self, m_create, m_engine):
        m_engine.return_value = mock.Mock()
        m_create.return_value = True

        dbm.create_database()

        m_create.assert_called_once_with(m_engine())

    @mock.patch.object(dbm, 'create_engine')
    @mock.patch.object(dbm, 'LOG')
    @mock.patch.object(cd, 'create_database_tables')
    def test_create_database_error(self, m_create, m_log, m_engine):
        m_engine.return_value = mock.Mock()
        m_create.side_effect = AssertionError()

        self.assertRaises(AssertionError, dbm.create_database)

        m_create.assert_called_once_with(m_engine())
        m_log.error.assert_called_once()
