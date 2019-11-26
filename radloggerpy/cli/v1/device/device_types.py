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

from radloggerpy.device.device_manager import DeviceManager


class DeviceTypes(Lister):
    """Command to list available device types and implementations"""

    def take_action(self, parsed_args):
        columns = ("type", 'implementation')

        # Convert data from device_map
        map = DeviceManager.get_device_map()
        data = []
        for key, values in map.items():
            for value in values:
                data.append((key, value.NAME))

        return (columns, data)
