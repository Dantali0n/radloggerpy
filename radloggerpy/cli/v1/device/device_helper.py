# Copyright (C) 2020 Dantali0n
# SPDX-License-Identifier: Apache-2.0

import abc

from radloggerpy._i18n import _
from radloggerpy.cli.argument_helper import ArgumentHelper
from radloggerpy.device.device_manager import DeviceManager


class DeviceHelper(ArgumentHelper, metaclass=abc.ABCMeta):
    """Abstract helper for shared device interface"""

    # Should be overridden by child classes
    _implementation_key = ""

    def _add_implementations(self, device_interface=None):
        if not self._implementation_key:
            raise NotImplementedError(
                _(
                    "_implementation_key variable is not overridden in "
                    "%s child class" % self.__class__.__name__
                )
            )

        if device_interface is None:
            choices = [dev.NAME for dev in DeviceManager.get_device_implementations()]
        else:
            choices = [
                dev.NAME
                for dev in DeviceManager.get_device_implementations()
                if dev.INTERFACE == device_interface
            ]

        self.arguments[self._implementation_key].add_kwarg("choices", choices)
