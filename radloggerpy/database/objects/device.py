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

from radloggerpy.database.models.device import Device
from radloggerpy.database.objects.base import DatabaseObject
from radloggerpy.types.device_types import TYPE_CHOICES


class DeviceObject(DatabaseObject):
    """device object with base model attributes"""

    id = None
    name = None
    type = None
    implementation = None

    m_device = None

    def _build_object(self):
        self.m_device = Device()

        if self.id:
            self.m_device.id = self.id
        if self.name:
            self.m_device.name = self.name

        if self.type in TYPE_CHOICES.keys():
            self.m_device.type = self.type
        elif self.type in TYPE_CHOICES.values():
            index = list(TYPE_CHOICES.values()).index(self.type)
            self.m_device.type = list(TYPE_CHOICES.keys())[index]

        if self.implementation:
            self.m_device.implementation = self.implementation

    @staticmethod
    def add(session, reference):
        NotImplementedError()

    @staticmethod
    def update(session, reference, base, allow_multiple=False):
        NotImplementedError()

    @staticmethod
    def delete(session, reference, allow_multiple=False):
        NotImplementedError()

    @staticmethod
    def find(session, reference, allow_multiple=True):
        reference._build_object()

        filters = reference._filter(reference.m_device)
        query = session.query(Device).filter_by(**filters)

        if allow_multiple:
            results = query.all()

            if results is None:
                return None

            ret_results = list()
            for result in results:
                result = DeviceObject(**reference._filter(result))
                result.type = TYPE_CHOICES[result.type]
                result.implementation = result.implementation.code
                ret_results.append(result)

            return ret_results
        else:
            result = query.one_or_none()

            if result is None:
                return None

            result = DeviceObject(**reference._filter(result))
            result.type = TYPE_CHOICES[result.type]
            result.implementation = result.implementation.code
            return result

    @staticmethod
    def find_all(session, references):
        NotImplementedError()

    @staticmethod
    def add_all(session, references):
        NotImplementedError()
