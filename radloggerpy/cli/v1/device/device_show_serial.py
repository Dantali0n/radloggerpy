# Copyright (C) 2019 Dantali0n
# SPDX-License-Identifier: Apache-2.0

from sqlalchemy.exc import MultipleResultsFound

from radloggerpy._i18n import _
from radloggerpy.cli.argument import Argument
from radloggerpy.cli.v1.device.device_show import DeviceShow
from radloggerpy.database.objects.serial_device import SerialDeviceObject
from radloggerpy.types.device_interfaces import DeviceInterfaces
from radloggerpy.types.serial_bytesize import BYTESIZE_CHOICES
from radloggerpy.types.serial_parity import PARITY_CHOICES
from radloggerpy.types.serial_stopbit import STOPBIT_CHOICES


class DeviceShowSerial(DeviceShow):
    """Command to show information about devices"""

    _arguments = None

    @property
    def arguments(self):
        if self._arguments is None:
            # retrieve existing arguments from baseclass
            self._arguments = super().arguments
            self._arguments.update(
                {
                    "--port": Argument(
                        help="Symbolic name of the serial port to be translated "
                        "to the physical device, such as /dev/ttyUSB0 or "
                        "COM1.",
                        default=None,
                    ),
                    "--baudrate": Argument(
                        "-r",
                        default=None,
                        help="The speed at which the device sends data expressed "
                        "in symbols per second (baud), typically 9600 Bd/s.",
                    ),
                    "--bytesize": Argument(
                        "-b", default=None, type=int, choices=BYTESIZE_CHOICES.values()
                    ),
                    "--parity": Argument(
                        "-p", default=None, choices=PARITY_CHOICES.values()
                    ),
                    "---stopbits": Argument(
                        "-s", default=None, type=float, choices=STOPBIT_CHOICES.values()
                    ),
                    "--timeout": Argument("-t", default=None),
                }
            )
            # remove interface argument as serial is predefined interface type
            if "--interface" in self._arguments:
                del self._arguments["--interface"]
        return self._arguments

    def get_parser(self, program_name):
        parser = super(DeviceShow, self).get_parser(program_name)
        self._add_implementations(DeviceInterfaces.SERIAL)
        self.register_arguments(parser)
        return parser

    def take_action(self, parsed_args):
        args = dict(parsed_args._get_kwargs())
        device_obj = SerialDeviceObject(**args)

        try:
            data = SerialDeviceObject.find(self.app.database_session, device_obj, False)
        except MultipleResultsFound:
            raise RuntimeWarning(_("Multiple devices found"))

        if data is None:
            raise RuntimeWarning(_("Device could not be found"))

        fields = (
            "id",
            "name",
            "measurement type",
            "interface",
            "implementation",
            "port",
            "baudrate",
            "bytesize",
            "parity",
            "stopbits",
            "timeout",
        )
        values = (
            data.id,
            data.name,
            data.type,
            data.interface,
            data.implementation,
            data.port,
            data.baudrate,
            data.bytesize,
            data.parity,
            data.stopbits,
            data.timeout,
        )

        return (fields, values)
