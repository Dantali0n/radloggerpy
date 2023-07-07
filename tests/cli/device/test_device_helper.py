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

from unittest import mock

from radloggerpy.cli.argument import Argument
from radloggerpy.cli.v1.device import device_helper

from tests import base


class TestDeviceHelper(base.TestCase):

    class TestDevHelper(device_helper.DeviceHelper):

        _arguments = None

        _implementation_key = 'impexp'

        @property
        def arguments(self):
            if self._arguments is None:
                self._arguments = dict()
                self._arguments.update({
                    'test': Argument('-t'),
                    'impexp': Argument('-i')
                })
            return self._arguments

    class TestDevHelperInvalid(device_helper.DeviceHelper):

        _arguments = None

        @property
        def arguments(self):
            if self._arguments is None:
                self._arguments = dict()
            return self._arguments

    def setUp(self):
        super(TestDeviceHelper, self).setUp()

    def test_construct_helper(self):
        helper = TestDeviceHelper.TestDevHelper()
        m_parser = mock.Mock()

        helper.register_arguments(m_parser)

        m_parser.add_argument.assert_has_calls(
            [
                mock.call('test', '-t'),
                mock.call('impexp', '-i')
            ],
            any_order=True
        )

    @mock.patch.object(device_helper, 'DeviceManager')
    def test_add_implementation(self, m_dev_manager):
        helper = TestDeviceHelper.TestDevHelper()

        m_dev_manager.get_device_implementations.return_value = [
            mock.Mock(NAME='example')
        ]

        helper._add_implementations()

        self.assertTrue(
            'example' in helper.arguments[
                helper._implementation_key].kwargs()['choices']
        )

    @mock.patch.object(device_helper, 'DeviceManager')
    def test_add_implementation_filter(self, m_dev_manager):
        helper = TestDeviceHelper.TestDevHelper()

        m_dev_manager.get_device_implementations.return_value = [
            mock.Mock(NAME='example1', INTERFACE='have'),
            mock.Mock(NAME='example2', INTERFACE='filter'),
        ]

        helper._add_implementations('have')

        self.assertTrue(
            'example1' in helper.arguments[
                helper._implementation_key].kwargs()['choices']
        )

        self.assertFalse(
            'example2' in helper.arguments[
                helper._implementation_key].kwargs()['choices']
        )

    @mock.patch.object(device_helper, 'DeviceManager')
    def test_add_implementation_error(self, m_dev_manager):
        """Error if not overriding _implementation_key in child classes"""
        helper = TestDeviceHelper.TestDevHelperInvalid()

        m_dev_manager.get_device_implementations.return_value = [
            mock.Mock(NAME='example1', INTERFACE='have'),
            mock.Mock(NAME='example2', INTERFACE='filter'),
        ]

        self.assertRaises(
            NotImplementedError, helper._add_implementations, 'have')
