# Copyright (C) 2019 Dantali0n
# SPDX-License-Identifier: Apache-2.0

import multiprocessing
from unittest import mock

from oslo_log import log
from radloggerpy import config
from radloggerpy.database.objects.device import DeviceObject

from radloggerpy.device import device_interfaces as di
from radloggerpy.device import device_manager as dm
from radloggerpy.device import devices as dev
from radloggerpy.types.device_implementations import IMPLEMENTATION_CHOICES
from radloggerpy.types.device_interfaces import DeviceInterfaces
from radloggerpy.types.device_interfaces import INTERFACE_CHOICES
from radloggerpy.types.device_types import DeviceTypes

from tests import base

LOG = log.getLogger(__name__)
CONF = config.CONF


class TestDeviceManager(base.TestCase):
    def setUp(self):
        super(TestDeviceManager, self).setUp()

    @mock.patch.object(multiprocessing, "cpu_count")
    def test_num_processors(self, m_cpu):
        m_cpu.return_value = 2

        self.m_dmanager = dm.DeviceManager()

        m_cpu.assert_called_once_with()

    @mock.patch.object(dm, "futurist")
    def test_conf_workers(self, m_futurist):
        CONF.devices.concurrent_worker_amount = 2

        self.m_dmanager = dm.DeviceManager()

        m_futurist.ThreadPoolExecutor.assert_called_once_with(max_workers=2)

    @mock.patch.object(dm, "import_modules")
    @mock.patch.object(dm, "list_module_names")
    def test_get_device_module(self, m_list_names, m_import):
        m_path = "path"
        m_package = "package"
        m_name = "test"
        m_class = "Test"

        m_module = mock.Mock(__path__=[m_path], __name__=m_package)

        m_list_names.return_value = [m_name]

        m_result = mock.Mock(Test=True)
        m_import.return_value = [(m_result, m_class)]

        result = dm.DeviceManager._get_device_module(m_module)

        m_list_names.assert_called_once_with(m_path)
        m_import.assert_called_once_with(
            [(m_name, m_class)], m_package, fetch_attribute=True
        )

        self.assertEqual([True], result)

    @mock.patch.object(dm.DeviceManager, "_get_device_module")
    def test_get_device_interfaces(self, m_get_device_module):
        """Assert get_device_interfaces called with correct module"""
        dm.DeviceManager.get_device_interfaces()

        m_get_device_module.assert_called_once_with(di)

    @mock.patch.object(dm.DeviceManager, "_get_device_module")
    def test_get_device_implementations(self, m_get_device_module):
        """Assert get_device_implementations called with correct module"""
        dm.DeviceManager.get_device_implementations()

        m_get_device_module.assert_called_once_with(dev)

    def test_get_device_map_created_once(self):
        m_map = dm.DeviceManager.get_device_map()

        self.assertEqual(m_map, dm.DeviceManager.get_device_map())

    def test_get_device_map_implementations(self):
        m_map = dm.DeviceManager.get_device_map()

        choices = {x: False for (x, y) in IMPLEMENTATION_CHOICES}
        num_choices = 0

        for key, value in m_map.items():
            num_choices += len(value)
            for imp in value:
                if imp.NAME in choices:
                    choices[imp.NAME] = True

        for x in choices:
            self.assertTrue(x)

        # This will break once an implementation supports multiple interfaces!
        self.assertEqual(num_choices, len(IMPLEMENTATION_CHOICES))

    @mock.patch.object(dm.DeviceManager, "get_device_map")
    def test_get_device_class(self, m_get_device_map):
        """Ensure class can be found for instances of DeviceObject

        This checks that instances of:
        :py:class:`radloggerpy.database.objects.device.DeviceObject` can have
        their corresponding class found by get_device_class.
        """

        m_class = mock.Mock(NAME="test")
        m_get_device_map.return_value = {
            DeviceInterfaces.SERIAL: [m_class, mock.Mock(NAME="different")]
        }

        # Create actual DeviceObject instead of mock as to not upset type
        # hinting.
        args = {
            "implementation": "test",
            "interface": INTERFACE_CHOICES[DeviceInterfaces.SERIAL],
        }
        m_obj = DeviceObject(**args)

        self.assertEqual(m_class, dm.DeviceManager.get_device_class(m_obj))

    def test_device_implementations_name(self):
        """Assert each concrete device implementation has a name"""
        implementations = dm.DeviceManager.get_device_implementations()

        for imp in implementations:
            self.assertIsNotNone(imp.NAME)

    def test_device_implementations_type(self):
        """Assert each concrete device implementation has a type"""
        implementations = dm.DeviceManager.get_device_implementations()

        for imp in implementations:
            self.assertNotEqual(imp.TYPE, DeviceTypes.UNDEFINED)
