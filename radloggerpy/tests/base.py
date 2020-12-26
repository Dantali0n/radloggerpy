# Copyright 2010-2011 OpenStack Foundation
# Copyright (c) 2013 Hewlett-Packard Development Company, L.P.
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

from oslo_config import cfg
from oslo_log import log
from oslotest import base
import testscenarios

from radloggerpy.tests import conf_fixture


CONF = cfg.CONF
try:
    log.register_options(CONF)
except cfg.ArgsAlreadyParsedError:
    pass
CONF.set_override('use_stderr', False)


class BaseTestCase(testscenarios.WithScenarios, base.BaseTestCase):
    """Test base class."""

    def setUp(self):
        super().setUp()

        # Use this fixture if class variables are changed so they get patched
        # back to the default value afterwards. This fixture also works for
        # ensuring singletons are patched back to default state.
        #
        # self.p_example = mock.patch.object(
        #     file, 'Class',
        #     new=file.Class)
        # self.m_example = self.p_example.start()
        # self.addCleanup(self.p_example.stop)
        #
        # This binds methods from the fixture to their respective class
        # has to be done for every method but only for python 2.7 so we can
        # almost get rid of this.
        # self.m_example.get_method = self.m_example.__get__(
        #   self.m_example, file.Class)

        self.addCleanup(cfg.CONF.reset)


class TestCase(BaseTestCase):
    """Test case base class for all unit tests."""

    def setUp(self):
        super().setUp()
        self.useFixture(conf_fixture.ConfReloadFixture())
        # self.useFixture(conf_fixture.ConfFixture(cfg.CONF))
