# -*- encoding: utf-8 -*-
# Copyright (c) 2019 Dantali0n
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""Starter script for RadLoggerPy."""

from oslo_log import log
import serial
import time

from radloggerpy import config

LOG = log.getLogger(__name__)
CONF = config.CONF


def main():
    LOG.warning(CONF.database.filename)
    try:
        ser = serial.Serial(port='/dev/ttyUSB0', baudrate=9600,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        bytesize=serial.EIGHTBITS)
    except serial.serialutil.SerialException as e:
        LOG.critical(e.errno)
        return

    string = ""
    while True:
        while ser.inWaiting() > 0:
            char = ser.read(1).decode("utf-8")
            if char == '\n':
                print(string)
                string = ""
            elif char == '\r':
                pass
            else:
                string += char
        time.sleep(60)
