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

from cliff.lister import Lister

from radloggerpy._i18n import _
from radloggerpy.cli.argument import Argument
from radloggerpy.cli.v1.device.device import DeviceCommand
from radloggerpy.database.objects.serial_device import SerialDeviceObject
from radloggerpy.types.device_interfaces import DeviceInterfaces
from radloggerpy.types.serial_bytesize import BYTESIZE_CHOICES
from radloggerpy.types.serial_parity import PARITY_CHOICES
from radloggerpy.types.serial_stopbit import STOPBIT_CHOICES


class DeviceListSerial(Lister, DeviceCommand):
    """Command to show lists of serial devices"""

    _arguments = None

    @property
    def arguments(self):
        if self._arguments is None:
            self._arguments = super().arguments
            self._arguments.update({
                '--port': Argument(
                    help="Symbolic name of the serial port to be translated "
                         "to the physical device, such as /dev/ttyUSB0 or "
                         "COM1.",
                    default=None),
                '--baudrate': Argument(
                    '-r', default=None,
                    help="The speed at which the device sends data expressed "
                         "in symbols per second (baud), typically 9600 Bd/s."
                    ),
                '--bytesize': Argument(
                    '-b', default=None, type=int,
                    choices=BYTESIZE_CHOICES.values()),
                '--parity': Argument(
                    '-p', default=None,
                    choices=PARITY_CHOICES.values()),
                '---stopbits': Argument(
                    '-s', default=None, type=float,
                    choices=STOPBIT_CHOICES.values()),
                '--timeout': Argument('-t', default=None),
            })
            if '--interface' in self._arguments:
                del self._arguments['--interface']
        return self._arguments

    def get_parser(self, program_name):
        parser = super(DeviceListSerial, self).get_parser(program_name)
        self._add_implementations(DeviceInterfaces.SERIAL)
        self.register_arguments(parser)
        return parser

    def take_action(self, parsed_args):
        args = dict(parsed_args._get_kwargs())
        device_obj = SerialDeviceObject(**args)

        data = SerialDeviceObject.find(
            self.app.database_session, device_obj, True)

        if len(data) == 0:
            raise RuntimeWarning(_("No devices found"))

        fields = (
            'id', 'enabled', 'name', 'measurement type', 'interface',
            'implementation', 'port', 'baudrate', 'bytesize', 'parity',
            'stopbits', 'timeout')
        values = []
        for result in data:
            value = (result.id, result.enabled, result.name, result.type,
                     result.interface, result.implementation, result.port,
                     result.baudrate, result.bytesize, result.parity,
                     result.stopbits, result.timeout)
            values.append(value)

        return [fields, values]
