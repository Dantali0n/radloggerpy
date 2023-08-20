# Copyright (C) 2020 Dantali0n
# SPDX-License-Identifier: Apache-2.0

import abc
from threading import Condition

from radloggerpy.database.objects.device import DeviceObject
from radloggerpy.device import device
from radloggerpy.types.device_interfaces import DeviceInterfaces


class UsbDevice(device.Device, metaclass=abc.ABCMeta):
    """UsbDevice base class"""

    NAME = "UsbDevice"
    INTERFACE = DeviceInterfaces.USB

    def __init__(self, info: DeviceObject, condition: Condition):
        super(UsbDevice, self).__init__(info, condition)
