# Copyright (C) 2019 Dantali0n
# SPDX-License-Identifier: Apache-2.0

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
