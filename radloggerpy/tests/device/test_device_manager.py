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

import multiprocessing
from unittest import mock

from oslo_log import log
from radloggerpy import config

from radloggerpy.device import device_interfaces as di
from radloggerpy.device import device_manager as dm
from radloggerpy.device import devices as dev
from radloggerpy.tests import base

LOG = log.getLogger(__name__)
CONF = config.CONF


class TestDeviceManager(base.TestCase):

    def setUp(self):
        super(TestDeviceManager, self).setUp()

    @mock.patch.object(multiprocessing, 'cpu_count')
    def test_num_processors(self, m_cpu):
        m_cpu.return_value = 2

        self.m_dmanager = dm.DeviceManager()

        m_cpu.assert_called_once_with()

    @mock.patch.object(dm, 'futurist')
    def test_conf_workers(self, m_futurist):
        CONF.devices.concurrent_worker_amount = 2

        self.m_dmanager = dm.DeviceManager()

        m_futurist.ThreadPoolExecutor.\
            assert_called_once_with(max_workers=2)

    @mock.patch.object(dm, 'import_modules')
    @mock.patch.object(dm, 'list_module_names')
    def test_get_device_module(self, m_list_names, m_import):
        m_path = 'path'
        m_package = 'package'
        m_name = 'test'
        m_class = 'Test'

        m_module = mock.Mock(__path__=[m_path], __name__=m_package)

        m_list_names.return_value = [m_name]

        m_result = mock.Mock(Test=True)
        m_import.return_value = [(m_result, m_class)]

        result = dm.DeviceManager._get_device_module(m_module)

        m_list_names.assert_called_once_with(m_path)
        m_import.assert_called_once_with(
            [(m_name, m_class)], m_package, fetch_attribute=True)

        self.assertEqual([True], result)

    @mock.patch.object(dm.DeviceManager, '_get_device_module')
    def test_get_device_types(self, m_get_device_module):
        """Assert get_device_types called with correct module"""
        dm.DeviceManager.get_device_interfaces()

        m_get_device_module.assert_called_once_with(di)

    @mock.patch.object(dm.DeviceManager, '_get_device_module')
    def test_get_device_implementations(self, m_get_device_module):
        """Assert get_device_implementations called with correct module"""
        dm.DeviceManager.get_device_implementations()

        m_get_device_module.assert_called_once_with(dev)

    def test_get_device_map_created_once(self):
        m_map = dm.DeviceManager.get_device_map()

        self.assertEqual(m_map, dm.DeviceManager.get_device_map())
