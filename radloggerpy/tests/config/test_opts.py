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

import inspect
from unittest import mock

from oslo_config import cfg
from oslo_log import log
from radloggerpy import config

from radloggerpy.common import dynamic_import as di
from radloggerpy.config import opts
from radloggerpy.tests import base

LOG = log.getLogger(__name__)
CONF = config.CONF


class TestConfOpts(base.TestCase):
    """Test opts file to generate configuration samples"""

    def setUp(self):
        super(TestConfOpts, self).setUp()

    def test_module_names_complete(self):
        """Test that all config files are property included in __init__.py"""

        # opts and cfg should not be included in init even though they are
        # modules
        remove = ['opts', 'cfg']

        # get all attributes of the config directory
        path = config.__path__[0]
        names = dir(config)
        modules = list()

        # for every attribute that is a module add it to modules
        for name in names:
            if inspect.ismodule(getattr(config, name, None)):
                modules.append(name)

        # remove the not to be included modules
        for r in remove:
            modules.remove(r)

        # ensure that opts._list_module_names() gets all modules properly
        self.assertEqual(modules, di.list_module_names(path, remove))

    def test_module_import(self):
        """Assert correct import of config modules based on string name"""

        path = 'radloggerpy.config'

        self.assertEqual(
            [config.devices],
            di.import_modules(['devices'], path, opts.LIST_OPTS_FUNC_NAME))

    class FakeOpts(object):
        """Simulate options module since list_opts won't distinguish"""
        fgroup = cfg.OptGroup(name='example_group',
                              title='Example')

        fopts = [cfg.IntOpt('example_opts')]

        @staticmethod
        def list_opts():
            return [(TestConfOpts.FakeOpts.fgroup,
                     TestConfOpts.FakeOpts.fopts)]

    @mock.patch.object(opts, 'import_modules')
    def test_list_opts(self, m_modules):
        """Test that with the FakeOpts the expected available config options"""

        m_modules.return_value = [self.FakeOpts]

        self.assertEqual([(self.FakeOpts.fgroup, self.FakeOpts.fopts)],
                         opts.list_opts())
