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

from radloggerpy.database.models.measurement import Measurement
from radloggerpy.database.objects.base import DatabaseObject


class MeasurementObject(DatabaseObject):
    """device object with base model attributes

    Setting the ``device`` or ``device_id`` attributes will configure the
    device relation this measurement object belongs to. Setting ``device_id``
    will take precedence over setting ``device``. Additionally, ``device``
    will **not** be set by ``_build_attributes`` only ``device_id`` will.
    """

    id = None
    timestamp = None

    cpm = None
    svh = None

    device = None
    device_id = None

    m_measurement = None

    def _build_object(self):
        self.m_measurement = Measurement()

        if self.id:
            self.m_measurement.id = self.id
        if self.timestamp:
            self.m_measurement.timestamp = self.timestamp

        if self.device_id:
            self.m_measurement.device_id = self.device_id
        elif self.device:
            self.m_measurement.base_device = self.device

        if self.cpm:
            self.m_measurement.cpm = self.cpm
        if self.svh:
            self.m_measurement.svh = self.svh

    def _build_attributes(self):
        if self.m_measurement.id:
            self.id = self.m_measurement.id
        if self.m_measurement.timestamp:
            self.timestamp = self.m_measurement.timestamp

        if self.m_measurement.device_id:
            self.device_id = self.m_measurement.device_id
        elif self.m_measurement.base_device.id:
            self.device_id = self.m_measurement.base_device.id

        if self.m_measurement.cpm:
            self.cpm = self.m_measurement.cpm
        if self.m_measurement.svh:
            self.svh = self.m_measurement.svh

    @staticmethod
    def add(session, reference):
        reference._build_object()

        session.add(reference.m_measurement)

        try:
            return session.commit()
        except Exception as e:
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
        except Exception as e:
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
