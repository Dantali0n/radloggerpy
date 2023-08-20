# Copyright (C) 2021 Dantali0n
# SPDX-License-Identifier: Apache-2.0

from enum import Enum
from enum import unique


@unique
class DeviceTypes(Enum):
    """Enum listing all possible device types"""

    UNDEFINED = 1
    CONTINUOUS = 2
    AVERAGE = 3


DEVICE_TYPE_CHOICES = {
    DeviceTypes.UNDEFINED: "undefined",
    DeviceTypes.CONTINUOUS: "continuous",
    DeviceTypes.AVERAGE: "average",
}
