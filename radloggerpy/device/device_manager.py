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

from collections import OrderedDict
import multiprocessing

from oslo_log import log
from radloggerpy import config

import futurist

from radloggerpy._i18n import _
from radloggerpy.common.dynamic_import import import_modules
from radloggerpy.common.dynamic_import import list_module_names
from radloggerpy.device import device_types as dt
from radloggerpy.device import devices as dev

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

    """Private Map of device types and corresponding implementations"""
    _DEVICE_MAP = None

    def __init__(self):
        num_workers = CONF.devices.concurrent_worker_amount

        if num_workers == -1:
            num_workers = multiprocessing.cpu_count()
            LOG.info(_("Configured device manager for %d workers")
                     % num_workers)

        self._threadpool = futurist.GreenThreadPoolExecutor(
            max_workers=num_workers)

    @staticmethod
    def _get_device_module(module):
        device_types = []

        # discover the path for the module directory and the package
        package_path = module.__path__[0]
        package = module.__name__

        modules = list()
        for module_name in list_module_names(package_path):
            modules.append((module_name, module_name.title().replace('_', '')))

        imported_modules = import_modules(
            modules, package, fetch_attribute=True)
        for module, attribute in imported_modules:
            device_types.append(getattr(module, attribute))

        return device_types

    @staticmethod
    def get_device_types():
        """Return a collection of all device types their abstract classes

        Access abstract classes their TYPE to determine how they map to
        :py:class:`radloggerpy.types.device_types.DeviceTypes`

        :return:
        :rtype:
        """

        return DeviceManager._get_device_module(dt)

    @staticmethod
    def get_device_implementations():
        """Return a collection of all device implementations

        Access implementations their TYPE to determine how they map to
        :py:class:`radloggerpy.types.device_types.DeviceTypes`

        :return:
        :rtype:
        """

        return DeviceManager._get_device_module(dev)

    @staticmethod
    def get_device_map():
        """Return dictionary mapping device types to all concrete classes

        The map will only be generated the first time this method is called
        and is subsequently stored in :py:attr:`_DEVICE_MAP`.

        The dictionary structure follows the following schema:

        ``OrderedDict([ (DeviceTypes.SERIAL, [devices.ArduinoGeigerPcb]) ])``

        :return: Ordered dictionary mapping DeviceType enums to concrete
                 classes
        :rtype: OrderedDict with DeviceTypes as key and lists as values
        """

        if DeviceManager._DEVICE_MAP is not None:
            return DeviceManager._DEVICE_MAP

        device_map = OrderedDict()

        d_types = DeviceManager.get_device_types()
        for d_type in d_types:
            device_map[d_type.TYPE] = []

        implementations = DeviceManager.get_device_implementations()
        for implementation in implementations:
            device_map[implementation.TYPE].append(implementation)

        DeviceManager._DEVICE_MAP = device_map
        return DeviceManager._DEVICE_MAP
