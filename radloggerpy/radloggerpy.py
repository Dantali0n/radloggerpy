# Copyright (C) 2019 Dantali0n
# SPDX-License-Identifier: Apache-2.0

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
    database_manager.check_database_missing, database_manager.create_database
)


def main():
    configurator.setup_config_and_logging(sys.argv, CONF)

    # Display logo's
    LOG.info(ascii_logo.TEXT + ascii_logo.LOGO)

    # Display pid
    LOG.info(_("Starting RadLoggerPy service on PID %s") % os.getpid())

    # Perform first time initialization if required
    FirstTimeRun()

    # Create database session for main thread
    sess = database_manager.create_session()

    # launch device manager
    manager = DeviceManager()

    devices = SerialDeviceObject.find_enabled(sess)
    for device in devices:
        manager.launch_device(device)

    # TODO(Dantali0n): Improve state checking and error handling
    while True:
        manager.check_devices()
        time.sleep(30)

    # close all database sessions that are still left open
    database_manager.close_lingering_sessions()


if __name__ == '__main__':
    sys.exit(main())
