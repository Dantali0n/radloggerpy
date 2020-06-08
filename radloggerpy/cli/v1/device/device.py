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
from radloggerpy.cli.v1.device.device_helper import DeviceHelper
from radloggerpy.types.device_types import TYPE_CHOICES


@six.add_metaclass(abc.ABCMeta)
class DeviceCommand(DeviceHelper):
    """Abstract command to interface with devices"""

    _arguments = None

    @property
    def arguments(self):
        if self._arguments is None:
            self._arguments = dict()
            self._arguments.update({
                '--id': Argument(
                    '-i', help="Database id associated with this object",
                    type=int),
                '--name': Argument(
                    '-n', help="Unique name to help identify this device."),
                '--type': Argument(
                    '-t', help="Type of interface to communicate with the "
                               "radiation monitoring device."),
                '--implementation': Argument(
                    '-m', help="The specific implementation of radiation "
                               "monitor device. See documentation for "
                               "supported models."),
            })
        return self._arguments

    def _add_types(self):
        self.arguments['--type'].add_kwarg(
            'choices',
            TYPE_CHOICES.values()
        )
