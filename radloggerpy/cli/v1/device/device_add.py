# Copyright (C) 2019 Dantali0n
# SPDX-License-Identifier: Apache-2.0

import abc

from radloggerpy.cli.argument import Argument
from radloggerpy.cli.v1.device.device_helper import DeviceHelper


class DeviceAddCommand(DeviceHelper, metaclass=abc.ABCMeta):
    """Abstract command to add devices"""

    _arguments = None

    # override key as it has changed compared to baseclass
    _implementation_key = "implementation"

    @property
    def arguments(self):
        if self._arguments is None:
            self._arguments = dict()
            self._arguments.update(
                {
                    "name": Argument(help="Unique name to help identify this device."),
                    "implementation": Argument(
                        help="The specific implementation of radiation monitor "
                        "device see documentation for supported models."
                    ),
                }
            )
        return self._arguments
