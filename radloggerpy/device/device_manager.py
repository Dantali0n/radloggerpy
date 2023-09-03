# Copyright (C) 2019 Dantali0n
# SPDX-License-Identifier: Apache-2.0

from collections import OrderedDict
import multiprocessing
from threading import Condition
from typing import List
from typing import Type
from typing import TypeVar


from oslo_log import log
from radloggerpy import config

import futurist
from futurist import Future

from radloggerpy._i18n import _
from radloggerpy.common.dynamic_import import import_modules
from radloggerpy.common.dynamic_import import list_module_names
from radloggerpy.database.objects.device import DeviceObject
from radloggerpy.device.device import Device
from radloggerpy.device.device_exception import DeviceException
from radloggerpy.device import device_interfaces as di
from radloggerpy.device import devices as dev
from radloggerpy.types.device_interfaces import INTERFACE_CHOICES_R

LOG = log.getLogger(__name__)
CONF = config.CONF


class ManagedDevice:
    """Small data structure to keep track of running devices"""

    future: Future
    device: Device

    consecutive_errors: int = 0

    _I = TypeVar("_I", bound=Device)
    """Bound to :py:class:`radloggerpy.device.device.Device`"""

    def __init__(self, future: Future, device: Type[_I]):
        self.future = future
        self.device = device


class DeviceManager:
    """Factory for device creation and management

    The following theory of operation is not finalized and alternative
    solutions are not only welcome but encouraged:

    Each device is run on the threadpool and gets scheduled and descheduled
    in accordance to the number of concurrent workers. Devices are expected
    to check for data and subsequently return to sleep upon waking up. The
    amount of time in between wake-ups should be long enough to give other
    devices time to retrieve data but short enough to have relevant timing
    data.

    Devices are expected to run in an endless loop, upon returning they will
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

    _DEVICE_MAP = None
    """Private Map of device types and corresponding implementations"""

    def __init__(self):
        num_workers = CONF.devices.concurrent_worker_amount

        if num_workers == -1:
            num_workers = multiprocessing.cpu_count()
            LOG.info(_("Configured device manager for %d workers") % num_workers)

        self._condition = Condition()

        self._mng_devices: List[ManagedDevice] = []
        "List of ManagedDevice devices see :py:class:`ManagedDevice`"
        self._threadpool = futurist.ThreadPoolExecutor(max_workers=num_workers)
        # self._threadpool = futurist.GreenThreadPoolExecutor(
        #    max_workers=num_workers
        # )

        self.get_device_map()

    _I = TypeVar("_I", bound=Device)
    """Bound to :py:class:`radloggerpy.device.device.Device`"""

    _U = TypeVar("_U", bound=DeviceObject)
    """Bound to :py:class:`radloggerpy.database.objects.device.DeviceObject`"""

    def launch_device(self, device_obj: Type[_U]):
        """Submit the device and its parameter to the threadpool

        Submitted devices are maintained as ManagedDevice instances, this
        enables to correlate a future to its corresponding device.
        """

        dev_class = self.get_device_class(device_obj)
        dev_inst = dev_class(device_obj, self._condition)
        self._mng_devices.append(
            ManagedDevice(self._threadpool.submit(dev_inst.run), dev_inst)
        )

    def check_devices(self):
        """Check the status of the devices and handle failures

        TODO(Dantali0n): This method should use the get_state method of devices
                         instead of relying on the futures to much.
        """

        removals = []
        for mng_device in self._mng_devices:

            mng_device.device.get_state()
            future_exception = mng_device.future.exception()

            if not isinstance(future_exception, DeviceException):
                LOG.error(_("Unhandled Exception"))

            if mng_device.future.done() and CONF.devices.restart_on_error:
                mng_device.future = self._threadpool.submit(mng_device.device.run)
            elif mng_device.future.done():
                removals.append(mng_device)

        "Clean up the managed devices that have run to completion"
        for device in removals:
            self._mng_devices.remove(device)

    @staticmethod
    def _get_device_module(module):
        device_modules = []

        # discover the path for the module directory and the package
        package_path = module.__path__[0]
        package = module.__name__

        modules = list()
        for module_name in list_module_names(package_path):
            modules.append((module_name, module_name.title().replace("_", "")))

        imported_modules = import_modules(modules, package, fetch_attribute=True)
        for module, attribute in imported_modules:
            device_modules.append(getattr(module, attribute))

        return device_modules

    @staticmethod
    def get_device_interfaces():
        """Return a collection of all device interfaces their abstract classes

        Access abstract classes their INTERFACE to determine how they map to
        :py:class:`radloggerpy.types.device_interfaces.DeviceInterfaces`

        :return:
        :rtype:
        """

        return DeviceManager._get_device_module(di)

    @staticmethod
    def get_device_implementations():
        """Return a collection of all device implementations

        Access implementations their INTERFACE to determine how they map to
        :py:class:`radloggerpy.types.device_interfaces.DeviceInterfaces`

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

        ``OrderedDict([(DeviceInterfaces.SERIAL,[devices.ArduinoGeigerPcb])])``

        :return: Ordered dictionary mapping DeviceInterface enums to concrete
                 classes
        :rtype: OrderedDict with DeviceTypes as key and lists as values
        """

        if DeviceManager._DEVICE_MAP is not None:
            return DeviceManager._DEVICE_MAP

        device_map = OrderedDict()

        d_interfaces = DeviceManager.get_device_interfaces()
        for d_interface in d_interfaces:
            device_map[d_interface.INTERFACE] = []

        implementations = DeviceManager.get_device_implementations()
        for implementation in implementations:
            device_map[implementation.INTERFACE].append(implementation)

        DeviceManager._DEVICE_MAP = device_map
        return DeviceManager._DEVICE_MAP

    @staticmethod
    def get_device_class(device_obj: Type[_U]) -> Type[_I]:
        """Determines the matching device class for a device object

        The device object must specify a concrete implementation
        """

        map = DeviceManager.get_device_map()
        interfaces_inverse = INTERFACE_CHOICES_R
        implementations = map[interfaces_inverse[device_obj.interface]]
        for x in implementations:
            if x.NAME == device_obj.implementation:
                return x
