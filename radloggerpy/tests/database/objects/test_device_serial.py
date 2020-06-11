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
from radloggerpy.database.models.serial_device import SerialDevice
from radloggerpy.database.objects.serial_device import SerialDeviceObject

from radloggerpy.tests import base
from radloggerpy.types.device_interfaces import DeviceInterfaces
from radloggerpy.types.serial_bytesize import SerialBytesizeTypes
from radloggerpy.types.serial_parity import SerialParityTypes
from radloggerpy.types.serial_stopbit import SerialStopbitTypes

LOG = log.getLogger(__name__)
CONF = config.CONF


class TestSerialDeviceObject(base.TestCase):

    def setUp(self):
        super(TestSerialDeviceObject, self).setUp()

    def test_init(self):

        m_atribs = {
            "port": "value1",
            "attributeskip": "none",
        }

        test_obj = SerialDeviceObject(**m_atribs)

        self.assertEqual("value1", test_obj.port)
        self.assertIsNone(None, getattr(test_obj, "attributeskip", None))

    def test_filter(self):

        m_atribs = {
            "port": "value1",
            "attributeskip": "none",
        }

        test_obj = SerialDeviceObject(**m_atribs)

        m_result = test_obj._filter(test_obj)

        self.assertEqual(
            {"port": "value1"}, m_result)

    def test_build_object_unset(self):

        test_obj = SerialDeviceObject()
        test_obj._build_object()

        self.assertIsNone(None, test_obj.m_serial_device.port)
        self.assertIsNone(None, test_obj.m_serial_device.baudrate)
        self.assertIsNone(None, test_obj.m_serial_device.bytesize)
        self.assertIsNone(None, test_obj.m_serial_device.parity)
        self.assertIsNone(None, test_obj.m_serial_device.stopbits)
        self.assertIsNone(None, test_obj.m_serial_device.timeout)

    def test_build_object_values(self):

        m_atribs = {
            "port": "/dev/ttyUSB0",
            "baudrate": 115200,
            "bytesize": 8,
            "parity": "odd",
            "stopbits": 1,
        }

        test_obj = SerialDeviceObject(**m_atribs)
        test_obj._build_object()

        self.assertEqual("/dev/ttyUSB0", test_obj.m_serial_device.port)
        self.assertEqual(115200, test_obj.m_serial_device.baudrate)
        self.assertEqual(
            SerialBytesizeTypes.EIGHTBITS, test_obj.m_serial_device.bytesize)
        self.assertEqual(
            SerialParityTypes.PARITY_ODD, test_obj.m_serial_device.parity)
        self.assertEqual(
            SerialStopbitTypes.STOPBITS_ONE, test_obj.m_serial_device.stopbits)

    def test_build_object_keys(self):

        m_atribs = {
            "port": "/dev/ttyUSB0",
            "baudrate": 115200,
            "bytesize": SerialBytesizeTypes.EIGHTBITS,
            "parity": SerialParityTypes.PARITY_ODD,
            "stopbits": SerialStopbitTypes.STOPBITS_ONE,
        }

        test_obj = SerialDeviceObject(**m_atribs)
        test_obj._build_object()

        self.assertEqual("/dev/ttyUSB0", test_obj.m_serial_device.port)
        self.assertEqual(115200, test_obj.m_serial_device.baudrate)
        self.assertEqual(
            SerialBytesizeTypes.EIGHTBITS, test_obj.m_serial_device.bytesize)
        self.assertEqual(
            SerialParityTypes.PARITY_ODD, test_obj.m_serial_device.parity)
        self.assertEqual(
            SerialStopbitTypes.STOPBITS_ONE, test_obj.m_serial_device.stopbits)

    def test_add(self):
        m_session = mock.Mock()

        # TODO(Dantali0n): change into setting attributes directly
        m_atribs = {
            "id": 1,
            "port": "/dev/ttyUSB0",
            "baudrate": 115200,
            "bytesize": SerialBytesizeTypes.EIGHTBITS,
            "parity": SerialParityTypes.PARITY_ODD,
            "stopbits": SerialStopbitTypes.STOPBITS_ONE,
        }

        test_obj = SerialDeviceObject(**m_atribs)
        SerialDeviceObject.add(m_session, test_obj)

        m_session.add.assert_has_calls(
            [
                mock.call(test_obj.m_device),
                mock.call(test_obj.m_serial_device),
            ],
            any_order=True
        )
        m_session.commit.assert_called_once()

    def test_add_error(self):
        m_session = mock.Mock()
        m_session.commit.side_effect = RuntimeError

        # TODO(Dantali0n): change into setting attributes directly
        m_atribs = {
            "id": 1,
            "port": "/dev/ttyUSB0",
            "baudrate": 115200,
            "bytesize": SerialBytesizeTypes.EIGHTBITS,
            "parity": SerialParityTypes.PARITY_ODD,
            "stopbits": SerialStopbitTypes.STOPBITS_ONE,
        }

        test_obj = SerialDeviceObject(**m_atribs)
        self.assertRaises(
            RuntimeError, SerialDeviceObject.add, m_session, test_obj)

        m_session.add.assert_has_calls(
            [
                mock.call(test_obj.m_device),
                mock.call(test_obj.m_serial_device),
            ],
            any_order=True
        )
        m_session.commit.assert_called_once()
        m_session.rollback.assert_called_once()

    def test_find_obj(self):

        """Represents mocked device as it will be retrieved from db """
        m_device = Device()
        m_device.id = 1
        m_device.name = "value2"
        m_device.interface = DeviceInterfaces.SERIAL
        m_device.implementation = mock.Mock(
            code="ArduinoGeigerPCB", value="arduinogeigerpcb")

        m_device_serial = SerialDevice()
        m_device_serial.port = "/dev/ttyUSB0"
        m_device_serial.baudrate = 115200
        m_device_serial.bytesize = SerialBytesizeTypes.EIGHTBITS
        m_device_serial.parity = SerialParityTypes.PARITY_ODD
        m_device_serial.stopbits = SerialStopbitTypes.STOPBITS_ONE

        m_device.serial = [m_device_serial]

        """Setup query and session to return mocked device"""
        m_query = mock.Mock()
        m_session = mock.Mock()
        m_session.query.return_value.filter_by.return_value.\
            join.return_value.filter_by.return_value = m_query
        m_query.one_or_none.return_value = m_device

        test_obj = SerialDeviceObject(**{"baudrate": 115200})
        result_obj = SerialDeviceObject.find(m_session, test_obj, False)

        self.assertEqual(1, result_obj.id)
        self.assertEqual("/dev/ttyUSB0", result_obj.port)
        self.assertEqual(8, result_obj.bytesize)
        self.assertEqual("odd", result_obj.parity)
        self.assertEqual(1, result_obj.stopbits)

    def test_find_obj_none(self):

        """Setup query and session to return mocked device"""
        m_query = mock.Mock()
        m_session = mock.Mock()
        m_session.query.return_value.filter_by.return_value. \
            join.return_value.filter_by.return_value = m_query
        m_query.one_or_none.return_value = None

        test_obj = SerialDeviceObject(**{"port": "/dev/ttyUSB0"})
        result_obj = SerialDeviceObject.find(m_session, test_obj, False)

        self.assertIsNone(result_obj)

    def test_find_obj_multiple(self):
        m_device1 = Device()
        m_device2 = Device()
        m_query = mock.Mock()
        m_session = mock.Mock()
        m_session.query.return_value.filter_by.return_value. \
            join.return_value.filter_by.return_value = m_query

        m_query.all.return_value = [m_device1, m_device2]

        m_device1.id = 1
        m_device1.name = "test1"
        m_device1.interface = DeviceInterfaces.SERIAL
        m_device1.implementation = mock.Mock(
            code="ArduinoGeigerPCB", value="arduinogeigerpcb")

        m_device_serial1 = SerialDevice()
        m_device_serial1.port = "/dev/ttyUSB0"
        m_device_serial1.baudrate = 115200
        m_device_serial1.bytesize = SerialBytesizeTypes.EIGHTBITS
        m_device_serial1.parity = SerialParityTypes.PARITY_ODD
        m_device_serial1.stopbits = SerialStopbitTypes.STOPBITS_ONE

        m_device1.serial = [m_device_serial1]

        m_device2.id = 2
        m_device2.name = "test2"
        m_device2.interface = DeviceInterfaces.SERIAL
        m_device2.implementation = mock.Mock(
            code="ArduinoGeigerPCB", value="arduinogeigerpcb")

        m_device_serial2 = SerialDevice()
        m_device_serial2.port = "/dev/ttyUSB2"
        m_device_serial2.baudrate = 9600
        m_device_serial2.bytesize = SerialBytesizeTypes.SEVENBITS
        m_device_serial2.parity = SerialParityTypes.PARITY_EVEN
        m_device_serial2.stopbits = SerialStopbitTypes.STOPBITS_TWO

        m_device2.serial = [m_device_serial2]

        test_obj = SerialDeviceObject(**{"interface": "serial"})
        result_obj = SerialDeviceObject.find(m_session, test_obj, True)

        self.assertEqual(1, result_obj[0].id)
        self.assertEqual("test1", result_obj[0].name)
        self.assertEqual("serial", result_obj[0].interface)
        self.assertEqual("/dev/ttyUSB0", result_obj[0].port)
        self.assertEqual(8, result_obj[0].bytesize)
        self.assertEqual("odd", result_obj[0].parity)
        self.assertEqual(1, result_obj[0].stopbits)

        self.assertEqual(2, result_obj[1].id)
        self.assertEqual("test2", result_obj[1].name)
        self.assertEqual("serial", result_obj[1].interface)
        self.assertEqual("/dev/ttyUSB2", result_obj[1].port)
        self.assertEqual(7, result_obj[1].bytesize)
        self.assertEqual("even", result_obj[1].parity)
        self.assertEqual(2, result_obj[1].stopbits)

    def test_find_obj_multiple_none(self):
        m_query = mock.Mock()
        m_session = mock.Mock()
        m_session.query.return_value.filter_by.return_value. \
            join.return_value.filter_by.return_value = m_query

        m_query.all.return_value = None

        test_obj = SerialDeviceObject(**{"interface": "serial"})
        result_obj = SerialDeviceObject.find(m_session, test_obj, True)

        self.assertIsNone(result_obj)
