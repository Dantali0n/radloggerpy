# Copyright (C) 2019 Dantali0n
# SPDX-License-Identifier: Apache-2.0

from cliff.show import ShowOne
from sqlalchemy.exc import MultipleResultsFound

from radloggerpy._i18n import _
from radloggerpy.cli.v1.device.device import DeviceCommand
from radloggerpy.database.objects.device import DeviceObject


class DeviceRemove(ShowOne, DeviceCommand):
    """Command to remove device"""

    _arguments = None

    @property
    def arguments(self):
        if self._arguments is None:
            self._arguments = super().arguments
            if "--interface" in self._arguments:
                del self._arguments["--interface"]
            if "--implementation" in self._arguments:
                del self._arguments["--implementation"]
        return self._arguments

    def get_parser(self, program_name):
        parser = super(DeviceRemove, self).get_parser(program_name)
        self.register_arguments(parser)
        return parser

    def take_action(self, parsed_args):
        args = dict(parsed_args._get_kwargs())
        device_obj = DeviceObject(**args)

        if device_obj.id is None and device_obj.name is None:
            raise RuntimeWarning(
                _("Either the id or name must be specified to " "remove a device")
            )

        try:
            data = DeviceObject.delete(self.app.database_session, device_obj, False)
        except MultipleResultsFound:
            raise RuntimeWarning(_("Multiple devices found"))

        if data is None:
            raise RuntimeWarning(_("Device could not be found"))

        fields = ("id", "name", "interface", "implementation")
        values = (data.id, data.name, data.interface, data.implementation)

        self.app.LOG.info(_("Device removed successfully"))
        return (fields, values)
