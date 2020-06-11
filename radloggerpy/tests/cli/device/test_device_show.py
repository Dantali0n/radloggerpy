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

from cliff.show import ShowOne
from sqlalchemy.orm.exc import MultipleResultsFound

from radloggerpy.cli.v1.device import device_show
from radloggerpy.device.device_manager import DeviceManager as dm

from radloggerpy.tests import base
from radloggerpy.types.device_interfaces import DeviceInterfaces
from radloggerpy.types.device_interfaces import INTERFACE_CHOICES
from radloggerpy.types.serial_bytesize import SerialBytesizeTypes
from radloggerpy.types.serial_parity import SerialParityTypes
from radloggerpy.types.serial_stopbit import SerialStopbitTypes


class TestDeviceShow(base.TestCase):

    def setUp(self):
        super(TestDeviceShow, self).setUp()

    @mock.patch.object(device_show, 'super')
    def test_parser(self, m_super):

        m_parser = mock.Mock()
        m_super.return_value.get_parser.return_value = m_parser

        bases = copy(device_show.DeviceShow.__bases__)
        f_bases = tuple(base for base in bases if base != ShowOne)

        m_base = mock.patch.object(
            device_show.DeviceShow, '__bases__', f_bases)
        with m_base:
            m_base.is_local = True
            t_device = device_show.DeviceShow()

            t_device._add_interfaces = mock.Mock()
            t_device._add_implementations = mock.Mock()
            t_device.register_arguments = mock.Mock()

            t_device.get_parser("test")

            t_device._add_interfaces.assert_called_once()
            t_device._add_implementations.assert_called_once()
            t_device.register_arguments.assert_called_once_with(m_parser)

        # ensure that is_local on the patch does not modify the actual bases
        self.assertEqual(bases, device_show.DeviceShow.__bases__)

    @mock.patch.object(device_show, 'DeviceObject')
    def test_take_action(self, m_dev_obj):

        bases = copy(device_show.DeviceShow.__bases__)
        f_bases = tuple(base for base in bases if base != ShowOne)

        m_args = mock.Mock()
        m_args._get_kwargs.return_value = {'detailed': None}

        m_mod_dev = mock.Mock()
        m_mod_dev.id = 1
        m_mod_dev.name = 'test'
        m_mod_dev.interface = DeviceInterfaces.SERIAL
        m_mod_dev.implementation = dm.get_device_implementations()[0].NAME
        m_dev_obj.find.return_value = m_mod_dev

        m_base = mock.patch.object(
            device_show.DeviceShow, '__bases__', f_bases)
        with m_base:
            m_base.is_local = True
            t_device = device_show.DeviceShow()

            t_device.app = mock.Mock()

            t_result = t_device.take_action(m_args)
            self.assertEqual(t_result[1][0], m_mod_dev.id)
            self.assertEqual(t_result[1][1], m_mod_dev.name)
            self.assertEqual(t_result[1][2], m_mod_dev.interface)
            self.assertEqual(t_result[1][3], m_mod_dev.implementation)

        # ensure that is_local on the patch does not modify the actual bases
        self.assertEqual(bases, device_show.DeviceShow.__bases__)

    @mock.patch.object(device_show, 'SerialDeviceObject')
    @mock.patch.object(device_show, 'DeviceObject')
    def test_take_action_details_serial(self, m_dev_obj, m_dev_ser_obj):

        bases = copy(device_show.DeviceShow.__bases__)
        f_bases = tuple(base for base in bases if base != ShowOne)

        m_args = mock.Mock()
        m_args._get_kwargs.return_value = {'detailed': True}

        m_mod_dev = mock.Mock()
        m_mod_dev.id = 1
        m_mod_dev.name = 'test'
        m_mod_dev.interface = INTERFACE_CHOICES[DeviceInterfaces.SERIAL]
        m_mod_dev.implementation = dm.get_device_implementations()[0].NAME

        m_dev_obj.find.return_value = m_mod_dev

        m_mod_ser_dev = mock.Mock()
        m_mod_ser_dev.port = '/dev/ttyUSB0'
        m_mod_ser_dev.baudrate = 9600
        m_mod_ser_dev.bytesize = SerialBytesizeTypes.FIVEBITS
        m_mod_ser_dev.parity = SerialParityTypes.PARITY_NONE
        m_mod_ser_dev.stopbits = SerialStopbitTypes.STOPBITS_ONE
        m_mod_ser_dev.timeout = None

        m_dev_ser_obj.find.return_value = m_mod_ser_dev

        m_base = mock.patch.object(
            device_show.DeviceShow, '__bases__', f_bases)
        with m_base:
            m_base.is_local = True
            t_device = device_show.DeviceShow()

            t_device.app = mock.Mock()

            t_result = t_device.take_action(m_args)
            self.assertEqual(t_result[1][0], m_mod_dev.id)
            self.assertEqual(t_result[1][1], m_mod_dev.name)
            self.assertEqual(t_result[1][2], m_mod_dev.interface)
            self.assertEqual(t_result[1][3], m_mod_dev.implementation)
            self.assertEqual(t_result[1][4], m_mod_ser_dev.port)
            self.assertEqual(t_result[1][5], m_mod_ser_dev.baudrate)
            self.assertEqual(t_result[1][6], m_mod_ser_dev.bytesize)
            self.assertEqual(t_result[1][7], m_mod_ser_dev.parity)
            self.assertEqual(t_result[1][8], m_mod_ser_dev.stopbits)
            self.assertEqual(t_result[1][9], m_mod_ser_dev.timeout)

        # ensure that is_local on the patch does not modify the actual bases
        self.assertEqual(bases, device_show.DeviceShow.__bases__)

    @mock.patch.object(device_show, 'DeviceObject')
    def test_take_action_none(self, m_dev_obj):

        bases = copy(device_show.DeviceShow.__bases__)
        f_bases = tuple(base for base in bases if base != ShowOne)

        m_args = mock.Mock()
        m_args._get_kwargs.return_value = {'detailed': None}

        m_dev_obj.find.return_value = None

        m_base = mock.patch.object(
            device_show.DeviceShow, '__bases__', f_bases)
        with m_base:
            m_base.is_local = True
            t_device = device_show.DeviceShow()

            t_device.app = mock.Mock()

            self.assertRaises(RuntimeWarning, t_device.take_action, m_args)

        # ensure that is_local on the patch does not modify the actual bases
        self.assertEqual(bases, device_show.DeviceShow.__bases__)

    @mock.patch.object(device_show, 'DeviceObject')
    def test_take_action_multiple(self, m_dev_obj):

        bases = copy(device_show.DeviceShow.__bases__)
        f_bases = tuple(base for base in bases if base != ShowOne)

        m_args = mock.Mock()
        m_args._get_kwargs.return_value = {'detailed': None}

        m_dev_obj.find.side_effect = MultipleResultsFound()

        m_base = mock.patch.object(
            device_show.DeviceShow, '__bases__', f_bases)
        with m_base:
            m_base.is_local = True
            t_device = device_show.DeviceShow()

            t_device.app = mock.Mock()

            self.assertRaises(RuntimeWarning, t_device.take_action, m_args)

        # ensure that is_local on the patch does not modify the actual bases
        self.assertEqual(bases, device_show.DeviceShow.__bases__)
