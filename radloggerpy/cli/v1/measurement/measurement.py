# Copyright (C) 2020 Dantali0n
# SPDX-License-Identifier: Apache-2.0

import abc

from radloggerpy.cli.argument import Argument
from radloggerpy.cli.argument_helper import ArgumentHelper


class MeasurementCommand(ArgumentHelper, metaclass=abc.ABCMeta):
    """Abstract command to interface with measurements"""

    _arguments = None

    @property
    def arguments(self):
        if self._arguments is None:
            self._arguments = dict()
            self._arguments.update(
                {
                    "--device": Argument(
                        "-d", type=int, help="Device id for associated " "measurements"
                    ),
                    "--name": Argument(
                        "-n", help="Device name for associated " "measurements"
                    ),
                }
            )
        return self._arguments
