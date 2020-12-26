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

import copy
from threading import Condition

from oslo_log import log
from radloggerpy import config

from readerwriterlock import rwlock

from radloggerpy._i18n import _
from radloggerpy.models.radiationreading import RadiationReading

LOG = log.getLogger(__name__)
CONF = config.CONF


class DeviceDataBuffer:
    """Native list protected by locks for devices as data buffer

    Read and Write lock are used in reverse because CPython GIL allows multiple
    threads to add elements concurrently without the List entering an invalid
    state. When all elements are fetched and cleared the write lock is used
    because it has preference over the readers.

    All readings in the data buffer must be of type RadiationReading as
    enforced while calling add_elements.

    Adding readings will acquire and notify on the condition as this will wake
    up the DeviceManager.
    """

    def __init__(self, condition: Condition):
        self.has_reading = False
        self.condition = condition
        self.data = list()
        self.rwlock = rwlock.RWLockRead()

    def add_readings(self, readings):
        """Add the readings to the buffer

        Add all the readings to the buffer and remove any elements not of type
        :py:class: '~.RadiationReading'.

        :param readings: The readings to be added to the data buffer
        :type readings: List of :py:class: '~.RadiationReading' instances
        :return: True if the elements were successfully added False otherwise
        """

        for e in readings:
            if not isinstance(e, RadiationReading):
                LOG.error(_("Element: %s, is not of type "
                            "RadiationReading") % e)
                readings.remove(e)

        lock = self.rwlock.gen_rlock()
        try:
            if lock.acquire():
                self.data.extend(readings)
                self.has_reading = True
                with self.condition:
                    self.condition.notify()
                return True
        finally:
            lock.release()

        return False

    def has_readings(self):
        """Indicate if the buffer is not empty

        :return: True if one or more entries in buffer, false otherwise
        """
        return self.has_reading

    def fetch_clear_readings(self):
        """Retrieve all the readings from the buffer and clear the buffer

        Gets a exclusive write lock to create a reference to current data
        and subsequently clears the internal buffer. Afterwards it returns
        the previous internal readings. If getting the exclusive write lock
        failed it will return None instead.

        :return: All the buffered readings available or None if the lock fails
        :rtype: List of :py:class: '~.RadiationReading' instances | None
        """

        lock = self.rwlock.gen_wlock()
        try:
            if lock.acquire():
                self.has_reading = False
                ref = copy.copy(self.data)
                self.data.clear()
                return ref
        finally:
            lock.release()
