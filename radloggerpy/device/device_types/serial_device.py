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

from radloggerpy.device import device
from radloggerpy.types.device_types import DeviceTypes


@six.add_metaclass(abc.ABCMeta)
class SerialDevice(device.Device):
    """"""

    NAME = "SerialDevice"
    TYPE = DeviceTypes.SERIAL

    def __init__(self):
        super(SerialDevice, self).__init__()
