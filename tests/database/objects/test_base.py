# Copyright (C) 2019 Dantali0n
# SPDX-License-Identifier: Apache-2.0

from unittest import mock

from oslo_log import log

from radloggerpy import config

from radloggerpy.database.objects import base as base_obj

from tests import base

LOG = log.getLogger(__name__)
CONF = config.CONF


class TestDatabaseObject(base.TestCase):
    class ExampleDatabaseObject(base_obj.DatabaseObject):
        attribute1 = None
        attribute2 = None

        m_model = None

        def _build_object(self):
            pass

        def _build_attributes(self):
            pass

        @staticmethod
        def add(session, reference):
            pass

        @staticmethod
        def update(session, reference, base, allow_multiple=False):
            pass

        @staticmethod
        def delete(session, reference, allow_multiple=False):
            pass

        @staticmethod
        def find(session, reference, allow_multiple=True):
            pass

        @staticmethod
        def find_all(session, references):
            pass

        @staticmethod
        def add_all(session, references):
            pass

    def setUp(self):
        super(TestDatabaseObject, self).setUp()

    def test_init(self):
        m_atribs = {
            "attribute1": "value1",
            "attribute2": "value2",
            "attributeskip": "none",
        }

        test_obj = self.ExampleDatabaseObject(**m_atribs)

        self.assertEqual("value1", test_obj.attribute1)
        self.assertEqual("value2", test_obj.attribute2)
        self.assertIsNone(getattr(test_obj, "attributeskip", None))

    def test_filter(self):
        m_atribs = {
            "attribute1": "value1",
            "attribute2": "value2",
            "attributeskip": "none",
        }

        test_obj = self.ExampleDatabaseObject(**m_atribs)

        m_result = test_obj._filter(test_obj)

        self.assertEqual({"attribute1": "value1", "attribute2": "value2"}, m_result)

    @mock.patch.object(base_obj, "LOG")
    def test_filter_deprecate(self, m_log):
        m_atribs = {
            "attribute1": "value1",
            "attribute2": "value2",
            "attributeskip": "none",
        }

        test_obj = self.ExampleDatabaseObject(**m_atribs)

        m_result = test_obj._filter(test_obj, ignore=["attribute2"])

        m_log.warning.assert_called_once()

        self.assertEqual({"attribute1": "value1"}, m_result)
