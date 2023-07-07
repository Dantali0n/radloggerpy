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
from datetime import datetime
from unittest import mock

from oslo_log import log

from radloggerpy import config
from radloggerpy.database.models.device import Device
from radloggerpy.database.models.measurement import Measurement
from radloggerpy.database.objects import device
from radloggerpy.database.objects import measurement as ms

from tests import base

LOG = log.getLogger(__name__)
CONF = config.CONF


class TestMeasurementObject(base.TestCase):

    def setUp(self):
        super(TestMeasurementObject, self).setUp()

    def test_init(self):

        m_atribs = {
            "cpm": 12,
            "svh": 0.045,
            "skipme": "shouldnotexist"
        }

        test_obj = ms.MeasurementObject(**m_atribs)

        self.assertEqual(12, test_obj.cpm)
        self.assertIsNone(None, getattr(test_obj, "skipme", None))

    def test_filter(self):

        m_atribs = {
            "cpm": 12,
            "attributeskip": "none",
        }

        test_obj = ms.MeasurementObject(**m_atribs)

        m_result = test_obj._filter(test_obj)

        self.assertEqual(
            {"cpm": 12}, m_result)

    def test_build_object_unset(self):

        test_obj = ms.MeasurementObject()
        test_obj._build_object()

        self.assertIsNone(None, test_obj.m_measurement.id)
        self.assertIsNone(None, test_obj.m_measurement.device_id)
        self.assertIsNone(None, test_obj.m_measurement.timestamp)
        self.assertIsNone(None, test_obj.m_measurement.base_device)
        self.assertIsNone(None, test_obj.m_measurement.cpm)
        self.assertIsNone(None, test_obj.m_measurement.svh)

    def test_build_object_values(self):

        m_device = mock.Mock()

        m_date = datetime.utcnow()

        m_atribs = {
            "cpm": 12,
            "svh": 0.0045,
            "timestamp": m_date,
            "device": m_device
        }

        test_obj = ms.MeasurementObject(**m_atribs)
        test_obj._build_object()

        self.assertEqual(12, test_obj.m_measurement.cpm)
        self.assertEqual(0.0045, test_obj.m_measurement.svh)
        self.assertEqual(m_date, test_obj.m_measurement.timestamp)
        m_device._build_object.assert_called_once()

    def test_build_attributes_none(self):

        test_obj = ms.MeasurementObject()
        test_obj.m_measurement = Measurement()
        test_obj._build_attributes()

        self.assertIsNone(test_obj.id)
        self.assertIsNone(test_obj.timestamp)
        self.assertIsNone(test_obj.device)
        self.assertIsNone(test_obj.cpm)
        self.assertIsNone(test_obj.svh)

    def test_add(self):
        m_session = mock.Mock()

        m_date = datetime.utcnow()

        # TODO(Dantali0n): change into setting attributes directly
        m_atribs = {
            "cpm": 12,
            "svh": 0.0045,
            "timestamp": m_date,
            "device": device.DeviceObject(**{'id': 1})
        }

        test_obj = ms.MeasurementObject(**m_atribs)
        ms.MeasurementObject.add(m_session, test_obj)

        m_session.add.assert_has_calls(
            [
                mock.call(test_obj.m_measurement),
            ],
            any_order=True
        )
        m_session.commit.assert_called_once()

    def test_add_find_device(self):
        m_session = mock.Mock()
        m_date = datetime.utcnow()

        # TODO(Dantali0n): change into setting attributes directly
        m_atribs = {
            "cpm": 12,
            "svh": 0.0045,
            "timestamp": m_date,
            "device": device.DeviceObject(**{'name': 'test'})
        }

        with mock.patch.object(ms, 'DeviceObject') as m_find:
            test_obj = ms.MeasurementObject(**m_atribs)

            m_dev = Device()
            m_dev.id = 1
            m_find.find.return_value = m_dev

            ms.MeasurementObject.add(m_session, test_obj)

            m_session.add.assert_has_calls(
                [
                    mock.call(test_obj.m_measurement),
                ],
                any_order=True
            )
            m_session.commit.assert_called_once()

        m_find.find.assert_called_once()

    def test_add_find_device_error(self):
        m_session = mock.Mock()
        m_date = datetime.utcnow()

        # TODO(Dantali0n): change into setting attributes directly
        m_atribs = {
            "cpm": 12,
            "svh": 0.0045,
            "timestamp": m_date,
            "device": device.DeviceObject(**{'name': 'test'})
        }

        with mock.patch.object(ms, 'DeviceObject') as m_find:
            test_obj = ms.MeasurementObject(**m_atribs)
            m_find.find.return_value = None
            self.assertRaises(
                RuntimeError, ms.MeasurementObject.add, m_session, test_obj)

        m_find.find.assert_called_once()

    def test_add_error(self):
        m_session = mock.Mock()
        m_session.commit.side_effect = RuntimeError

        # TODO(Dantali0n): change into setting attributes directly
        m_atribs = {
            "cpm": 12,
            "device": device.DeviceObject(**{'id': 1})
        }

        test_obj = ms.MeasurementObject(**m_atribs)
        self.assertRaises(
            RuntimeError, ms.MeasurementObject.add, m_session, test_obj)

        m_session.add.assert_has_calls(
            [
                mock.call(test_obj.m_measurement),
            ],
            any_order=True
        )
        m_session.commit.assert_called_once()
        m_session.rollback.assert_called_once()

    def test_delete_obj(self):
        m_date = datetime.utcnow()

        """Represents mocked device as it will be retrieved from db """
        m_measurement = Measurement()
        m_measurement.id = 1
        m_measurement.timestamp = m_date
        m_measurement.cpm = 12
        m_measurement.svh = 0.0045
        m_measurement.base_device = Device()
        m_measurement.base_device.id = 1

        """Setup query and session to return mocked device"""
        m_query = mock.Mock()
        m_session = mock.Mock()
        m_session.query.return_value.filter_by.return_value = m_query
        m_query.one_or_none.return_value = m_measurement

        test_obj = ms.MeasurementObject(
            **{"device": device.DeviceObject(**{'id': 1})})
        result_obj = ms.MeasurementObject.delete(m_session, test_obj, False)

        m_session.delete.assert_has_calls(
            [
                mock.call(m_measurement),
            ],
            any_order=True
        )
        m_session.commit.assert_called_once()

        self.assertEqual(1, result_obj.id)
        self.assertEqual(m_date, result_obj.timestamp)
        self.assertEqual(12, result_obj.cpm)
        self.assertEqual(0.0045, result_obj.svh)
        self.assertEqual(1, result_obj.device.id)

    def test_delete_obj_multiple(self):
        m_measurement_1 = Measurement()
        m_measurement_1.id = 1
        m_measurement_1.cpm = 12
        m_measurement_1.base_device = Device()
        m_measurement_1.base_device.id = 1

        m_measurement_2 = Measurement()
        m_measurement_2.id = 2
        m_measurement_2.cpm = 34
        m_measurement_2.base_device = Device()
        m_measurement_2.base_device.id = 1

        m_query = mock.Mock()
        m_session = mock.Mock()
        m_session.query.return_value.filter_by.return_value = m_query

        m_query.all.return_value = [m_measurement_1, m_measurement_2]

        test_obj = ms.MeasurementObject(
            **{"device": device.DeviceObject(**{'id': 1})})
        result_obj = ms.MeasurementObject.delete(m_session, test_obj, True)

        m_session.delete.assert_has_calls(
            [
                mock.call(m_measurement_1),
                mock.call(m_measurement_2),
            ],
            any_order=True
        )
        m_session.commit.assert_called_once()

        self.assertEqual(1, result_obj[0].id)
        self.assertEqual(12, result_obj[0].cpm)
        self.assertEqual(1, result_obj[0].device.id)

        self.assertEqual(2, result_obj[1].id)
        self.assertEqual(34, result_obj[1].cpm)
        self.assertEqual(1, result_obj[1].device.id)

    def test_find_obj(self):
        m_date = datetime.utcnow()

        """Represents mocked device as it will be retrieved from db """
        m_measurement = Measurement()
        m_measurement.id = 1
        m_measurement.timestamp = m_date
        m_measurement.cpm = 12
        m_measurement.svh = 0.0045
        m_measurement.base_device = Device()
        m_measurement.base_device.id = 1

        """Setup query and session to return mocked device"""
        m_query = mock.Mock()
        m_session = mock.Mock()
        m_session.query.return_value.filter_by.return_value.\
            join.return_value.filter_by.return_value = m_query
        m_query.one_or_none.return_value = m_measurement

        test_obj = ms.MeasurementObject(
            **{"device": device.DeviceObject(**{'id': 1})})
        result_obj = ms.MeasurementObject.find(m_session, test_obj, False)

        self.assertEqual(1, result_obj.id)
        self.assertEqual(m_date, result_obj.timestamp)
        self.assertEqual(12, result_obj.cpm)
        self.assertEqual(0.0045, result_obj.svh)
        self.assertEqual(1, result_obj.device.id)

    def test_find_obj_none(self):

        """Setup query and session to return mocked device"""
        m_query = mock.Mock()
        m_session = mock.Mock()
        m_session.query.return_value.filter_by.return_value = m_query
        m_query.one_or_none.return_value = None

        test_obj = ms.MeasurementObject(**{"id": 1})
        result_obj = ms.MeasurementObject.find(m_session, test_obj, False)

        self.assertIsNone(result_obj)

    def test_find_obj_multiple(self):
        m_measurement_1 = Measurement()
        m_measurement_1.id = 1
        m_measurement_1.cpm = 12
        m_measurement_1.base_device = Device()
        m_measurement_1.base_device.id = 1

        m_measurement_2 = Measurement()
        m_measurement_2.id = 2
        m_measurement_2.cpm = 34
        m_measurement_2.base_device = Device()
        m_measurement_2.base_device.id = 1

        m_query = mock.Mock()
        m_session = mock.Mock()
        m_session.query.return_value.filter_by.return_value. \
            join.return_value.filter_by.return_value = m_query

        m_query.all.return_value = [m_measurement_1, m_measurement_2]

        test_obj = ms.MeasurementObject(
            **{"device": device.DeviceObject(**{'id': 1})})
        result_obj = ms.MeasurementObject.find(m_session, test_obj, True)

        self.assertEqual(1, result_obj[0].id)
        self.assertEqual(12, result_obj[0].cpm)
        self.assertEqual(1, result_obj[0].device.id)

        self.assertEqual(2, result_obj[1].id)
        self.assertEqual(34, result_obj[1].cpm)
        self.assertEqual(1, result_obj[1].device.id)

    def test_find_obj_multiple_none(self):
        m_query = mock.Mock()
        m_session = mock.Mock()
        m_session.query.return_value.filter_by.return_value. \
            join.return_value.filter_by.return_value = m_query

        m_query.all.return_value = None

        test_obj = ms.MeasurementObject(
            **{"device": device.DeviceObject(**{'id': 1})})
        result_obj = ms.MeasurementObject.find(m_session, test_obj, True)

        self.assertIsNone(result_obj)
