# Copyright (C) 2019 Dantali0n
# SPDX-License-Identifier: Apache-2.0

from oslo_log import log

from radloggerpy import config

from tests import base

LOG = log.getLogger(__name__)
CONF = config.CONF


class DatabaseIntegrationBase(base.TestCase):
    def setUp(self):
        super(DatabaseIntegrationBase, self).setUp()
