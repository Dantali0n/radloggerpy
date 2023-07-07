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

from radloggerpy import radloggerpy

from tests import base


class TestRadloggerpy(base.TestCase):

    def setUp(self):
        super().setUp()

        self.p_configurator = mock.patch.object(
            radloggerpy, 'configurator')
        self.m_configurator = self.p_configurator.start()
        self.addCleanup(self.p_configurator.stop)

        self.p_database = mock.patch.object(
            radloggerpy, 'database_manager')
        self.m_database = self.p_database.start()
        self.addCleanup(self.p_database.stop)

        self.p_first_run = mock.patch.object(
            radloggerpy, 'FirstTimeRun')
        self.m_first_run = self.p_first_run.start()
        self.addCleanup(self.p_first_run.stop)

        # self.p_serial = mock.patch.object(
        #     radloggerpy.serial, 'Serial')
        # self.m_serial = self.p_serial.start()
        # self.addCleanup(self.p_serial.stop)

    # @mock.patch.object(radloggerpy.time, 'sleep')
    # @mock.patch.object(radloggerpy, 'MeasurementObject')
    # def test_run_main(self, m_measurement, m_sleep):
    #     m_sleep.side_effect = InterruptedError
    #
    #     m_serial_instance = mock.Mock()
    #     m_serial_instance.inWaiting.side_effect = [11, 1, 0]
    #     m_serial_instance.read.side_effect = [
    #         "14".encode('utf-8'),
    #         '\n'.encode('utf-8')
    #     ]
    #
    #     self.m_serial.return_value = m_serial_instance
    #
    #     self.assertRaises(InterruptedError, radloggerpy.main)
    #     m_sleep.assert_called_once()
    #     m_measurement.add.assert_called_once()
    #
    # def test_run_main_err_no_device(self):
    #     m_execption = SerialException
    #     m_execption.errno = errno.EACCES
    #     self.m_serial.side_effect = m_execption
    #
    #     radloggerpy.main()
    #
    #     self.m_first_run.assert_called_once()
    #     self.m_database.close_lingering_sessions.assert_called_once()
    #     self.m_configurator.setup_config_and_logging.assert_called_once()
    #
    # def test_run_main_err_access(self):
    #     m_execption = SerialException
    #     m_execption.errno = errno.ENOENT
    #     self.m_serial.side_effect = m_execption
    #
    #     radloggerpy.main()
    #
    #     self.m_first_run.assert_called_once()
    #     self.m_database.close_lingering_sessions.assert_called_once()
    #     self.m_configurator.setup_config_and_logging.assert_called_once()
    #
    # def test_run_main_err_arbitrary(self):
    #     m_execption = SerialException
    #     m_execption.errno = errno.EFAULT
    #     self.m_serial.side_effect = m_execption
    #
    #     radloggerpy.main()
    #
    #     self.m_first_run.assert_called_once()
    #     self.m_database.close_lingering_sessions.assert_called_once()
    #     self.m_configurator.setup_config_and_logging.assert_called_once()
