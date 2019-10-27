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

import sys
import mock

from oslo_log import log
from radloggerpy import config

from radloggerpy.config import config as configurator
from radloggerpy.tests import base

LOG = log.getLogger(__name__)
CONF = config.CONF


class TestConfig(base.TestCase):

    def setUp(self):
        super(TestConfig, self).setUp()

    @mock.patch.object(log, 'register_options')
    def test_setup_config_and_logging(self, m_log):
        configurator.setup_config_and_logging(sys.argv, CONF)

        m_log.assert_called_once_with(CONF)

    def test_has_list_opts(self):
        """Test that radloggerpy.config.config.py contains list_opts method"""
        self.assertEqual([], configurator.list_opts())
