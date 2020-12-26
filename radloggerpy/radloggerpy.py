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

import os
import sys
import time

from oslo_log import log
from radloggerpy import config

from radloggerpy._i18n import _
from radloggerpy.common import ascii_logo
from radloggerpy.common.first_time_run import FirstTimeRun
from radloggerpy.config import config as configurator
from radloggerpy.database import database_manager
from radloggerpy.database.objects.serial_device import SerialDeviceObject
from radloggerpy.device.device_manager import DeviceManager

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

    # Create database session for main thread
    sess = database_manager.create_session()

    # launch device manager
    manager = DeviceManager()

    # import pdb; pdb.set_trace()
    devices = SerialDeviceObject.find_enabled(sess)
    for device in devices:
        manager.launch_device(device)

    while True:
        time.sleep(1)

    # close all database sessions that are still left open
    database_manager.close_lingering_sessions()
