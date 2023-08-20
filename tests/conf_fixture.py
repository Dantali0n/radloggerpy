# Copyright 2010 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

from oslo_config import cfg
from oslo_config import fixture as conf_fixture

from radloggerpy.config import config


class ConfFixture(conf_fixture.Config):
    """Fixture to manage conf settings."""

    def setUp(self):
        super().setUp()
        config.parse_config_args([], default_config_files=[])


class ConfReloadFixture(ConfFixture):
    """Fixture to manage reloads of conf settings."""

    def __init__(self, conf=cfg.CONF):
        self.conf = conf
        self._original_parse_cli_opts = self.conf._parse_cli_opts

    def _fake_parser(self, *args, **kw):
        return cfg.ConfigOpts._parse_cli_opts(self.conf, [])

    def _restore_parser(self):
        self.conf._parse_cli_opts = self._original_parse_cli_opts

    def setUp(self):
        super().setUp()
        self.conf._parse_cli_opts = self._fake_parser
        self.addCleanup(self._restore_parser)
