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

import importlib
# from collections import OrderedDict
import multiprocessing
import pkgutil

from oslo_log import log
from radloggerpy import config

import futurist

from radloggerpy._i18n import _
from radloggerpy.device import device_types as dt

LOG = log.getLogger(__name__)
CONF = config.CONF


class DeviceManager(object):
    """Factory for device creation and management

    The following theory of operation is not finalized and alternative
    solutions are not only welcome but encouraged:

    Each device is run on the threadpool and gets scheduled and descheduled
    in accordance to the number of concurrent workers. Devices are expected
    to check for data and subsequently return to sleep upon waking up. The
    amount of time in between wake-ups should be long enough to give other
    devices time to retrieve data but short enough to have relevant timing
    data.

    Devices are expected to run in a endless loop, upon returning they will
    NOT get automatically rescheduled back into the queue of the threadpool.
    Since all devices inherit the Device super class this class will provide
    methods to store data. The storage and retrieval methods for data can
    be assumed to be thread-safe by the device.

    The polling rate of DeviceManager to retrieve data from devices depends
    on the /systems/ used to store data permanently. Some online platforms
    do not allow to specify timestamps while uploading data. This in turn
    requires a high polling rate to be able to ensure measurements get
    uploaded with accurate time information.

    """

    # """Map of types and their device names with classes"""
    # DEVICE_MAP = OrderedDict(
    #     {DeviceTypes.serial=[
    #     (ArduinoGeigerPCB.NAME, ArduinoGeigerPCB)
    # ]})

    def __init__(self):
        num_workers = CONF.devices.concurrent_worker_amount

        if num_workers == -1:
            num_workers = multiprocessing.cpu_count()
            LOG.info(_("Configured device manager for %d workers")
                     % num_workers)

        self._threadpool = futurist.GreenThreadPoolExecutor(
            max_workers=num_workers)

    @staticmethod
    def get_device_types():
        """Return a collection of all device types their abstract classes

        Access abstract classes their TYPE to determine how they map to
        :py:class:`radloggerpy.types.device_types.DeviceTypes`

        :return:
        :rtype:
        """
        device_types = []

        # discover the path for device.device_types directory
        package_path = dt.__path__

        # iterate over all files in device_types and append classes to the list
        for __, modname, ispkg in pkgutil.iter_modules(path=[package_path]):
            class_name = modname.title().replace('_', '')
            mod = importlib.import_module(package_path + modname)
            if not hasattr(mod, class_name):
                msg = "The module '" + package_path + ".%s' should have a" \
                      "'%s' class similar to the module name." % \
                      (modname, class_name)
                raise AttributeError(msg)
            else:
                device_types.append(getattr(mod, class_name))
        return device_types

    @staticmethod
    def get_device_map():
        """Return dictionary mapping device types to all concrete classes

        The dictionary structure follows the following schema;
            { DeviceTypes.serial : [devices.ArduinoGeigerPCB]}

        :return:
        :rtype:
        """
        pass
