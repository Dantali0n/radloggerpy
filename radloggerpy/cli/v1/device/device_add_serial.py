# Copyright (C) 2019 Dantali0n
# SPDX-License-Identifier: Apache-2.0

from cliff.command import Command

from radloggerpy.cli.argument import Argument
from radloggerpy.cli.v1.device.device_add import DeviceAddCommand
from radloggerpy.database.objects.serial_device import SerialDeviceObject
from radloggerpy.device.device_manager import DeviceManager as Dm
from radloggerpy.types.device_interfaces import DeviceInterfaces
from radloggerpy.types.device_interfaces import INTERFACE_CHOICES
from radloggerpy.types.serial_bytesize import BYTESIZE_CHOICES
from radloggerpy.types.serial_parity import PARITY_CHOICES
from radloggerpy.types.serial_stopbit import STOPBIT_CHOICES


class DeviceAddSerial(Command, DeviceAddCommand):
    """Command to add serial devices"""

    _arguments = None

    @property
    def arguments(self):
        if self._arguments is None:
            # retrieve existing arguments from baseclass
            self._arguments = super().arguments
            self._arguments.update(
                {
                    "port": Argument(
                        help="Symbolic name of the serial port to be translated "
                        "to the physical device, such as /dev/ttyUSB0 or "
                        "COM1."
                    ),
                    "baudrate": Argument(
                        help="The speed at which the device sends data expressed "
                        "in symbols per second (baud), typically 9600 Bd/s."
                    ),
                    "--bytesize": Argument(
                        "-b", default=8, type=int, choices=BYTESIZE_CHOICES.values()
                    ),
                    "--parity": Argument(
                        "-p", default="none", choices=PARITY_CHOICES.values()
                    ),
                    "---stopbits": Argument(
                        "-s", default=1, type=float, choices=STOPBIT_CHOICES.values()
                    ),
                    "--timeout": Argument("-t", default=None),
                }
            )
        return self._arguments

    def get_parser(self, program_name):
        parser = super(DeviceAddSerial, self).get_parser(program_name)

        # Add implementations ensures only serial interface devices are shown
        # as valid parameter.
        self._add_implementations(DeviceInterfaces.SERIAL)

        self.register_arguments(parser)
        return parser

    def take_action(self, parsed_args):
        serial_obj = SerialDeviceObject(**dict(parsed_args._get_kwargs()))

        # Set the serial attribute as string, since get_device_class expects it
        # as retrieved when constructing objects from database
        serial_obj.interface = INTERFACE_CHOICES[DeviceInterfaces.SERIAL]

        # Get the class for the implementation and use it to set type
        # TODO(Dantali0n): Catch and raise errors (if any, should not be
        #  possible due to parameter restrictions)
        implementation = Dm.get_device_class(serial_obj)
        serial_obj.type = implementation.TYPE

        return SerialDeviceObject.add(self.app.database_session, serial_obj)
