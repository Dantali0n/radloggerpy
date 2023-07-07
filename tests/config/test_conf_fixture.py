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

from oslo_log import log

from radloggerpy import __version__
from radloggerpy import config

from tests import base

LOG = log.getLogger(__name__)
CONF = config.CONF


class TestConfFixture(base.TestCase):
    """Test conf fixture resetting config between tests"""

    def setUp(self):
        super(TestConfFixture, self).setUp()

        # store the value for the filename database option
        self.filename_opts = [i for i in config.database.DATABASE_OPTS
                              if i.name == 'filename'][0]

    def test_cfg_reset_part_one(self):
        self.assertEqual(self.filename_opts.default,
                         CONF.database.filename)
        CONF.database.filename = 'part_one'
        self.assertEqual('part_one', CONF.database.filename)

    def test_cfg_reset_part_two(self):
        self.assertEqual(self.filename_opts.default,
                         CONF.database.filename)
        CONF.database.filename = 'part_two'
        self.assertEqual('part_two', CONF.database.filename)

    def test_cfg_parse_args_one(self):
        version_default = __version__
        self.assertEqual(version_default, CONF.version)
        CONF.version = 'args_one'
        self.assertEqual('args_one', CONF.version)

    def test_cfg_parse_args_two(self):
        version_default = __version__
        self.assertEqual(version_default, CONF.version)
        CONF.version = 'args_two'
        self.assertEqual('args_two', CONF.version)
