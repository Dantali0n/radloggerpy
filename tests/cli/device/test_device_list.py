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

from radloggerpy.cli.v1.device import device_list as dl
from radloggerpy.device.device_manager import DeviceManager as dm

from radloggerpy.types.device_interfaces import DeviceInterfaces
from radloggerpy.types.device_types import DeviceTypes

from tests import base


class TestDeviceList(base.TestCase):

    def setUp(self):
        super(TestDeviceList, self).setUp()

    @mock.patch.object(dl, 'super')
    def test_arguments(self, m_super):
        m_super.return_value = mock.Mock(arguments={})

        bases = copy(dl.DeviceList.__bases__)
        f_bases = tuple(base for base in bases if base != Lister)

        m_base = mock.patch.object(
            dl.DeviceList, '__bases__', f_bases)
        with m_base:
            m_base.is_local = True
            t_device = dl.DeviceList()
            t_device.register_arguments(mock.Mock())

            m_super.assert_called_once()

            self.assertEqual(0, len(t_device._arguments))

        # ensure that is_local on the patch does not modify the actual bases
        self.assertEqual(bases, dl.DeviceList.__bases__)

    @mock.patch.object(dl, 'super')
    def test_parser(self, m_super):

        m_parser = mock.Mock()
        m_super.return_value.get_parser.return_value = m_parser

        # remove ShowOne from the DeviceShow inheritance
        bases = copy(dl.DeviceList.__bases__)
        f_bases = tuple(base for base in bases if base != Lister)

        m_base = mock.patch.object(
            dl.DeviceList, '__bases__', f_bases)
        with m_base:
            m_base.is_local = True
            t_device = dl.DeviceList()

            t_device._add_interfaces = mock.Mock()
            t_device._add_implementations = mock.Mock()
            t_device.register_arguments = mock.Mock()

            t_device.get_parser("test")

            t_device._add_interfaces.assert_called_once_with()
            t_device._add_implementations.assert_called_once_with()
            t_device.register_arguments.assert_called_once_with(m_parser)

        # ensure that is_local on the patch does not modify the actual bases
        self.assertEqual(bases, dl.DeviceList.__bases__)

    @mock.patch.object(dl, 'DeviceObject')
    def test_take_action(self, m_dev_obj):

        # remove ShowOne from the DeviceShow inheritance
        bases = copy(dl.DeviceList.__bases__)
        f_bases = tuple(base for base in bases if base != Lister)

        m_args = mock.Mock()
        m_args._get_kwargs.return_value = {}

        m_mod_dev = mock.Mock()
        m_mod_dev.id = 1
        m_mod_dev.name = 'test'
        m_mod_dev.type = DeviceTypes.AVERAGE
        m_mod_dev.interface = DeviceInterfaces.SERIAL
        m_mod_dev.implementation = dm.get_device_implementations()[0].NAME
        m_dev_obj.find.return_value = [m_mod_dev]

        m_base = mock.patch.object(
            dl.DeviceList, '__bases__', f_bases)
        with m_base:
            m_base.is_local = True
            t_device = dl.DeviceList()

            t_device.app = mock.Mock()

            t_result = t_device.take_action(m_args)
            self.assertEqual(t_result[1][0][0], m_mod_dev.id)
            self.assertEqual(t_result[1][0][1], m_mod_dev.enabled)
            self.assertEqual(t_result[1][0][2], m_mod_dev.name)
            self.assertEqual(t_result[1][0][3], m_mod_dev.type)
            self.assertEqual(t_result[1][0][4], m_mod_dev.interface)
            self.assertEqual(t_result[1][0][5], m_mod_dev.implementation)

        # ensure that is_local on the patch does not modify the actual bases
        self.assertEqual(bases, dl.DeviceList.__bases__)

    @mock.patch.object(dl, 'DeviceObject')
    def test_take_action_none(self, m_dev_obj):

        # remove ShowOne from the DeviceShow inheritance
        bases = copy(dl.DeviceList.__bases__)
        f_bases = tuple(base for base in bases if base != Lister)

        m_args = mock.Mock()
        m_args._get_kwargs.return_value = {}

        m_dev_obj.find.return_value = []

        m_base = mock.patch.object(
            dl.DeviceList, '__bases__', f_bases)
        with m_base:
            m_base.is_local = True
            t_device = dl.DeviceList()

            t_device.app = mock.Mock()

            self.assertRaises(RuntimeWarning, t_device.take_action, m_args)

        # ensure that is_local on the patch does not modify the actual bases
        self.assertEqual(bases, dl.DeviceList.__bases__)
