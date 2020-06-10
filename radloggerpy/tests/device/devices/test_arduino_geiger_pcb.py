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

from oslo_log import log
from radloggerpy import config

from radloggerpy.device.devices import arduino_geiger_pcb as agpcb
from radloggerpy.tests import base

LOG = log.getLogger(__name__)
CONF = config.CONF


class TestArduinoGeigerPcb(base.TestCase):

    def setUp(self):
        super(TestArduinoGeigerPcb, self).setUp()

    def test_name(self):
        m_device = agpcb.ArduinoGeigerPcb()
        self.assertEqual(agpcb.ArduinoGeigerPcb.NAME, m_device.NAME)

    @mock.patch.object(agpcb, 'time')
    def test_run(self, m_time):
        m_time.sleep.side_effect = [InterruptedError]
        m_device = agpcb.ArduinoGeigerPcb()

        self.assertRaises(InterruptedError, m_device.run)
