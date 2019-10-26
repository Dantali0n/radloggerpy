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

from oslo_log import log
from radloggerpy import config

from radloggerpy.datastructures import device_data_buffer
from radloggerpy.datastructures import reentrant_rw_lock
from radloggerpy.models.radiationreading import RadiationReading
from radloggerpy.tests import base

LOG = log.getLogger(__name__)
CONF = config.CONF


class TestDeviceDataBuffer(base.TestCase):

    def setUp(self):
        super(TestDeviceDataBuffer, self).setUp()
        self.m_buffer = device_data_buffer.DeviceDataBuffer()

    def test_add_readings_empty(self):
        """Test that buffer remains empty when adding empty collection"""
        self.m_buffer.add_readings([])

        self.assertEqual([], self.m_buffer.fetch_clear_readings())

    def test_add_reading(self):
        """Add single valid reading and assert it can be fetched"""
        m_reading = RadiationReading()

        self.m_buffer.add_readings([m_reading])

        readings = self.m_buffer.fetch_clear_readings()
        self.assertEqual([m_reading], readings)

    @mock.patch.object(device_data_buffer, 'LOG')
    def test_add_reading_invalid(self, m_log):
        """Assert that invalid objects can not be added to the buffer"""
        m_add_readings = [RadiationReading(), object()]

        self.m_buffer.add_readings(m_add_readings)
        readings = self.m_buffer.fetch_clear_readings()

        m_log.error.assert_called_once()
        self.assertEqual(m_add_readings, readings)

    @mock.patch.object(
        reentrant_rw_lock.ReentrantReadWriteLock, 'read_acquire')
    def test_add_reading_lock(self, m_read):
        """Simulate failed lock and correct add_readings return value"""
        m_read.return_value = False
        m_reading = RadiationReading()

        self.assertFalse(self.m_buffer.add_readings([m_reading]))

    @mock.patch.object(
        reentrant_rw_lock.ReentrantReadWriteLock, 'write_acquire')
    def test_fetch_readings_lock(self, m_read):
        """Simulate failed lock and correct fetch_x_readings return value"""
        m_read.side_effect = [False]
        m_reading = RadiationReading()

        self.assertTrue(self.m_buffer.add_readings([m_reading]))
        self.assertIsNone(self.m_buffer.fetch_clear_readings())
