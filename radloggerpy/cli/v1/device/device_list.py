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

from cliff.lister import Lister

from radloggerpy._i18n import _
from radloggerpy.cli.v1.device.device import DeviceCommand
from radloggerpy.database.objects.device import DeviceObject


class DeviceList(Lister, DeviceCommand):
    """Command to show lists of devices"""

    _arguments = None

    @property
    def arguments(self):
        if self._arguments is None:
            self._arguments = super().arguments
        return self._arguments

    def get_parser(self, program_name):
        parser = super(DeviceList, self).get_parser(program_name)
        self._add_types()
        self._add_implementations()
        self.register_arguments(parser)
        return parser

    def take_action(self, parsed_args):
        args = dict(parsed_args._get_kwargs())
        device_obj = DeviceObject(**args)

        data = DeviceObject.find(
            self.app.database_session, device_obj, True)

        if len(data) == 0:
            raise RuntimeWarning(_("No devices found"))

        fields = ('id', 'name', 'type', 'implementation')
        values = []
        for result in data:
            value = (result.id, result.name, result.type,
                     result.implementation)
            values.append(value)

        return [fields, values]
