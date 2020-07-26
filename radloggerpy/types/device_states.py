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
