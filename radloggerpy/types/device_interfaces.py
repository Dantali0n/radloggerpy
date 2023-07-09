# Copyright (C) 2019 Dantali0n
# SPDX-License-Identifier: Apache-2.0

from enum import Enum
from enum import unique


@unique
class DeviceInterfaces(Enum):
    """Enum listing all possible supported interfaces for device"""

    ETHERNET = 1
    SERIAL = 2
    USB = 3


INTERFACE_CHOICES = {
    DeviceInterfaces.ETHERNET: "ethernet",
    DeviceInterfaces.SERIAL: "serial",
    DeviceInterfaces.USB: "usb",
}

INTERFACE_CHOICES_R = {value: key for (key, value) in INTERFACE_CHOICES.items()}
