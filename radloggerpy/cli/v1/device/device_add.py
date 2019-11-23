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

from cliff.command import Command


class DeviceAdd(Command):
    """Command to add devices"""

    def get_parser(self, program_name):
        parser = super(DeviceAdd, self).get_parser(program_name)
        parser.add_argument('id', nargs='?', default=None)
        return parser

    def take_action(self, parsed_args):
        self.app.LOG.info(self.app.database_session)
        columns = ["action"]
        data = [parsed_args.action]
        return (columns, data)
