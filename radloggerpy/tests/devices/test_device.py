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

from concurrent.futures import ThreadPoolExecutor
import time

from oslo_log import log
from radloggerpy import config

from radloggerpy.device.device import Device
from radloggerpy.models.radiationreading import RadiationReading
from radloggerpy.tests import base

LOG = log.getLogger(__name__)
CONF = config.CONF


class TestDevice(base.TestCase):

    class FakeDevice(Device):
        """Fake class to implement device for testing"""

        runner = True

        def __init__(self):
            super(TestDevice.FakeDevice, self).__init__()

        def run(self):
            """Add RadiationReading element"""
            for i in range(2):
                self.data.add_readings([RadiationReading()])
                time.sleep(0.1)

            while self.runner:
                """Keep running until stopped externally"""
                time.sleep(0.1)

    def setUp(self):
        super(TestDevice, self).setUp()
        self.m_device = self.FakeDevice()

    def test_run_sequential(self):
        self.m_device.runner = False
        self.m_device.run()

        self.assertEqual(2, len(self.m_device.get_data()))

    def test_run_runner(self):

        executor = ThreadPoolExecutor(max_workers=1)
        future = executor.submit(self.m_device.run)

        time.sleep(0.5)

        self.assertEqual(2, len(self.m_device.get_data()))
        self.assertFalse(future.done())

        self.m_device.runner = False
        time.sleep(0.5)
        self.assertTrue(future.done())
