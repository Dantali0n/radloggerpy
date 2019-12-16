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

from radloggerpy import config

from cliff import app
from cliff import commandmanager
from cliff.complete import CompleteCommand

from radloggerpy._i18n import _
from radloggerpy.common import ascii_logo
from radloggerpy.common.first_time_run import FirstTimeRun
from radloggerpy.config.config import parse_args
from radloggerpy.database import database_manager as dm
from radloggerpy import version

CONF = config.CONF

FirstTimeRun.add_check_task(
    dm.check_database_missing, dm.create_database)


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
        self.database_session = dm.create_session()

    def initialize_app(self, argv):
        # update configuration (sets CONF.version amongst others)
        parse_args(argv=())

        # Display logo
        self.LOG.info(ascii_logo.TEXT + ascii_logo.LOGO)

        # Perform first time initialization if required
        FirstTimeRun()

        # Display version
        self.LOG.info(_('Initializing radloggercli %s') % CONF.version)

    def prepare_to_run_command(self, cmd):
        self.LOG.debug('prepare_to_run_command %s', cmd.__class__.__name__)

    def clean_up(self, cmd, result, err):
        self.LOG.debug('clean_up %s', cmd.__class__.__name__)
        if err:
            self.LOG.debug('got an error: %s', err)

    def run(self, argv):
        try:
            super(RadLoggerShell, self).run(argv)
        except Exception as e:
            self.LOG.error(_('Exception raised: %s'), str(e))
