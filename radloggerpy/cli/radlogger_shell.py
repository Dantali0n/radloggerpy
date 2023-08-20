# Copyright (C) 2019 Dantali0n
# SPDX-License-Identifier: Apache-2.0

from radloggerpy import config

from cliff import app
from cliff import commandmanager
from cliff.complete import CompleteCommand

from radloggerpy import __version__
from radloggerpy._i18n import _
from radloggerpy.common import ascii_logo
from radloggerpy.common.first_time_run import FirstTimeRun
from radloggerpy.config.config import setup_config_and_logging
from radloggerpy.database import database_manager as dm

CONF = config.CONF

FirstTimeRun.add_check_task(dm.check_database_missing, dm.create_database)


class RadLoggerShell(app.App):
    """RadLoggerPy interactive command line interface"""

    def __init__(self, **kwargs):
        super().__init__(
            description=self.__doc__.strip(),
            version=__version__,
            command_manager=commandmanager.CommandManager("radloggerpy.cli"),
            deferred_help=True,
            **kwargs
        )
        self.command_manager.add_command("complete", CompleteCommand)
        self.database_session = dm.create_session()

    def initialize_app(self, argv):
        # update configuration (sets CONF.version amongst others)
        setup_config_and_logging(argv=argv, conf=config.CONF)

        # Display logo
        self.LOG.info(ascii_logo.TEXT + ascii_logo.LOGO)

        # Perform first time initialization if required
        FirstTimeRun()

        # Display version
        self.LOG.info(_("Initializing radloggercli %s") % CONF.version)

    def prepare_to_run_command(self, cmd):
        self.LOG.debug("prepare_to_run_command %s", cmd.__class__.__name__)

    def clean_up(self, cmd, result, err):
        self.LOG.debug("clean_up %s", cmd.__class__.__name__)
        if err:
            self.LOG.debug("got an error: %s", err)

    def run(self, argv):
        try:
            super().run(argv)
        except Exception as e:
            self.LOG.error(_("Exception raised: %s"), str(e))
