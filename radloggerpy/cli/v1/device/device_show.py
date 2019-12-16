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

from cliff.show import ShowOne
from sqlalchemy.orm.exc import MultipleResultsFound

from radloggerpy._i18n import _
from radloggerpy.cli.v1.device.device import DeviceCommand
from radloggerpy.database.objects.device import DeviceObject


class DeviceShow(ShowOne, DeviceCommand):
    """Command to show information about devices"""

    _arguments = None

    @property
    def arguments(self):
        if self._arguments is None:
            self._arguments = super().arguments
        return self._arguments

    def get_parser(self, program_name):
        parser = super(DeviceShow, self).get_parser(program_name)
        self._add_types()
        self._add_implementations()
        self.register_arguments(parser)
        return parser

    def take_action(self, parsed_args):
        device_obj = DeviceObject(**dict(parsed_args._get_kwargs()))

        try:
            data = DeviceObject.find(
                self.app.database_session, device_obj, False)
        except MultipleResultsFound:
            raise RuntimeWarning(_("Multiple devices found"))

        if data is None:
            raise RuntimeWarning(_("Device could not be found"))

        fields = ('id', 'name', 'type', 'implementation')
        values = (data.id, data.name, data.type, data.implementation)
        return (fields, values)
