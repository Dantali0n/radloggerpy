# Copyright (C) 2020 Dantali0n
# SPDX-License-Identifier: Apache-2.0

import abc
from threading import Condition

from radloggerpy.database.objects.device import DeviceObject
from radloggerpy.device import device
from radloggerpy.types.device_interfaces import DeviceInterfaces


class EthernetDevice(device.Device, metaclass=abc.ABCMeta):
    """EthernetDevice base class"""

    NAME = "EthernetDevice"
    INTERFACE = DeviceInterfaces.ETHERNET

    def __init__(self, info: DeviceObject, condition: Condition):
        super(EthernetDevice, self).__init__(info, condition)
