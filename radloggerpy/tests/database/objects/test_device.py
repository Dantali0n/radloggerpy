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

from oslo_log import log

from radloggerpy import config
from radloggerpy.database.objects.device import DeviceObject

from radloggerpy.tests import base
from radloggerpy.types.device_types import DeviceTypes

LOG = log.getLogger(__name__)
CONF = config.CONF


class TestDeviceObject(base.TestCase):

    def setUp(self):
        super(TestDeviceObject, self).setUp()

    def test_init(self):

        m_atribs = {
            "name": "value1",
            "attributeskip": "none",
        }

        test_obj = DeviceObject(**m_atribs)

        self.assertEqual("value1", test_obj.name)
        self.assertIsNone(None, getattr(test_obj, "attributeskip", None))

    def test_filter(self):

        m_atribs = {
            "name": "value1",
            "attributeskip": "none",
        }

        test_obj = DeviceObject(**m_atribs)

        m_result = test_obj._filter(test_obj)

        self.assertEqual(
            {"name": "value1"}, m_result)

    def test_build_object_unset(self):

        test_obj = DeviceObject()
        test_obj._build_object()

        self.assertIsNone(None, test_obj.m_device.id)
        self.assertIsNone(None, test_obj.m_device.name)
        self.assertIsNone(None, test_obj.m_device.type)
        self.assertIsNone(None, test_obj.m_device.implementation)

    def test_build_object_values(self):

        m_atribs = {
            "id": 1,
            "name": "value1",
            "type": "serial",
            "implementation": "ArduinoGeigerPCB",
        }

        test_obj = DeviceObject(**m_atribs)
        test_obj._build_object()

        self.assertEqual(1, test_obj.m_device.id)
        self.assertEqual("value1", test_obj.m_device.name)
        self.assertEqual(DeviceTypes.SERIAL, test_obj.m_device.type)

    def test_build_object_keys(self):

        m_atribs = {
            "id": 2,
            "name": "value2",
            "type": DeviceTypes.SERIAL,
            "implementation": "ArduinoGeigerPCB",
        }

        test_obj = DeviceObject(**m_atribs)
        test_obj._build_object()

        self.assertEqual(2, test_obj.m_device.id)
        self.assertEqual("value2", test_obj.m_device.name)
        self.assertEqual(DeviceTypes.SERIAL, test_obj.m_device.type)
