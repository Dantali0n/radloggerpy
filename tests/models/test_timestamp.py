# Copyright (C) 2019 Dantali0n
# SPDX-License-Identifier: Apache-2.0

import time
from unittest import mock

from radloggerpy.models import timestamp

from tests import base


class TestTimeStampModel(base.TestCase):
    def setUp(self):
        super(TestTimeStampModel, self).setUp()

        self.m_timestamp = timestamp.TimeStamp()

    def test_no_instance_attributes(self):
        """Test that the class has no instance variables"""

        self.assertEqual(len(dir(timestamp.TimeStamp)), len(dir(self.m_timestamp)))

    @mock.patch.object(time, "time")
    def test_update_get(self, m_time):
        m_time.return_value = 0

        self.m_timestamp.update_timestamp()
        self.assertEqual(0, self.m_timestamp.get_timestamp())

    def test_set_get(self):
        self.m_timestamp.set_timestamp(1500)
        self.assertEqual(1500, self.m_timestamp.get_timestamp())
