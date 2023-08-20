# Copyright (C) 2020 Dantali0n
# SPDX-License-Identifier: Apache-2.0

from copy import copy
from unittest import mock

from cliff.show import ShowOne
from sqlalchemy.exc import MultipleResultsFound

from radloggerpy.cli.v1.device import device_show as ds
from radloggerpy.cli.v1.device import device_show_serial as dss
from radloggerpy.device.device_manager import DeviceManager as dm

from radloggerpy.types.device_interfaces import DeviceInterfaces
from radloggerpy.types.device_types import DeviceTypes
from radloggerpy.types.serial_bytesize import SerialBytesizeTypes
from radloggerpy.types.serial_parity import SerialParityTypes
from radloggerpy.types.serial_stopbit import SerialStopbitTypes

from tests import base


class TestDeviceShowSerial(base.TestCase):
    def setUp(self):
        super(TestDeviceShowSerial, self).setUp()

    @mock.patch.object(dss, "super")
    def test_arguments(self, m_super):
        m_super.return_value = mock.Mock(arguments={})

        bases = copy(ds.DeviceShow.__bases__)
        f_bases = tuple(base for base in bases if base != ShowOne)

        m_base = mock.patch.object(ds.DeviceShow, "__bases__", f_bases)
        with m_base:
            m_base.is_local = True
            t_device = dss.DeviceShowSerial()
            t_device.register_arguments(mock.Mock())

            m_super.assert_called_once()

            self.assertTrue("--port" in t_device._arguments.keys())
            self.assertFalse("--interface" in t_device._arguments.keys())

        # ensure that is_local on the patch does not modify the actual bases
        self.assertEqual(bases, ds.DeviceShow.__bases__)

    @mock.patch.object(dss, "super")
    def test_parser(self, m_super):
        m_parser = mock.Mock()
        m_super.return_value.get_parser.return_value = m_parser

        # remove ShowOne from the DeviceShow inheritance
        bases = copy(ds.DeviceShow.__bases__)
        f_bases = tuple(base for base in bases if base != ShowOne)

        m_base = mock.patch.object(ds.DeviceShow, "__bases__", f_bases)
        with m_base:
            m_base.is_local = True
            t_device = dss.DeviceShowSerial()

            t_device._add_implementations = mock.Mock()
            t_device.register_arguments = mock.Mock()

            t_device.get_parser("test")

            t_device._add_implementations.assert_called_once_with(
                DeviceInterfaces.SERIAL
            )
            t_device.register_arguments.assert_called_once_with(m_parser)

        # ensure that is_local on the patch does not modify the actual bases
        self.assertEqual(bases, dss.DeviceShow.__bases__)

    @mock.patch.object(dss, "SerialDeviceObject")
    def test_take_action(self, m_dev_obj):
        # remove ShowOne from the DeviceShow inheritance
        bases = copy(ds.DeviceShow.__bases__)
        f_bases = tuple(base for base in bases if base != ShowOne)

        m_args = mock.Mock()
        m_args._get_kwargs.return_value = {"detailed": None}

        m_mod_dev = mock.Mock()
        m_mod_dev.id = 1
        m_mod_dev.name = "test"
        m_mod_dev.type = DeviceTypes.AVERAGE
        m_mod_dev.interface = DeviceInterfaces.SERIAL
        m_mod_dev.implementation = dm.get_device_implementations()[0].NAME
        m_mod_dev.port = "/dev/ttyUSB0"
        m_mod_dev.baudrate = 9600
        m_mod_dev.bytesize = SerialBytesizeTypes.FIVEBITS
        m_mod_dev.parity = SerialParityTypes.PARITY_NONE
        m_mod_dev.stopbits = SerialStopbitTypes.STOPBITS_ONE
        m_mod_dev.timeout = None
        m_dev_obj.find.return_value = m_mod_dev

        m_base = mock.patch.object(ds.DeviceShow, "__bases__", f_bases)
        with m_base:
            m_base.is_local = True
            t_device = dss.DeviceShowSerial()

            t_device.app = mock.Mock()

            t_result = t_device.take_action(m_args)
            self.assertEqual(t_result[1][0], m_mod_dev.id)
            self.assertEqual(t_result[1][1], m_mod_dev.name)
            self.assertEqual(t_result[1][2], m_mod_dev.type)
            self.assertEqual(t_result[1][3], m_mod_dev.interface)
            self.assertEqual(t_result[1][4], m_mod_dev.implementation)
            self.assertEqual(t_result[1][5], m_mod_dev.port)
            self.assertEqual(t_result[1][6], m_mod_dev.baudrate)
            self.assertEqual(t_result[1][7], m_mod_dev.bytesize)
            self.assertEqual(t_result[1][8], m_mod_dev.parity)
            self.assertEqual(t_result[1][9], m_mod_dev.stopbits)
            self.assertEqual(t_result[1][10], m_mod_dev.timeout)

        # ensure that is_local on the patch does not modify the actual bases
        self.assertEqual(bases, ds.DeviceShow.__bases__)

    @mock.patch.object(dss, "SerialDeviceObject")
    def test_take_action_none(self, m_dev_obj):
        # remove ShowOne from the DeviceShow inheritance
        bases = copy(ds.DeviceShow.__bases__)
        f_bases = tuple(base for base in bases if base != ShowOne)

        m_args = mock.Mock()
        m_args._get_kwargs.return_value = {"detailed": None}

        m_dev_obj.find.return_value = None

        m_base = mock.patch.object(ds.DeviceShow, "__bases__", f_bases)
        with m_base:
            m_base.is_local = True
            t_device = dss.DeviceShowSerial()

            t_device.app = mock.Mock()

            self.assertRaises(RuntimeWarning, t_device.take_action, m_args)

        # ensure that is_local on the patch does not modify the actual bases
        self.assertEqual(bases, ds.DeviceShow.__bases__)

    @mock.patch.object(dss, "SerialDeviceObject")
    def test_take_action_multiple(self, m_dev_obj):
        # remove ShowOne from the DeviceShow inheritance
        bases = copy(ds.DeviceShow.__bases__)
        f_bases = tuple(base for base in bases if base != ShowOne)

        m_args = mock.Mock()
        m_args._get_kwargs.return_value = {"detailed": None}

        m_dev_obj.find.side_effect = MultipleResultsFound()

        m_base = mock.patch.object(ds.DeviceShow, "__bases__", f_bases)
        with m_base:
            m_base.is_local = True
            t_device = dss.DeviceShowSerial()

            t_device.app = mock.Mock()

            self.assertRaises(RuntimeWarning, t_device.take_action, m_args)

        # ensure that is_local on the patch does not modify the actual bases
        self.assertEqual(bases, ds.DeviceShow.__bases__)
