# Copyright (C) 2019 Dantali0n
# SPDX-License-Identifier: Apache-2.0

import abc

from radloggerpy.cli.argument import Argument
from radloggerpy.cli.v1.device.device_helper import DeviceHelper
from radloggerpy.types.device_interfaces import INTERFACE_CHOICES


class DeviceCommand(DeviceHelper, metaclass=abc.ABCMeta):
    """Abstract command to interface with devices"""

    _arguments = None

    _implementation_key = "--implementation"

    @property
    def arguments(self):
        if self._arguments is None:
            self._arguments = dict()
            self._arguments.update(
                {
                    "--id": Argument(
                        "-i", help="Database id associated with this object", type=int
                    ),
                    "--name": Argument(
                        "-n", help="Unique name to help identify this device."
                    ),
                    "--interface": Argument(
                        "-f",
                        help="Type of interface to communicate with the "
                        "radiation monitoring device.",
                    ),
                    "--implementation": Argument(
                        "-m",
                        help="The specific implementation of radiation "
                        "monitor device. See documentation for "
                        "supported models.",
                    ),
                }
            )
        return self._arguments

    def _add_interfaces(self):
        self.arguments["--interface"].add_kwarg("choices", INTERFACE_CHOICES.values())
