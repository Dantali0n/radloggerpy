# Copyright (C) 2020 Dantali0n
# SPDX-License-Identifier: Apache-2.0

from radloggerpy.cli.v1.device import device
from radloggerpy.types.device_interfaces import INTERFACE_CHOICES

from tests import base


class TestDeviceCommand(base.TestCase):
    class DevCommandExp(device.DeviceCommand):
        _arguments = None

        @property
        def arguments(self):
            if self._arguments is None:
                self._arguments = super().arguments
            return self._arguments

    def setUp(self):
        super(TestDeviceCommand, self).setUp()

    def test_add_interfaces(self):
        dev_command = TestDeviceCommand.DevCommandExp()

        dev_command._add_interfaces()

        self.assertItemsEqual(
            INTERFACE_CHOICES.values(),
            dev_command.arguments["--interface"].kwargs()["choices"],
        )
