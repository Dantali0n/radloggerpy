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

import errno
import serial
from threading import Condition
import time

from oslo_log import log
from radloggerpy import config

from radloggerpy._i18n import _
from radloggerpy.database.objects.serial_device import SerialDeviceObject
from radloggerpy.device.device_exception import DeviceException
from radloggerpy.device.device_interfaces.serial_device import SerialDevice
from radloggerpy.models.radiationreading import RadiationReading
from radloggerpy.types.device_types import DeviceTypes
from radloggerpy.types.serial_parity import PARITY_CHOICES_R

LOG = log.getLogger(__name__)
CONF = config.CONF


class ArduinoGeigerPcb(SerialDevice):
    """"""

    NAME = "ArduinoGeigerPCB"

    TYPE = DeviceTypes.AVERAGE

    def __init__(self, info: SerialDeviceObject, condition: Condition):
        super(ArduinoGeigerPcb, self).__init__(info, condition)
        self.stop = False
        self.serial = None

    def _init(self):
        self.stop = False
        parity = PARITY_CHOICES_R[self.info.parity].value
        try:
            self.serial = serial.Serial(
                port=self.info.port, baudrate=self.info.baudrate,
                parity=parity, stopbits=self.info.stopbits,
                bytesize=self.info.bytesize)
        except serial.serialutil.SerialException as e:
            if e.errno == errno.EACCES:
                LOG.critical(_("Insufficient permissions "
                               "to open device."))
                raise DeviceException
            elif e.errno == errno.ENOENT:
                LOG.critical(_("Device does not exist"))
                raise DeviceException
            else:
                LOG.critical(_("Device error %d") % e.errno)
                raise DeviceException

    def _run(self):
        string = ""
        while not self.stop:
            while self.serial.inWaiting() > 0:
                char = self.serial.read(1).decode("utf-8")
                if char == '\n':
                    measure = RadiationReading()
                    measure.set_cpm(int(string))
                    self.data.append(measure)
                    string = ""
                elif char == '\r':
                    pass
                else:
                    string += char
            time.sleep(CONF.devices.minimal_polling_delay / 1000)

        # clear serial object when returning from _run
        self.serial = None

    def stop(self):
        self.stop = True

    def is_stopping(self):
        return self.stop
