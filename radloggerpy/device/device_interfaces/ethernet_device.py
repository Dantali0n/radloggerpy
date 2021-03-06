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

import abc
from threading import Condition

import six

from radloggerpy.database.objects.device import DeviceObject
from radloggerpy.device import device
from radloggerpy.types.device_interfaces import DeviceInterfaces


@six.add_metaclass(abc.ABCMeta)
class EthernetDevice(device.Device):
    """EthernetDevice base class"""

    NAME = "EthernetDevice"
    INTERFACE = DeviceInterfaces.ETHERNET

    def __init__(self, info: DeviceObject, condition: Condition):
        super(EthernetDevice, self).__init__(info, condition)
