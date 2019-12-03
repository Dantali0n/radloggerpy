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

from cliff.command import Command
import serial

from radloggerpy.cli.argument import Argument
from radloggerpy.cli.v1.device.device_add import DeviceAdd
from radloggerpy.types.device_types import DeviceTypes


class DeviceAddSerial(Command, DeviceAdd):
    """Command to add serial devices"""

    _arguments = None

    @property
    def arguments(self):
        if self._arguments is None:
            self._arguments = super().arguments
            self._arguments.update({
                'port': Argument(),
                'baudrate': Argument(),
                '--bytesize': Argument('-b', default=8, type=int),
                '--parity': Argument('-p', default=serial.PARITY_NONE),
                '---stopbits': Argument('-s', default=1, type=int),
                '--timeout': Argument('-t', default=None),
            })
        return self._arguments

    def get_parser(self, program_name):
        parser = super(DeviceAddSerial, self).get_parser(program_name)
        self._add_implementations(DeviceTypes.SERIAL)
        self.register_arguments(parser)
        return parser

    def take_action(self, parsed_args):
        pass
