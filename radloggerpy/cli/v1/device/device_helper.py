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

import abc

from radloggerpy.cli.argument_helper import ArgumentHelper
from radloggerpy.device.device_manager import DeviceManager


class DeviceHelper(ArgumentHelper, metaclass=abc.ABCMeta):
    """Abstract helper for shared device interface"""

    # Should be overridden by child classes
    _implementation_key = ''

    def _add_implementations(self, device_interface=None):

        if device_interface is None:
            choices = [dev.NAME for dev in
                       DeviceManager.get_device_implementations()]
        else:
            choices = [dev.NAME for dev in
                       DeviceManager.get_device_implementations()
                       if dev.INTERFACE == device_interface]

        self.arguments[self._implementation_key].add_kwarg(
            'choices', choices
        )
