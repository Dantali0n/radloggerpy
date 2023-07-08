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

from unittest import mock

from radloggerpy.models import radiationreading

from tests import base


class TestRadiationReadingModel(base.TestCase):
    def setUp(self):
        super(TestRadiationReadingModel, self).setUp()

        self.m_radiation_reading = radiationreading.RadiationReading()

    def test_no_instance_attributes(self):
        """Test that the class has no instance variables"""

        test = radiationreading.RadiationReading()
        self.assertEqual(len(dir(radiationreading.RadiationReading)), len(dir(test)))

    def test_set_get(self):
        self.m_radiation_reading.set_cpm(24)
        self.assertEqual(24, self.m_radiation_reading.get_cpm())

    @mock.patch.object(radiationreading, "LOG")
    def test_set_invalid(self, m_log):
        """Set cpm to an invalid value and check it stays unchanged and logs"""

        self.m_radiation_reading.set_cpm(0)
        self.m_radiation_reading.set_cpm(-1)

        m_log.warning.assert_called_once()
        self.assertEqual(0, self.m_radiation_reading.get_cpm())
