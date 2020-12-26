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

from typing import Type
from typing import TypeVar

from oslo_log import log
from radloggerpy import config

from radloggerpy._i18n import _
from radloggerpy.common.state_machine import StateMachine
from radloggerpy.database.objects.device import DeviceObject
from radloggerpy.datastructures.device_data_buffer import DeviceDataBuffer
from radloggerpy.types.device_states import DeviceStates

LOG = log.getLogger(__name__)
CONF = config.CONF


class Device(StateMachine, metaclass=abc.ABCMeta):
    """Abstract class all radiation monitoring devices should implement"""

    NAME = "Device"
    """Each radiation monitoring device should have a unique name"""

    INTERFACE = None
    """Each radiation monitoring device should use a specific interface"""

    POSSIBLE_STATES = DeviceStates.STOPPED
    """Initial state and possible state types"""

    _transitions = {
        DeviceStates.STOPPED: {DeviceStates.INITIALIZING},
        DeviceStates.INITIALIZING: {DeviceStates.RUNNING, DeviceStates.ERROR},
        DeviceStates.RUNNING: {DeviceStates.STOPPED, DeviceStates.ERROR},
        DeviceStates.ERROR: {DeviceStates.STOPPED}
    }
    """Possible states and subsequent transitions"""

    _U = TypeVar('_U', bound=DeviceObject)
    """This is what makes type hinting ugly and clunky in Python"""

    def __init__(self, info: Type[_U], condition: Condition):
        super().__init__(self._transitions)

        self.condition = condition
        self.info = info
        self.data = DeviceDataBuffer(self.condition)

    @abc.abstractmethod
    def _init(self):
        """Method to perform device initialization

        Devices are allowed to clear any flags or variables set when stop() was
        called previously inside of this method.
        """

    @abc.abstractmethod
    def _run(self):
        """Method to be called to run continuously in its own thread

        Devices should not return from this method unless the intent is for the
        device to stop retrieving data. Data can be gathered by either polling
        or using events / wait if the external system supports to do so.
        Timers may also be used, please be sure to honor:
        CONF.devices.minimal_polling_delay
        """

    def run(self):
        """Entry point for devices to initialize and start running

        Serves as the entry point for devices and calls _init and _run. In
        addition handles any required state transitions

        Any exception encountered will be raised so DeviceManager can handle it
        appropriately.
        """

        if self.get_state() is DeviceStates.ERROR:
            "Recover device from error state"
            LOG.info(_("Restarting device from previous error state"))
            self.reset_state()
        elif self.get_state() is not DeviceStates.STOPPED:
            "Not logging a message here, DeviceManager can easily do that"
            raise RuntimeError(_("Can not start same device multiple times"))

        try:
            self.transition(DeviceStates.INITIALIZING)
            self._init()
        except RuntimeError:
            self.transition(DeviceStates.ERROR)
            raise

        try:
            self.transition(DeviceStates.RUNNING)
            self._run()
        except RuntimeError:
            self.transition(DeviceStates.ERROR)
            raise

        if self.get_state() is DeviceStates.RUNNING:
            self.transition(DeviceStates.STOPPED)

    @abc.abstractmethod
    def stop(self):
        """Method when called that should halt operation of device asap

        Halting can be achieved by setting a variable and checking this
        variable inside a loop in the _run method. Other methods include using
        conditions to notify the _run method.
        """

    @abc.abstractmethod
    def is_stopping(self):
        """Should return true if in the progress of stopping false otherwise

        :return: True if stopping, false otherwise
        """

    def has_data(self):
        """Wrapper around internal buffer"""

        return self.data.has_readings()

    def get_data(self):
        """Return a collection of radiation monitoring data if any is available

        Retrieves the currently stored collection of radiation monitoring data
        and subsequently clears it.

        :return: Collection of RadiationReading objects
        :rtype: List of :py:class: '~.RadiationReading' instances
        """
        got_data = self.data.fetch_clear_readings()
        if got_data:
            return got_data
        else:
            LOG.error(_("Unable to retrieve data for: %s") % self.NAME)
            return []
