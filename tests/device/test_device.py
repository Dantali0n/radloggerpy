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
from threading import Condition
from unittest import mock

from concurrent.futures import ThreadPoolExecutor
import time

from oslo_log import log
from radloggerpy import config
from radloggerpy.database.objects.device import DeviceObject

from radloggerpy.device.device import Device
from radloggerpy.models.radiationreading import RadiationReading
from radloggerpy.types.device_states import DeviceStates

from tests import base

LOG = log.getLogger(__name__)
CONF = config.CONF


class TestDevice(base.TestCase):

    class FakeDevice(Device):
        """Fake class to implement device for testing"""

        runner = True

        def __init__(self):
            m_dev = DeviceObject()
            m_condition = Condition()
            super(TestDevice.FakeDevice, self).__init__(m_dev, m_condition)

        def _init(self):
            self.runner = True

        def _run(self):
            """Add RadiationReading element"""
            for i in range(2):
                self.data.add_readings([RadiationReading()])
                time.sleep(0.1)

            while self.runner:
                """Keep running until stopped externally"""
                time.sleep(0.1)

        def stop(self):
            self.runner = False

        def is_stopping(self):
            return self.runner

    def setUp(self):
        super(TestDevice, self).setUp()

    def test_run_sequential(self):
        m_device = self.FakeDevice()
        m_device.runner = False
        m_device._run()

        self.assertEqual(2, len(m_device.get_data()))

    def test_run_runner(self):
        m_device = self.FakeDevice()
        self.assertEqual(DeviceStates.STOPPED, m_device.get_state())

        executor = ThreadPoolExecutor(max_workers=1)
        future = executor.submit(m_device.run)

        time.sleep(0.5)

        self.assertEqual(2, len(m_device.get_data()))
        self.assertFalse(future.done())

        m_device.runner = False
        time.sleep(0.5)
        self.assertTrue(future.done())
        self.assertEqual(DeviceStates.STOPPED, m_device.get_state())

    def test_run_error(self):
        m_device = self.FakeDevice()
        self.assertEqual(DeviceStates.STOPPED, m_device.get_state())

        m_error = RuntimeError()
        m_init = mock.Mock()
        m_init.side_effect = m_error
        m_device._init = m_init

        executor = ThreadPoolExecutor(max_workers=1)
        future = executor.submit(m_device.run)

        time.sleep(0.5)

        self.assertEqual(DeviceStates.ERROR, m_device.get_state())
        self.assertEqual(m_error, future.exception())

    def test_run_stop(self):
        m_device = self.FakeDevice()
        self.assertEqual(DeviceStates.STOPPED, m_device.get_state())

        executor = ThreadPoolExecutor(max_workers=1)
        future = executor.submit(m_device.run)

        time.sleep(0.5)

        self.assertEqual(2, len(m_device.get_data()))
        self.assertFalse(future.done())
        self.assertEqual(DeviceStates.RUNNING, m_device.get_state())

        m_device.stop()
        time.sleep(0.5)
        self.assertTrue(future.done())
        self.assertEqual(DeviceStates.STOPPED, m_device.get_state())

    def test_run_double(self):
        m_device = self.FakeDevice()
        self.assertEqual(DeviceStates.STOPPED, m_device.get_state())

        executor = ThreadPoolExecutor(max_workers=2)
        future = executor.submit(m_device.run)

        time.sleep(0.5)

        self.assertEqual(2, len(m_device.get_data()))
        self.assertFalse(future.done())
        self.assertEqual(DeviceStates.RUNNING, m_device.get_state())

        future2 = executor.submit(m_device.run)
        time.sleep(0.5)
        self.assertIsInstance(future2.exception(), RuntimeError)
        self.assertEqual(DeviceStates.RUNNING, m_device.get_state())

        m_device.stop()
        time.sleep(0.5)
        self.assertTrue(future.done())
        self.assertEqual(DeviceStates.STOPPED, m_device.get_state())

    def test_transition_double(self):
        """Tests against statemachine being a static variable"""

        m_device1 = self.FakeDevice()
        self.assertEqual(DeviceStates.STOPPED, m_device1.get_state())

        m_error = RuntimeError()
        m_init = mock.Mock()
        m_init.side_effect = m_error
        m_device1._init = m_init

        m_device2 = self.FakeDevice()
        self.assertEqual(DeviceStates.STOPPED, m_device2.get_state())

        executor = ThreadPoolExecutor(max_workers=2)
        executor.submit(m_device1.run)
        executor.submit(m_device2.run)

        time.sleep(0.5)

        self.assertEqual(DeviceStates.ERROR, m_device1.get_state())
        self.assertEqual(DeviceStates.RUNNING, m_device2.get_state())

        m_device1.stop()
        m_device2.stop()

        time.sleep(0.5)
        self.assertEqual(DeviceStates.STOPPED, m_device2.get_state())

    def test_run_stop_run(self):
        m_device = self.FakeDevice()
        executor = ThreadPoolExecutor(max_workers=1)
        future = executor.submit(m_device.run)

        time.sleep(0.5)

        self.assertEqual(2, len(m_device.get_data()))
        self.assertFalse(future.done())

        m_device.stop()
        time.sleep(0.5)
        self.assertTrue(future.done())

        future = executor.submit(m_device.run)

        time.sleep(0.5)

        self.assertEqual(2, len(m_device.get_data()))
        self.assertFalse(future.done())

        m_device.stop()
        time.sleep(0.5)
        self.assertTrue(future.done())

    def test_init_error_run(self):
        m_device = self.FakeDevice()
        executor = ThreadPoolExecutor(max_workers=1)

        r_init = m_device._init
        m_error = RuntimeError()
        m_init = mock.Mock()
        m_init.side_effect = m_error
        m_device._init = m_init

        future = executor.submit(m_device.run)

        time.sleep(0.5)

        self.assertEqual(DeviceStates.ERROR, m_device.get_state())
        self.assertEqual(m_error, future.exception())

        m_device._init = r_init

        future = executor.submit(m_device.run)

        time.sleep(0.5)

        self.assertEqual(2, len(m_device.get_data()))
        self.assertFalse(future.done())

        m_device.stop()
        time.sleep(0.5)
        self.assertTrue(future.done())

    def test_run_error_run(self):
        m_device = self.FakeDevice()
        executor = ThreadPoolExecutor(max_workers=1)

        r_run = m_device._run
        m_error = RuntimeError()
        m_run = mock.Mock()
        m_run.side_effect = m_error
        m_device._run = m_run

        future = executor.submit(m_device.run)

        time.sleep(0.5)

        self.assertEqual(DeviceStates.ERROR, m_device.get_state())
        self.assertEqual(m_error, future.exception())

        m_device._run = r_run

        future = executor.submit(m_device.run)

        time.sleep(0.5)

        self.assertEqual(2, len(m_device.get_data()))
        self.assertFalse(future.done())

        m_device.stop()
        time.sleep(0.5)
        self.assertTrue(future.done())
