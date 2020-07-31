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
from threading import Condition

import six

from radloggerpy.database.objects.serial_device import SerialDeviceObject
from radloggerpy.device import device
from radloggerpy.types.device_interfaces import DeviceInterfaces


@six.add_metaclass(abc.ABCMeta)
class SerialDevice(device.Device):
    """SerialDevice class for serial communication interface devices

    A SerialDevice is used for communication interfaces typically available
    such as `RS-232` or `RS-485`. If the device to support uses a COMx port on
    Windows or is listed in `/dev/tty*` on Linux this is the abstract class to
    implement.

    Devices implementing this class their settings are stored in the database
    with the :py:class:`radloggerpy.database.serial_device.SerialDevice`. if
    any additional information is required these can be stored using the
    :py:class:`radloggerpy.database.device_attribute.DeviceAttribute`.
    """

    # TODO(Dantali0n): Do not refer to database models but to database
    #                  interfacing classes(add_devices(session, [device])).

    NAME = "SerialDevice"
    INTERFACE = DeviceInterfaces.SERIAL

    def __init__(self, info: SerialDeviceObject, condition: Condition):
        super(SerialDevice, self).__init__(info, condition)
