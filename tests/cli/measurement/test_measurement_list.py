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
from datetime import datetime
from unittest import mock

from cliff.lister import Lister

from radloggerpy.cli.argument import Argument
from radloggerpy.cli.v1.measurement import measurement_list as mc
from radloggerpy.database.objects.device import DeviceObject

from tests import base


class TestDeviceList(base.TestCase):

    def setUp(self):
        super(TestDeviceList, self).setUp()

    def test_arguments_base(self):
        bases = copy(mc.MeasurementList.__bases__)
        f_bases = tuple(base for base in bases if base != Lister)

        m_base = mock.patch.object(
            mc.MeasurementList, '__bases__', f_bases)
        with m_base:
            m_base.is_local = True
            t_device = mc.MeasurementList()
            t_device.register_arguments(mock.Mock())

            self.assertTrue('--device' in t_device._arguments.keys())
            self.assertTrue('--name' in t_device._arguments.keys())

        # ensure that is_local on the patch does not modify the actual bases
        self.assertEqual(bases, mc.MeasurementList.__bases__)

    @mock.patch.object(mc, 'super')
    def test_arguments(self, m_super):
        m_super.return_value = mock.Mock(
            arguments={'--device': Argument(), '--name': Argument()}
        )

        bases = copy(mc.MeasurementList.__bases__)
        f_bases = tuple(base for base in bases if base != Lister)

        m_base = mock.patch.object(
            mc.MeasurementList, '__bases__', f_bases)
        with m_base:
            m_base.is_local = True
            t_device = mc.MeasurementList()
            t_device.register_arguments(mock.Mock())

            m_super.assert_called_once()

            self.assertTrue('--device' in t_device.arguments.keys())
            self.assertTrue('--name' in t_device.arguments.keys())

        # ensure that is_local on the patch does not modify the actual bases
        self.assertEqual(bases, mc.MeasurementList.__bases__)

    @mock.patch.object(mc, 'super')
    def test_parser(self, m_super):

        m_parser = mock.Mock()
        m_super.return_value.get_parser.return_value = m_parser

        # remove ShowOne from the DeviceShow inheritance
        bases = copy(mc.MeasurementList.__bases__)
        f_bases = tuple(base for base in bases if base != Lister)

        m_base = mock.patch.object(
            mc.MeasurementList, '__bases__', f_bases)
        with m_base:
            m_base.is_local = True
            t_device = mc.MeasurementList()

            t_device._add_interfaces = mock.Mock()
            t_device._add_implementations = mock.Mock()
            t_device.register_arguments = mock.Mock()

            t_device.get_parser("test")

            t_device._add_interfaces.assert_not_called()
            t_device._add_implementations.assert_not_called()

            t_device.register_arguments.assert_called_once_with(m_parser)

        # ensure that is_local on the patch does not modify the actual bases
        self.assertEqual(bases, mc.MeasurementList.__bases__)

    @mock.patch.object(mc, 'MeasurementObject')
    def test_take_action(self, m_dev_obj):

        # remove ShowOne from the DeviceShow inheritance
        bases = copy(mc.MeasurementList.__bases__)
        f_bases = tuple(base for base in bases if base != Lister)

        m_args = mock.Mock()
        m_args._get_kwargs.return_value = {}

        m_mod_dev = mock.Mock()
        m_mod_dev.id = 1337
        m_mod_dev.timestamp = datetime.utcnow()
        m_mod_dev.cpm = 12
        m_mod_dev.svh = 0.12
        m_mod_dev.device = DeviceObject(**{'id': 1})

        m_dev_obj.find.return_value = [m_mod_dev]

        m_base = mock.patch.object(
            mc.MeasurementList, '__bases__', f_bases)
        with m_base:
            m_base.is_local = True
            t_device = mc.MeasurementList()

            t_device.app = mock.Mock()

            t_result = t_device.take_action(m_args)

            self.assertEqual(t_result[1][0][0], m_mod_dev.timestamp)
            self.assertEqual(t_result[1][0][1], m_mod_dev.device.id)
            self.assertEqual(t_result[1][0][2], m_mod_dev.cpm)
            self.assertEqual(t_result[1][0][3], m_mod_dev.svh)

        # ensure that is_local on the patch does not modify the actual bases
        self.assertEqual(bases, mc.MeasurementList.__bases__)

    @mock.patch.object(mc, 'DeviceObject')
    @mock.patch.object(mc, 'MeasurementObject')
    def test_take_action_device(self, m_dev_obj, m_obj):

        # remove ShowOne from the DeviceShow inheritance
        bases = copy(mc.MeasurementList.__bases__)
        f_bases = tuple(base for base in bases if base != Lister)

        m_args = mock.Mock()
        m_args._get_kwargs.return_value = {'device': 1, 'name': 'test'}

        m_mock = mock.Mock()
        m_obj.return_value = m_mock

        m_dev_obj.find.return_value = [mock.Mock()]

        m_base = mock.patch.object(
            mc.MeasurementList, '__bases__', f_bases)
        with m_base:
            m_base.is_local = True
            t_device = mc.MeasurementList()

            t_device.app = mock.Mock()

            t_device.take_action(m_args)
            m_dev_obj.assert_called_once_with(**{'device': m_mock})

        # ensure that is_local on the patch does not modify the actual bases
        self.assertEqual(bases, mc.MeasurementList.__bases__)

    @mock.patch.object(mc, 'MeasurementObject')
    def test_take_action_none(self, m_dev_obj):

        # remove ShowOne from the DeviceShow inheritance
        bases = copy(mc.MeasurementList.__bases__)
        f_bases = tuple(base for base in bases if base != Lister)

        m_args = mock.Mock()
        m_args._get_kwargs.return_value = {}

        m_dev_obj.find.return_value = []

        m_base = mock.patch.object(
            mc.MeasurementList, '__bases__', f_bases)
        with m_base:
            m_base.is_local = True
            t_device = mc.MeasurementList()

            t_device.app = mock.Mock()

            self.assertRaises(RuntimeWarning, t_device.take_action, m_args)

        # ensure that is_local on the patch does not modify the actual bases
        self.assertEqual(bases, mc.MeasurementList.__bases__)
