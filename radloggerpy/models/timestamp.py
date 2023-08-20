# Copyright (C) 2019 Dantali0n
# SPDX-License-Identifier: Apache-2.0

import time

from radloggerpy.models import base


class TimeStamp(base.BaseModel):
    _timestamp = 0

    def __init__(self):
        """Performs essential initialization for TimeStamp model"""

        super().__init__()
        # auto generate timestamp upon instantiation.
        self._timestamp = time.time()

    def set_timestamp(self, timestamp):
        """Set the internal timestamp to the passed timestamp in Epoch

        :param timestamp: The timestamp in Epoch such as from time.time()
        :type timestamp: float
        """
        self._timestamp = timestamp

    def update_timestamp(self):
        """Update the internal timestamp to the current time.time() Epoch"""

        self._timestamp = time.time()

    def get_timestamp(self):
        """Retrieve and return the internal timestamp

        :return: Epoch, time.time() representation of current time
        :rtype: float
        """
        return self._timestamp
