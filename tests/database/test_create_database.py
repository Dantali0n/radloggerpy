# Copyright (C) 2019 Dantali0n
# SPDX-License-Identifier: Apache-2.0

import importlib
import pkgutil
from unittest import mock


from oslo_log import log
from radloggerpy import config

from sqlalchemy import create_engine, text

from radloggerpy.common.dynamic_import import import_modules
from radloggerpy.common.dynamic_import import list_module_names
from radloggerpy.database import create_database as cd
from radloggerpy.database import models
from radloggerpy.database.models import device

from tests import base

LOG = log.getLogger(__name__)
CONF = config.CONF


class TestCreateDatabase(base.TestCase):
    def setUp(self):
        super(TestCreateDatabase, self).setUp()

        self.m_path = models.__path__[0]

    def test_create_tables(self):
        m_engine = create_engine("sqlite:///:memory:", echo=True)
        cd.create_database_tables(m_engine)

        # connect to the in memory database and query the number of tables
        m_conn = m_engine.connect()
        m_text = text("SELECT name FROM sqlite_master WHERE type='table'")
        result = m_conn.execute(m_text).fetchall()
        m_conn.close()

        # assert that as many tables as models were created.
        # WARNING: this will break when there are many-to-many relationships
        self.assertEqual(len(list_module_names(self.m_path)), len(result))

    @mock.patch.object(cd, "import_modules")
    @mock.patch.object(cd, "list_module_names")
    def test_list_tables(self, m_list_modules, m_import_models):
        """Test list_tables list generation by accessing tuples"""

        # return a list with the supposed names of modules
        m_list_modules.return_value = ["a", "b"]

        # create mocked classes with the __table__ attribute
        m_a = mock.Mock(__table__="value1")
        m_b = mock.Mock(__table__="value2")

        # return tuples were the right side contains a string to access the
        # attribute of the left object. This object should have the __table__
        # attribute.
        m_import_models.return_value = [
            (mock.Mock(A=m_a), "A"),
            (mock.Mock(B=m_b), "B"),
        ]

        result = cd._list_tables()

        # assert _list_tables called list_model and import_models
        m_list_modules.assert_called_once_with(self.m_path)
        m_import_models.assert_called_once_with(
            [("a", "A"), ("b", "B")],
            "radloggerpy.database.models",
            fetch_attribute=True,
        )

        self.assertEqual(["value1", "value2"], result)

    def test_modules_names(self):
        """Test that all model files are properly discovered"""

        # get all modules of the model directory using the directory __path__
        modules = list()
        for __, modname, ispkg in pkgutil.iter_modules(path=[models.__path__[0]]):
            modules.append(modname)

        # ensure that _list_model_names() gets all modules properly
        self.assertEqual(modules, list_module_names(self.m_path))

    def test_module_import(self):
        """Assert correct import of model with returned tuple"""

        self.assertEqual(
            [(device, "Device")],
            import_modules(
                [("device", "Device")],
                "radloggerpy.database.models",
                fetch_attribute=True,
            ),
        )

    @mock.patch.object(importlib, "import_module")
    def test_module_import_exception(self, m_importlib):
        """Assert raising exception on failed import of model"""
        m_module = ("fake_model", "FakeModel")

        # ensure mocked return does not have attribute FakeModel
        m_importlib.return_value = object()

        self.assertRaises(
            AttributeError,
            import_modules,
            [m_module],
            self.m_path,
            fetch_attribute=True,
        )
