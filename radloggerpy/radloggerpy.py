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
from radloggerpy.common import ascii_logo
from radloggerpy.common.first_time_run import FirstTimeRun
from radloggerpy.config import config as configurator
from radloggerpy.database import database_manager
from radloggerpy.database.objects.device import DeviceObject
from radloggerpy.database.objects.measurement import MeasurementObject

LOG = log.getLogger(__name__)
CONF = config.CONF

FirstTimeRun.add_check_task(
    database_manager.check_database_missing, database_manager.create_database)


def main():
    configurator.setup_config_and_logging(sys.argv, CONF)

    # Display logo's
    LOG.info(ascii_logo.TEXT + ascii_logo.LOGO)

    # Display pid
    LOG.info(_('Starting RadLoggerPy service on PID %s') % os.getpid())

    # Perform first time initialization if required
    FirstTimeRun()

    # device = Device(type=DeviceTypes.SERIAL)
    # serial_device = SerialDevice(base_device=device)
    # device.serial = serial_device
    #
    # session = database_manager.create_session()
    # session.add(device)
    # session.add(serial_device)
    # session.commit()
    try:
        ser = serial.Serial(port='/dev/ttyUSB0', baudrate=9600,
                            parity=serial.PARITY_NONE,
                            stopbits=serial.STOPBITS_ONE,
                            bytesize=serial.EIGHTBITS)
    except serial.serialutil.SerialException as e:
        if e.errno == errno.EACCES:
            LOG.critical(_("Insufficient permissions "
                           "to open device."))
        elif e.errno == errno.ENOENT:
            LOG.critical(_("Device does not exist"))
        else:
            LOG.critical(_("Device error %d") % e.errno)
        # close all database sessions that are still left open
        database_manager.close_lingering_sessions()
        return

    sess = database_manager.create_session()
    string = ""
    while True:
        while ser.inWaiting() > 0:
            char = ser.read(1).decode("utf-8")
            if char == '\n':
                print(string)
                measure = MeasurementObject()
                measure.device = DeviceObject(**{'id': 1})
                measure.cpm = int(string)
                MeasurementObject.add(sess, measure)
                string = ""
            elif char == '\r':
                pass
            else:
                string += char
        time.sleep(60)

    # close all database sessions that are still left open
    database_manager.close_lingering_sessions()
