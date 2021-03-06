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

import time
from unittest import mock

from radloggerpy.models import timestamp
from radloggerpy.tests import base


class TestTimeStampModel(base.TestCase):

    def setUp(self):
        super(TestTimeStampModel, self).setUp()

        self.m_timestamp = timestamp.TimeStamp()

    def test_no_instance_attributes(self):
        """Test that the class has no instance variables"""

        self.assertEqual(
            len(dir(timestamp.TimeStamp)), len(dir(self.m_timestamp)))

    @mock.patch.object(time, 'time')
    def test_update_get(self, m_time):
        m_time.return_value = 0

        self.m_timestamp.update_timestamp()
        self.assertEqual(0, self.m_timestamp.get_timestamp())

    def test_set_get(self):
        self.m_timestamp.set_timestamp(1500)
        self.assertEqual(1500, self.m_timestamp.get_timestamp())
