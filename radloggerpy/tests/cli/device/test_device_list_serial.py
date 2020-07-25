# -*- encoding: utf-8 -*-
# Copyright (c) 2020 Dantali0n
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

from copy import copy
from unittest import mock

from cliff.lister import Lister

from radloggerpy.cli.argument import Argument
from radloggerpy.cli.v1.device import device_list_serial as dl
from radloggerpy.device.device_manager import DeviceManager as dm

from radloggerpy.tests import base
from radloggerpy.types.device_interfaces import DeviceInterfaces
from radloggerpy.types.serial_bytesize import SerialBytesizeTypes
from radloggerpy.types.serial_parity import SerialParityTypes
from radloggerpy.types.serial_stopbit import SerialStopbitTypes


class TestDeviceList(base.TestCase):

    def setUp(self):
        super(TestDeviceList, self).setUp()

    @mock.patch.object(dl, 'super')
    def test_arguments(self, m_super):
        m_super.return_value = mock.Mock(
            arguments={'--port': Argument(), '--interface': Argument()}
        )

        bases = copy(dl.DeviceListSerial.__bases__)
        f_bases = tuple(base for base in bases if base != Lister)

        m_base = mock.patch.object(
            dl.DeviceListSerial, '__bases__', f_bases)
        with m_base:
            m_base.is_local = True
            t_device = dl.DeviceListSerial()
            t_device.register_arguments(mock.Mock())

            m_super.assert_called_once()

            self.assertTrue('--port' in t_device.arguments.keys())
            self.assertFalse('--interface' in t_device.arguments.keys())

        # ensure that is_local on the patch does not modify the actual bases
        self.assertEqual(bases, dl.DeviceListSerial.__bases__)

    @mock.patch.object(dl, 'super')
    def test_parser(self, m_super):

        m_parser = mock.Mock()
        m_super.return_value.get_parser.return_value = m_parser

        # remove ShowOne from the DeviceShow inheritance
        bases = copy(dl.DeviceListSerial.__bases__)
        f_bases = tuple(base for base in bases if base != Lister)

        m_base = mock.patch.object(
            dl.DeviceListSerial, '__bases__', f_bases)
        with m_base:
            m_base.is_local = True
            t_device = dl.DeviceListSerial()

            t_device._add_interfaces = mock.Mock()
            t_device._add_implementations = mock.Mock()
            t_device.register_arguments = mock.Mock()

            t_device.get_parser("test")

            t_device._add_interfaces.assert_not_called()

            t_device._add_implementations.assert_called_once_with(
                DeviceInterfaces.SERIAL)
            t_device.register_arguments.assert_called_once_with(m_parser)

        # ensure that is_local on the patch does not modify the actual bases
        self.assertEqual(bases, dl.DeviceListSerial.__bases__)

    @mock.patch.object(dl, 'SerialDeviceObject')
    def test_take_action(self, m_dev_obj):

        # remove ShowOne from the DeviceShow inheritance
        bases = copy(dl.DeviceListSerial.__bases__)
        f_bases = tuple(base for base in bases if base != Lister)

        m_args = mock.Mock()
        m_args._get_kwargs.return_value = {}

        m_mod_dev = mock.Mock()
        m_mod_dev.id = 1
        m_mod_dev.name = 'test'
        m_mod_dev.interface = DeviceInterfaces.SERIAL
        m_mod_dev.implementation = dm.get_device_implementations()[0].NAME
        m_mod_dev.port = '/dev/ttyUSB0'
        m_mod_dev.baudrate = 9600
        m_mod_dev.bytesize = SerialBytesizeTypes.FIVEBITS
        m_mod_dev.parity = SerialParityTypes.PARITY_NONE
        m_mod_dev.stopbits = SerialStopbitTypes.STOPBITS_ONE
        m_mod_dev.timeout = None
        m_dev_obj.find.return_value = [m_mod_dev]

        m_base = mock.patch.object(
            dl.DeviceListSerial, '__bases__', f_bases)
        with m_base:
            m_base.is_local = True
            t_device = dl.DeviceListSerial()

            t_device.app = mock.Mock()

            t_result = t_device.take_action(m_args)
            self.assertEqual(t_result[1][0][0], m_mod_dev.id)
            self.assertEqual(t_result[1][0][1], m_mod_dev.name)
            self.assertEqual(t_result[1][0][2], m_mod_dev.interface)
            self.assertEqual(t_result[1][0][3], m_mod_dev.implementation)
            self.assertEqual(t_result[1][0][4], m_mod_dev.port)
            self.assertEqual(t_result[1][0][5], m_mod_dev.baudrate)
            self.assertEqual(t_result[1][0][6], m_mod_dev.bytesize)
            self.assertEqual(t_result[1][0][7], m_mod_dev.parity)
            self.assertEqual(t_result[1][0][8], m_mod_dev.stopbits)
            self.assertEqual(t_result[1][0][9], m_mod_dev.timeout)

        # ensure that is_local on the patch does not modify the actual bases
        self.assertEqual(bases, dl.DeviceListSerial.__bases__)

    @mock.patch.object(dl, 'SerialDeviceObject')
    def test_take_action_none(self, m_dev_obj):

        # remove ShowOne from the DeviceShow inheritance
        bases = copy(dl.DeviceListSerial.__bases__)
        f_bases = tuple(base for base in bases if base != Lister)

        m_args = mock.Mock()
        m_args._get_kwargs.return_value = {}

        m_dev_obj.find.return_value = []

        m_base = mock.patch.object(
            dl.DeviceListSerial, '__bases__', f_bases)
        with m_base:
            m_base.is_local = True
            t_device = dl.DeviceListSerial()

            t_device.app = mock.Mock()

            self.assertRaises(RuntimeWarning, t_device.take_action, m_args)

        # ensure that is_local on the patch does not modify the actual bases
        self.assertEqual(bases, dl.DeviceListSerial.__bases__)
