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
from radloggerpy.cli.v1.measurement.measurement import MeasurementCommand
from radloggerpy.database.objects.device import DeviceObject
from radloggerpy.database.objects.measurement import MeasurementObject


class MeasurementList(Lister, MeasurementCommand):
    """Command to show lists of measurements"""

    _arguments = None

    @property
    def arguments(self):
        if self._arguments is None:
            self._arguments = super().arguments
        return self._arguments

    def get_parser(self, program_name):
        parser = super(MeasurementList, self).get_parser(program_name)
        self.register_arguments(parser)
        return parser

    def take_action(self, parsed_args):
        args = dict(parsed_args._get_kwargs())

        if args['device'] or args['name']:
            """Set device for MeasurementObject if any device params are set"""
            dev_obj = DeviceObject()
            if args['device']:
                dev_obj.id = args['device']
                del args['device']
            if args['name']:
                dev_obj.name = args['name']
                del args['name']
            args['device'] = dev_obj

        measure_obj = MeasurementObject(**args)

        data = MeasurementObject.find(
            self.app.database_session, measure_obj, True)

        if len(data) == 0:
            raise RuntimeWarning(_("No measurements found"))

        fields = ('timestamp', 'device', 'cpm', 'μSv/h')
        values = []
        for result in data:
            value = (result.timestamp, result.device.id, result.cpm,
                     result.svh)
            values.append(value)

        return [fields, values]
