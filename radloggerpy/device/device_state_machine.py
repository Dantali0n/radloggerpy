# Copyright (C) 2021 Dantali0n
# SPDX-License-Identifier: Apache-2.0

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
        DeviceStates.ERROR: {DeviceStates.STOPPED},
    }
    """Possible states and subsequent transitions"""

    def __init__(self):
        super(DeviceStateMachine, self).__init__(self._transitions)
