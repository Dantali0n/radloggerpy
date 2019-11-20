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

from cliff import app
from cliff import commandmanager
from cliff.complete import CompleteCommand

from radloggerpy import version

from oslo_log import log

LOG = log.getLogger(__name__)


class RadLoggerShell(app.App):
    """RadLoggerPy interactive command line interface"""

    def __init__(self, **kwargs):
        super(RadLoggerShell, self).__init__(
            description=self.__doc__.strip(),
            version=version.version_string,
            command_manager=commandmanager.CommandManager(
                'radloggerpy.cli'),
            deferred_help=True,
            **kwargs
        )
        self.command_manager.add_command('complete', CompleteCommand)

    def initialize_app(self, argv):
        self.LOG.debug('initialize_app')

    def prepare_to_run_command(self, cmd):
        self.LOG.debug('prepare_to_run_command %s', cmd.__class__.__name__)

    def clean_up(self, cmd, result, err):
        self.LOG.debug('clean_up %s', cmd.__class__.__name__)
        if err:
            self.LOG.debug('got an error: %s', err)

    # def run(self, argv):
    #     try:
    #         super(RadLoggerShell, self).run(argv)
    #     except Exception as e:
    #         LOG.error(_('Exception raised: %s'), str(e))
