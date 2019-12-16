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

import abc
import six

from radloggerpy.cli.argument import Argument
from radloggerpy.cli.argument_helper import ArgumentHelper
from radloggerpy.device.device_manager import DeviceManager


@six.add_metaclass(abc.ABCMeta)
class DeviceAddCommand(ArgumentHelper):
    """Abstract command to add devices"""

    _arguments = None

    @property
    def arguments(self):
        if self._arguments is None:
            self._arguments = dict()
            self._arguments.update({
                'name': Argument(
                    help="Unique name to help identify this device."),
                'implementation': Argument(
                    help="The specific implementation of radiation monitor "
                         "device see documentation for supported models."),
            })
        return self._arguments

    def _add_implementations(self, device_type):
        self.arguments['implementation'].add_kwarg(
            'choices',
            [dev.NAME for dev in DeviceManager.get_device_implementations()
             if dev.TYPE == device_type]
        )
