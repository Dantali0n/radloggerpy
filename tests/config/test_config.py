# Copyright (C) 2019 Dantali0n
# SPDX-License-Identifier: Apache-2.0

import sys

from unittest import mock

from oslo_log import log
from radloggerpy import config

from radloggerpy.config import config as configurator

from tests import base

LOG = log.getLogger(__name__)
CONF = config.CONF


class TestConfig(base.TestCase):
    def setUp(self):
        super(TestConfig, self).setUp()

    @mock.patch.object(log, "register_options")
    def test_setup_config_and_logging(self, m_log):
        configurator.setup_config_and_logging(sys.argv, CONF)

        m_log.assert_called_once_with(CONF)

    def test_has_list_opts(self):
        """Test that radloggerpy.config.config.py contains list_opts method"""
        self.assertEqual([], configurator.list_opts())
