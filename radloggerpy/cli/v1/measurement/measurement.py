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
            self._arguments.update({
                '--device': Argument(
                    '-d', type=int, help="Device id for associated "
                                         "measurements"),
                '--name': Argument(
                    '-n', help="Device name for associated "
                               "measurements")
            })
        return self._arguments
