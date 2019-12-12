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

import abc
import six

from radloggerpy.database.models.device import Device
from radloggerpy.database.objects.base import DatabaseObject


@six.add_metaclass(abc.ABCMeta)
class DeviceObject(DatabaseObject):
    """Abstract device object with basic model attributes"""

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
        if self.type:
            self.m_device.type = self.type
        if self.implementation:
            self.m_device.implementation = self.implementation
