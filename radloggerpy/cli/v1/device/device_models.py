# Copyright (C) 2019 Dantali0n
# SPDX-License-Identifier: Apache-2.0

from cliff.lister import Lister

from radloggerpy.device.device_manager import DeviceManager


class DeviceModels(Lister):
    """Command to list available device interfaces and implementations"""

    def take_action(self, parsed_args):
        columns = ("interface", "implementation")

        # Convert data from device_map
        map = DeviceManager.get_device_map()
        data = []
        for key, values in map.items():
            for value in values:
                data.append((key, value.NAME))

        return (columns, data)
