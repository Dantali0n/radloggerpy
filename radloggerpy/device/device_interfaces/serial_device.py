# Copyright (C) 2019 Dantali0n
# SPDX-License-Identifier: Apache-2.0

import abc
from threading import Condition

from radloggerpy.database.objects.serial_device import SerialDeviceObject
from radloggerpy.device import device
from radloggerpy.types.device_interfaces import DeviceInterfaces


class SerialDevice(device.Device, metaclass=abc.ABCMeta):
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
