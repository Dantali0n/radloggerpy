# -*- encoding: utf-8 -*-
# Copyright (c) 2020 Dantali0n
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

from radloggerpy.cli.v1.device import device

from radloggerpy.tests import base
from radloggerpy.types.device_interfaces import INTERFACE_CHOICES


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
            INTERFACE_CHOICES.values(), dev_command.arguments[
                '--interface'].kwargs()['choices']
        )
