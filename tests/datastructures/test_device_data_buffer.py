# Copyright (C) 2019 Dantali0n
# SPDX-License-Identifier: Apache-2.0

from unittest import mock

from oslo_log import log
from radloggerpy import config

from readerwriterlock import rwlock

from radloggerpy.datastructures import device_data_buffer
from radloggerpy.models.radiationreading import RadiationReading

from tests import base

LOG = log.getLogger(__name__)
CONF = config.CONF


class TestDeviceDataBuffer(base.TestCase):
    def setUp(self):
        super(TestDeviceDataBuffer, self).setUp()
        self.m_condition = mock.Mock()
        self.m_condition.__enter__ = mock.Mock()
        self.m_condition.__exit__ = mock.Mock()
        self.m_buffer = device_data_buffer.DeviceDataBuffer(self.m_condition)

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

    @mock.patch.object(device_data_buffer, "LOG")
    def test_add_reading_invalid(self, m_log):
        """Assert that invalid objects can not be added to the buffer"""
        m_add_readings = [RadiationReading(), object()]

        self.m_buffer.add_readings(m_add_readings)
        readings = self.m_buffer.fetch_clear_readings()

        m_log.error.assert_called_once()
        self.assertEqual(m_add_readings, readings)

    def test_add_reading_condition(self):
        m_condition = mock.Mock()
        m_condition.__enter__ = mock.Mock()
        m_condition.__exit__ = mock.Mock()
        buffer = device_data_buffer.DeviceDataBuffer(m_condition)

        m_reading = RadiationReading()
        buffer.add_readings([m_reading])

        m_condition.notify.assert_called_once()

    def test_clearing_buffer(self):
        """Test that fetch_clear will remove previous readings"""
        m_reading = RadiationReading()

        self.m_buffer.add_readings([m_reading])

        self.assertEqual([m_reading], self.m_buffer.fetch_clear_readings())
        self.assertEqual([], self.m_buffer.fetch_clear_readings())

    @mock.patch.object(rwlock.RWLockRead, "gen_rlock")
    def test_add_reading_lock(self, m_read):
        """Simulate failed lock and correct add_readings return value"""
        m_read.return_value.acquire.return_value = False
        m_reading = RadiationReading()

        self.assertFalse(self.m_buffer.add_readings([m_reading]))

    @mock.patch.object(rwlock.RWLockRead, "gen_wlock")
    def test_fetch_readings_lock(self, m_write):
        """Simulate failed lock and correct fetch_x_readings return value"""
        m_write.return_value.acquire.side_effect = [False]
        m_reading = RadiationReading()

        self.assertTrue(self.m_buffer.add_readings([m_reading]))
        self.assertIsNone(self.m_buffer.fetch_clear_readings())
