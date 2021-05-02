# Copyright (c) 2021 Dantali0n
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

from oslo_log import log
from radloggerpy import config

from radloggerpy.common.state_machine import StateMachine
from radloggerpy.types.device_states import DeviceStates

LOG = log.getLogger(__name__)
CONF = config.CONF


class DeviceStateMachine(StateMachine):
    """State machine class for devices

    can be constructed without arguments
    """

    POSSIBLE_STATES = DeviceStates.STOPPED
    """Initial state and possible state types"""

    _transitions = {
        DeviceStates.STOPPED: {DeviceStates.INITIALIZING},
        DeviceStates.INITIALIZING: {DeviceStates.RUNNING, DeviceStates.ERROR},
        DeviceStates.RUNNING: {DeviceStates.STOPPED, DeviceStates.ERROR},
        DeviceStates.ERROR: {DeviceStates.STOPPED}
    }
    """Possible states and subsequent transitions"""

    def __init__(self):
        super(DeviceStateMachine, self).__init__(self._transitions)
