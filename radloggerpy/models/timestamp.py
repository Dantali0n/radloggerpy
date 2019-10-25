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

import time

from radloggerpy.models import base


class TimeStamp(base.BaseModel):

    _timestamp = 0

    def __init__(self):
        """Performs essential initialization for TimeStamp model"""

        super(TimeStamp, self).__init__()
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
