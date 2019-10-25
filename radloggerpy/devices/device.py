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

import abc
import six

from oslo_log import log
from radloggerpy import config

from radloggerpy._i18n import _C
from radloggerpy.datastructures.device_data_buffer import DeviceDataBuffer

LOG = log.getLogger(__name__)
CONF = config.CONF


@six.add_metaclass(abc.ABCMeta)
class Device(object):
    """Abstract class all radiation monitoring devices should implement"""

    "Each radiation monitoring device should have a unique name"
    NAME = "Device"

    def __init__(self):
        self.data = DeviceDataBuffer(CONF.devices.initial_buffer_size)

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
            LOG.error(_C("Unable to retrieve data for: {0}".format(self.NAME)))
            return []
