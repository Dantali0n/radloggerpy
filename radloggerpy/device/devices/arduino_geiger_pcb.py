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

from oslo_log import log
from radloggerpy import config
from radloggerpy.database.objects.serial_device import SerialDeviceObject

from radloggerpy.device.device_interfaces.serial_device import SerialDevice

LOG = log.getLogger(__name__)
CONF = config.CONF


class ArduinoGeigerPcb(SerialDevice):
    """"""

    NAME = "ArduinoGeigerPCB"

    _halt = False

    def __init__(self, info: SerialDeviceObject):
        super(ArduinoGeigerPcb, self).__init__(info)

    def _init(self):
        pass

    def _run(self):
        while not self._halt:
            time.sleep(0.1)

    def stop(self):
        self._halt = True
