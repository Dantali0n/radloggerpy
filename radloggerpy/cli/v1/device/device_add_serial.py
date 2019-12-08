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

from radloggerpy.cli.argument import Argument
from radloggerpy.cli.v1.device.device_add import DeviceAdd
from radloggerpy.database.objects.serial_device import SerialDeviceObject
from radloggerpy.types.device_types import DeviceTypes
from radloggerpy.types.serial_bytesize_types import SerialBytesizeTypes
from radloggerpy.types.serial_parity_types import SerialParityTypes
from radloggerpy.types.serial_stopbit_types import SerialStopbitTypes


class DeviceAddSerial(Command, DeviceAdd):
    """Command to add serial devices"""

    BYTESIZE_CHOICES = {
        5: SerialBytesizeTypes.FIVEBITS,
        6: SerialBytesizeTypes.SIXBITS,
        7: SerialBytesizeTypes.SEVENBITS,
        8: SerialBytesizeTypes.EIGHTBITS,
    }

    PARITY_CHOICES = {
        "none": SerialParityTypes.PARITY_NONE,
        "odd": SerialParityTypes.PARITY_ODD,
        "even": SerialParityTypes.PARITY_EVEN,
        "mark": SerialParityTypes.PARITY_MARK,
        "space": SerialParityTypes.PARITY_SPACE
    }

    STOPBIT_CHOICES = {
        1: SerialStopbitTypes.STOPBITS_ONE,
        1.5: SerialStopbitTypes.STOPBITS_ONE_POINT_FIVE,
        2: SerialStopbitTypes.STOPBITS_TWO,
    }

    _arguments = None

    @property
    def arguments(self):
        if self._arguments is None:
            self._arguments = super().arguments
            self._arguments.update({
                'port': Argument(
                    help="Symbolic name of the serial port to be translated "
                         "to the physical device, such as /dev/ttyUSB0 or "
                         "COM1."),
                'baudrate': Argument(
                    help="The speed at which the device sends data expressed "
                         "in symbols per second (baud), typically 9600 Bd/s."),
                '--bytesize': Argument(
                    '-b', default=8, type=int,
                    choices=self.BYTESIZE_CHOICES),
                '--parity': Argument(
                    '-p', default="none",
                    choices=self.PARITY_CHOICES),
                '---stopbits': Argument(
                    '-s', default=1, type=float,
                    choices=self.STOPBIT_CHOICES),
                '--timeout': Argument('-t', default=None),
            })
        return self._arguments

    def get_parser(self, program_name):
        parser = super(DeviceAddSerial, self).get_parser(program_name)
        self._add_implementations(DeviceTypes.SERIAL)
        self.register_arguments(parser)
        return parser

    def take_action(self, parsed_args):
        import pdb
        pdb.set_trace()
        test_obj = SerialDeviceObject(**dict(parsed_args._get_kwargs()))
        test_obj.type = DeviceTypes.SERIAL
