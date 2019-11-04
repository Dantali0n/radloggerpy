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

import mock
import multiprocessing

from oslo_log import log
from radloggerpy import config

from radloggerpy.device.device_manager import DeviceManager
from radloggerpy.tests import base

LOG = log.getLogger(__name__)
CONF = config.CONF


class TestDeviceManager(base.TestCase):

    def setUp(self):
        super(TestDeviceManager, self).setUp()

    @mock.patch.object(multiprocessing, 'cpu_count')
    def test_num_processors(self, m_cpu):
        m_cpu.return_value = 2

        self.m_dmanager = DeviceManager()

        m_cpu.assert_called_once_with()

    def test_conf_workers(self):
        CONF.devices.concurrent_worker_amount = 2

        self.m_dmanager = DeviceManager()
