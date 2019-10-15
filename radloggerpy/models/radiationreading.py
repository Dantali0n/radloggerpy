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

from radloggerpy.models import timestamp


class RadiationReading(timestamp.TimeStamp):

    _cpm = 0

    def __init__(self):
        super(RadiationReading, self).__init__()

    def set_cpm(self, cpm):
        """Set the counts per minute to the new value

        :param cpm: Counts per minute
        :type cpm: int
        """
        self._cpm = cpm

    def get_cpm(self):
        """Get the current counts per minute

        :return: The current internal counts per minute
        :rtype: int
        """
        return self._cpm
