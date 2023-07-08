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

from radloggerpy._i18n import _
from radloggerpy.database.models.device import Device
from radloggerpy.database.models.measurement import Measurement
from radloggerpy.database.objects.base import DatabaseObject
from radloggerpy.database.objects.device import DeviceObject


class MeasurementObject(DatabaseObject):
    """Measurement object with base model attributes

    The device attribute can be set to an instance of
    :py:class:`radloggerpy.database.objects.device.DeviceObject` with any
    desired attribute set. When this is set it will be used by methods if
    applicable.
    """

    id = None  # Type: int
    timestamp = None  # Type: datetime.datetime

    cpm = None  # Type: int
    svh = None  # Type: float

    device = None  # Type: DeviceObject

    m_measurement = None  # Type: Measurement

    def _build_object(self):
        self.m_measurement = Measurement()

        if self.id:
            self.m_measurement.id = self.id
        if self.timestamp:
            self.m_measurement.timestamp = self.timestamp

        if self.device:
            self.device._build_object()

        if self.cpm:
            self.m_measurement.cpm = self.cpm
        if self.svh:
            self.m_measurement.svh = self.svh

    def _build_attributes(self):
        if self.m_measurement.id:
            self.id = self.m_measurement.id
        if self.m_measurement.timestamp:
            self.timestamp = self.m_measurement.timestamp

        if self.m_measurement.base_device:
            dev_obj = DeviceObject()
            dev_obj.m_device = self.m_measurement.base_device
            dev_obj._build_attributes()
            self.device = dev_obj

        if self.m_measurement.cpm:
            self.cpm = self.m_measurement.cpm
        if self.m_measurement.svh:
            self.svh = self.m_measurement.svh

    @staticmethod
    def add(session, reference):
        reference._build_object()

        """Measurement.device_id must be set to populate the field"""
        if (
            reference.m_measurement.device_id is None and
            hasattr(reference.device, "id") and
            reference.device.id
        ):
            """If no device_id is set find it through device id"""
            reference.m_measurement.device_id = reference.device.id
        elif reference.m_measurement.device_id is None and reference.device:
            """If no device_id find it through device"""
            dev = DeviceObject.find(session, reference.device, False)
            if dev is None:
                raise RuntimeError(_("No associateable Device found"))
            reference.m_measurement.device_id = dev.id

        session.add(reference.m_measurement)

        try:
            return session.commit()
        except Exception:
            session.rollback()
            # TODO(Dantali0n): These errors are horrendous for users to
            #                  understand an error abstraction is needed.
            raise

    @staticmethod
    def update(session, reference, base, allow_multiple=False):
        NotImplementedError()

    @staticmethod
    def delete(session, reference, allow_multiple=False):
        reference._build_object()

        filters = reference._filter(reference.m_measurement)
        query = session.query(Measurement).filter_by(**filters)

        if allow_multiple:
            results = query.all()

            if results is None:
                return None

            devs = list()

            for result in results:
                dev = MeasurementObject()
                dev.m_measurement = result
                session.delete(result)
                dev._build_attributes()
                devs.append(dev)
        else:
            result = query.one_or_none()

            if result is None:
                return None

            dev = MeasurementObject()
            dev.m_measurement = result
            dev._build_attributes()
            session.delete(result)

        try:
            session.commit()
        except Exception:
            session.rollback()
            # TODO(Dantali0n): These errors are horrendous for users to
            #                  understand an error abstraction is needed.
            raise

        if allow_multiple:
            return devs
        else:
            return dev

    @staticmethod
    def find(session, reference, allow_multiple=True):
        reference._build_object()

        filters = reference._filter(reference.m_measurement)
        query = session.query(Measurement).filter_by(**filters)

        if reference.device:
            dev_filter = reference.device._filter(reference.device.m_device)
            query = (
                session.query(Measurement)
                .filter_by(**filters)
                .join(Device)
                .filter_by(**dev_filter)
            )

        if allow_multiple:
            results = query.all()

            if results is None:
                return None

            ret_results = list()
            for result in results:
                dev = MeasurementObject()
                dev.m_measurement = result
                dev._build_attributes()
                ret_results.append(dev)

            return ret_results
        else:
            result = query.one_or_none()

            if result is None:
                return None

            dev = MeasurementObject()
            dev.m_measurement = result
            dev._build_attributes()
            return dev

    @staticmethod
    def find_all(session, references):
        NotImplementedError()

    @staticmethod
    def add_all(session, references):
        NotImplementedError()
