# Copyright (C) 2019 Dantali0n
# SPDX-License-Identifier: Apache-2.0

import abc
from threading import Condition

from typing import Type
from typing import TypeVar

from oslo_log import log
from radloggerpy import config

from radloggerpy._i18n import _
from radloggerpy.database.objects.device import DeviceObject
from radloggerpy.datastructures.device_data_buffer import DeviceDataBuffer
from radloggerpy.device.device_state_machine import DeviceStateMachine
from radloggerpy.types.device_states import DeviceStates
from radloggerpy.types.device_types import DeviceTypes

LOG = log.getLogger(__name__)
CONF = config.CONF


class Device(metaclass=abc.ABCMeta):
    """Abstract class all radiation monitoring devices should implement"""

    NAME = "Device"
    """Each radiation monitoring device should have a unique name"""

    INTERFACE = None
    """Each radiation monitoring device should use a specific interface"""

    TYPE = DeviceTypes.UNDEFINED
    """Each radiation monitoring device should define its type"""

    _U = TypeVar("_U", bound=DeviceObject)
    """Bound to :py:class:`radloggerpy.database.objects.device.DeviceObject`"""

    def __init__(self, info: Type[_U], condition: Condition):
        self.condition = condition
        self.info = info
        self.data = DeviceDataBuffer(self.condition)

        self._statemachine = DeviceStateMachine()

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

        if self._statemachine.get_state() is DeviceStates.ERROR:
            "Recover device from error state"
            LOG.info(
                _(
                    "Restarting {} device of implementation {} from "
                    "previous error state."
                ).format(self.info.name, self.info.implementation)
            )
            self._statemachine.reset_state()
        elif self._statemachine.get_state() is not DeviceStates.STOPPED:
            "Not logging a message here, DeviceManager can easily do that"
            raise RuntimeError(
                _("Can not start same device {} multiple times").format(self.info.name)
            )

        try:
            self._statemachine.transition(DeviceStates.INITIALIZING)
            self._init()
        except Exception:
            self._statemachine.transition(DeviceStates.ERROR)
            raise

        try:
            self._statemachine.transition(DeviceStates.RUNNING)
            self._run()
        except Exception:
            self._statemachine.transition(DeviceStates.ERROR)
            raise

        if self._statemachine.get_state() is DeviceStates.RUNNING:
            self._statemachine.transition(DeviceStates.STOPPED)

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

    def get_state(self):
        """Return the current statemachine state"""

        return self._statemachine.get_state()

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
