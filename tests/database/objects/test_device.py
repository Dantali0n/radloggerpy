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

from unittest import mock

from oslo_log import log


from radloggerpy import config
from radloggerpy.database.models.device import Device
from radloggerpy.database.objects.device import DeviceObject
from radloggerpy.device.devices.arduino_geiger_pcb import ArduinoGeigerPcb
from radloggerpy.types.device_interfaces import DeviceInterfaces

from tests import base

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
        self.assertIsNone(None, test_obj.m_device.interface)
        self.assertIsNone(None, test_obj.m_device.implementation)

    def test_build_object_values(self):

        m_atribs = {
            "id": 1,
            "name": "value1",
            "interface": "serial",
            "implementation": "ArduinoGeigerPCB",
        }

        test_obj = DeviceObject(**m_atribs)
        test_obj._build_object()

        self.assertEqual(1, test_obj.m_device.id)
        self.assertEqual("value1", test_obj.m_device.name)
        self.assertEqual(DeviceInterfaces.SERIAL, test_obj.m_device.interface)

    def test_build_object_keys(self):

        m_atribs = {
            "id": 2,
            "name": "value2",
            "interface": DeviceInterfaces.SERIAL,
            "implementation": "ArduinoGeigerPCB",
        }

        test_obj = DeviceObject(**m_atribs)
        test_obj._build_object()

        self.assertEqual(2, test_obj.m_device.id)
        self.assertEqual("value2", test_obj.m_device.name)
        self.assertEqual(DeviceInterfaces.SERIAL, test_obj.m_device.interface)

    def test_build_attributes_none(self):

        test_obj = DeviceObject()
        test_obj.m_device = Device()
        test_obj._build_attributes()

        self.assertIsNone(test_obj.id)
        self.assertIsNone(test_obj.name)
        self.assertIsNone(test_obj.interface)
        self.assertIsNone(test_obj.implementation)

    def test_delete(self):
        m_session = mock.Mock()

        # TODO(Dantali0n): change into setting attributes directly
        m_atribs = {
            "id": 1,
            "name": "test1",
            "interface": DeviceInterfaces.SERIAL,
            "implementation": "ArduinoGeigerPCB",
        }

        m_query = mock.Mock()
        m_device = Device()
        m_device.id = 1
        m_device.name = "test1"
        m_device.interface = DeviceInterfaces.SERIAL
        m_device.implementation = mock.Mock(
            code="ArduinoGeigerPCB", value="arduinogeigerpcb")

        m_session.query.return_value.filter_by.return_value = m_query
        m_query.one_or_none.return_value = m_device

        test_obj = DeviceObject(**m_atribs)
        DeviceObject.delete(m_session, test_obj)

        m_session.delete.assert_has_calls(
            [
                mock.call(m_device),
            ],
            any_order=True
        )
        m_session.commit.assert_called_once()

    def test_delete_none(self):
        m_session = mock.Mock()

        # TODO(Dantali0n): change into setting attributes directly
        m_atribs = {
            "id": 1,
            "name": "test1",
            "interface": DeviceInterfaces.SERIAL,
            "implementation": "ArduinoGeigerPCB",
        }

        m_query = mock.Mock()
        m_device = Device()
        m_device.id = 1
        m_device.name = "test1"
        m_device.interface = DeviceInterfaces.SERIAL
        m_device.implementation = mock.Mock(
            code="ArduinoGeigerPCB", value="arduinogeigerpcb")

        m_session.query.return_value.filter_by.return_value = m_query
        m_query.one_or_none.return_value = None

        test_obj = DeviceObject(**m_atribs)
        DeviceObject.delete(m_session, test_obj)

        m_session.delete.assert_not_called()
        m_session.commit.assert_not_called()

    def test_delete_exception(self):
        m_session = mock.Mock()

        # TODO(Dantali0n): change into setting attributes directly
        m_atribs = {
            "id": 1,
            "name": "test1",
            "interface": DeviceInterfaces.SERIAL,
            "implementation": "ArduinoGeigerPCB",
        }

        m_query = mock.Mock()
        m_device = Device()
        m_device.id = 1
        m_device.name = "test1"
        m_device.interface = DeviceInterfaces.SERIAL
        m_device.implementation = mock.Mock(
            code="ArduinoGeigerPCB", value="arduinogeigerpcb")

        m_session.query.return_value.filter_by.return_value = m_query
        m_query.one_or_none.return_value = m_device

        m_session.commit.side_effect = RuntimeWarning

        test_obj = DeviceObject(**m_atribs)
        self.assertRaises(
            RuntimeWarning, DeviceObject.delete, m_session, test_obj)

        m_session.delete.assert_has_calls(
            [
                mock.call(m_device),
            ],
            any_order=True
        )
        m_session.commit.assert_called_once()
        m_session.rollback.assert_called_once()

    def test_delete_all(self):
        m_session = mock.Mock()

        # TODO(Dantali0n): change into setting attributes directly
        m_atribs = {
            "id": 1,
            "name": "test1",
            "interface": DeviceInterfaces.SERIAL,
            "implementation": "ArduinoGeigerPCB",
        }

        m_query = mock.Mock()
        m_device = Device()
        m_device.id = 1
        m_device.name = "test1"
        m_device.interface = DeviceInterfaces.SERIAL
        m_device.implementation = mock.Mock(
            code="ArduinoGeigerPCB", value="arduinogeigerpcb")

        m_session.query.return_value.filter_by.return_value = m_query
        m_query.all.return_value = [m_device]

        test_obj = DeviceObject(**m_atribs)
        DeviceObject.delete(m_session, test_obj, True)

        m_session.delete.assert_has_calls(
            [
                mock.call(m_device),
            ],
            any_order=True
        )
        m_session.commit.assert_called_once()

    def test_find_obj(self):

        """Represents mocked device as it will be retrieved from db """
        m_device = Device()
        m_device.id = 1
        m_device.name = "test"
        m_device.interface = DeviceInterfaces.SERIAL
        m_device.implementation = mock.Mock(
            code="ArduinoGeigerPCB", value="arduinogeigerpcb")

        """Setup query and session to return mocked device"""
        m_query = mock.Mock()
        m_session = mock.Mock()
        m_session.query.return_value.filter_by.return_value = m_query
        m_query.one_or_none.return_value = m_device

        test_obj = DeviceObject(**{"id": 1})
        result_obj = DeviceObject.find(m_session, test_obj, False)

        self.assertEqual(1, result_obj.id)
        self.assertEqual("test", result_obj.name)
        self.assertEqual("serial", result_obj.interface)
        self.assertEqual(ArduinoGeigerPcb.NAME, result_obj.implementation)

    def test_find_obj_none(self):
        m_query = mock.Mock()
        m_session = mock.Mock()
        m_session.query.return_value.filter_by.return_value = m_query

        m_query.one_or_none.return_value = None

        test_obj = DeviceObject(**{"id": 1})
        result_obj = DeviceObject.find(m_session, test_obj, False)

        self.assertIsNone(result_obj)

    def test_find_obj_multiple(self):
        m_device1 = Device()
        m_device2 = Device()
        m_query = mock.Mock()
        m_session = mock.Mock()
        m_session.query.return_value.filter_by.return_value = m_query

        m_query.all.return_value = [m_device1, m_device2]

        m_device1.id = 1
        m_device1.name = "test1"
        m_device1.interface = DeviceInterfaces.SERIAL
        m_device1.implementation = mock.Mock(
            code="ArduinoGeigerPCB", value="arduinogeigerpcb")

        m_device2.id = 2
        m_device2.name = "test2"
        m_device2.interface = DeviceInterfaces.SERIAL
        m_device2.implementation = mock.Mock(
            code="ArduinoGeigerPCB", value="arduinogeigerpcb")

        test_obj = DeviceObject(**{"interface": "serial"})
        result_obj = DeviceObject.find(m_session, test_obj, True)

        self.assertEqual(1, result_obj[0].id)
        self.assertEqual("test1", result_obj[0].name)
        self.assertEqual("serial", result_obj[0].interface)
        self.assertEqual(ArduinoGeigerPcb.NAME, result_obj[0].implementation)

        self.assertEqual(2, result_obj[1].id)
        self.assertEqual("test2", result_obj[1].name)
        self.assertEqual("serial", result_obj[1].interface)
        self.assertEqual(ArduinoGeigerPcb.NAME, result_obj[1].implementation)

    def test_find_obj_multiple_none(self):
        m_query = mock.Mock()
        m_session = mock.Mock()
        m_session.query.return_value.filter_by.return_value = m_query

        m_query.all.return_value = None

        test_obj = DeviceObject(**{"id": 1})
        result_obj = DeviceObject.find(m_session, test_obj, True)

        self.assertIsNone(result_obj)
