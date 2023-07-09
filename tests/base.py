# Copyright 2010-2011 OpenStack Foundation
# Copyright (c) 2013 Hewlett-Packard Development Company, L.P.
# Copyright (C) 2023 Dantali0n
# SPDX-License-Identifier: Apache-2.0

from oslo_config import cfg
from oslo_log import log
from oslotest import base
import testscenarios

from tests import conf_fixture


CONF = cfg.CONF
try:
    log.register_options(CONF)
except cfg.ArgsAlreadyParsedError:
    pass
CONF.set_override("use_stderr", False)


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
