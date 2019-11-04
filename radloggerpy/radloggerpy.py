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

import errno
import os
import serial
import sys
import time

from oslo_log import log
from radloggerpy import config

from radloggerpy._i18n import _
from radloggerpy.common.first_time_run import FirstTimeRun
from radloggerpy.config import config as configurator
from radloggerpy.database import database_manager
from radloggerpy.database.models.device import Device
from radloggerpy.types.device_types import DeviceTypes

LOG = log.getLogger(__name__)
CONF = config.CONF

FirstTimeRun.add_check_task(
    database_manager.check_database_missing, database_manager.create_database)


def main():
    configurator.setup_config_and_logging(sys.argv, CONF)

    # Perform first time initialization if required
    FirstTimeRun()

    LOG.info(_('Starting RadLoggerPy service on PID %s') % os.getpid())

    device = Device(type=DeviceTypes.arduino_geiger_pcb)
    session = database_manager.create_session()
    session.add(device)
    session.commit()

    try:
        ser = serial.Serial(port='/dev/ttyUSB0', baudrate=9600,
                            parity=serial.PARITY_NONE,
                            stopbits=serial.STOPBITS_ONE,
                            bytesize=serial.EIGHTBITS)
    except serial.serialutil.SerialException as e:
        if e.errno == errno.EACCES:
            LOG.critical(_("Insufficient permissions "
                           "to open device %s") % ser)
        elif e.errno == errno.EADDRNOTAVAIL:
            LOG.critical(_("Device %s does not exist") % ser)
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

    # close all database sessions that are still left open
    database_manager.close_lingering_sessions()
