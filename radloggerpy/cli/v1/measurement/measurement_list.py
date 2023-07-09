# Copyright (C) 2020 Dantali0n
# SPDX-License-Identifier: Apache-2.0

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

        if "device" in args or "name" in args:
            """Set device for MeasurementObject if any device params are set"""
            dev_obj = DeviceObject()
            if args["device"]:
                dev_obj.id = args["device"]
                del args["device"]
            if args["name"]:
                dev_obj.name = args["name"]
                del args["name"]
            args["device"] = dev_obj

        measure_obj = MeasurementObject(**args)

        data = MeasurementObject.find(self.app.database_session, measure_obj, True)

        if len(data) == 0:
            raise RuntimeWarning(_("No measurements found"))

        fields = ("timestamp", "device", "cpm", "μSv/h")
        values = []
        for result in data:
            value = (result.timestamp, result.device.id, result.cpm, result.svh)
            values.append(value)

        return [fields, values]
