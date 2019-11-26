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

from radloggerpy.cli.argument import Argument
from radloggerpy.cli.argument_helper import ArgumentHelper


class DeviceAdd(Command, ArgumentHelper):
    """Command to add devices"""

    arguments = {
        'name': Argument(default="henk"),
        '--type': Argument('-t', required=True),
    }

    def get_parser(self, program_name):
        parser = super(DeviceAdd, self).get_parser(program_name)
        self.arguments['name'].add_kwarg('choices', {'henk', 'tank'})
        self.register_arguments(parser)
        return parser

    def take_action(self, parsed_args):
        pass

    # return self._verify_required_arguments(parsed_args)

    # def _verify_required_arguments(self, parsed_args):
    #     for key, value in self._ARGUMENTS.items():
    #         if value.required is True and not hasattr(parsed_args,  key):
    #             self.app.LOG.error(_("Missing required attribute: %s") % key)
    #             return False
    #     return True
