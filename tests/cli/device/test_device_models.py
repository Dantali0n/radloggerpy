# -*- encoding: utf-8 -*-
# Copyright (c) 2020 Dantali0n
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

from copy import copy
from unittest import mock

from cliff.lister import Lister

from radloggerpy.cli.v1.device import device_models

from tests import base


class TestDeviceModels(base.TestCase):
    def setUp(self):
        super(TestDeviceModels, self).setUp()

    class BaseDummy(object):
        pass

    @mock.patch.object(device_models, "DeviceManager")
    def test_take_action(self, m_dm):
        bases = copy(device_models.DeviceModels.__bases__)
        f_bases = tuple(base for base in bases if base != Lister) + (self.BaseDummy,)

        m_dm.get_device_map.return_value = {"test": [mock.Mock(NAME="value")]}

        m_base = mock.patch.object(device_models.DeviceModels, "__bases__", f_bases)
        with m_base:
            m_base.is_local = True
            t_device = device_models.DeviceModels()

            t_device.app = mock.Mock()

            t_result = t_device.take_action(None)
            self.assertEqual(
                t_result, (("interface", "implementation"), [("test", "value")])
            )

        # ensure that is_local on the patch does not modify the actual bases
        self.assertEqual(bases, device_models.DeviceModels.__bases__)
