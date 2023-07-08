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

import hashlib

from oslo_log import log
from radloggerpy import config

from radloggerpy.common import ascii_logo

from tests import base

LOG = log.getLogger(__name__)
CONF = config.CONF


class TestASCIILogo(base.TestCase):
    def setUp(self):
        super(TestASCIILogo, self).setUp()
        self.m_hash = hashlib.sha384()

    def test_text_hash(self):
        m_text_hex = (
            "b55e32b9d5317638f1f1e0c0aec328a8f94ae9d867240d539ff16d"
            "43493de90c89d43553b85174309c9e0f8d62148882"
        )

        self.m_hash.update(ascii_logo.TEXT.encode("utf-8"))

        self.assertEqual(m_text_hex, self.m_hash.hexdigest())

    def test_logo_hash(self):
        m_logo_hex = (
            "e5394c5c4b95b4747cea38cd271019531418b3beec476ab6bcd0fe"
            "ada6e93cbb447be6abac5494fe7813c92982f76a88"
        )

        self.m_hash.update(ascii_logo.LOGO.encode("utf-8"))

        self.assertEqual(m_logo_hex, self.m_hash.hexdigest())
