# Copyright (C) 2019 Dantali0n
# SPDX-License-Identifier: Apache-2.0

from enum import Enum
from enum import unique


@unique
class DeviceStates(Enum):
    """Enum listing all possible device states"""

    STOPPED = 1
    INITIALIZING = 2
    RUNNING = 3
    ERROR = 4


DEVICE_STATE_CHOICES = {
    DeviceStates.STOPPED: "stopped",
    DeviceStates.INITIALIZING: "initializing",
    DeviceStates.RUNNING: "running",
    DeviceStates.ERROR: "error",
}
