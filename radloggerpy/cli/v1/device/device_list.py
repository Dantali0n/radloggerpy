# Copyright (C) 2019 Dantali0n
# SPDX-License-Identifier: Apache-2.0

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
        self._add_interfaces()
        self._add_implementations()
        self.register_arguments(parser)
        return parser

    def take_action(self, parsed_args):
        args = dict(parsed_args._get_kwargs())
        device_obj = DeviceObject(**args)

        data = DeviceObject.find(self.app.database_session, device_obj, True)

        if len(data) == 0:
            raise RuntimeWarning(_("No devices found"))

        fields = (
            "id",
            "enabled",
            "name",
            "measurement type",
            "interface",
            "implementation",
        )
        values = []
        for result in data:
            value = (
                result.id,
                result.enabled,
                result.name,
                result.type,
                result.interface,
                result.implementation,
            )
            values.append(value)

        return [fields, values]
