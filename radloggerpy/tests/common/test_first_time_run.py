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

import mock

from oslo_log import log
from radloggerpy import config

from radloggerpy.common import first_time_run
from radloggerpy.common.first_time_run import FirstTimeRun
from radloggerpy.tests import base

LOG = log.getLogger(__name__)
CONF = config.CONF


class TestFirstTimeRun(base.TestCase):

    def setUp(self):
        super(TestFirstTimeRun, self).setUp()

        self.p_ftr = mock.patch.object(
            FirstTimeRun, '_tasks',
            new=list())
        self.m_tasks = self.p_ftr.start()
        self.addCleanup(self.p_ftr.stop)

        self.p_ftr = mock.patch.object(
            FirstTimeRun, '_checks',
            new=list())
        self.m_checks = self.p_ftr.start()
        self.addCleanup(self.p_ftr.stop)

    @staticmethod
    def fake_check_true():
        return True

    @staticmethod
    def fake_check_false():
        return False

    @staticmethod
    def fake_task():
        pass

    def test_add_check(self):
        FirstTimeRun.add_check(self.fake_check_true)

        self.assertEqual(1, len(FirstTimeRun._checks))

    def test_add_check_fake(self):
        FirstTimeRun.add_check(True)

        self.assertEqual(0, len(FirstTimeRun._checks))

    def test_add_task(self):
        FirstTimeRun.add_task(self.fake_task)

        self.assertEqual(1, len(FirstTimeRun._tasks))

    def test_add_task_fake(self):
        FirstTimeRun.add_task(True)

        self.assertEqual(0, len(FirstTimeRun._tasks))

    @mock.patch.object(first_time_run, 'LOG')
    def test_run_checks_error(self, m_log):
        m_run = FirstTimeRun()
        m_run._checks.append(True)

        self.assertFalse(m_run._run_checks())
        m_log.error.assert_called_once()

    def test_run_checks_false(self):
        m_run = FirstTimeRun()
        m_run.add_check(self.fake_check_false)

        self.assertFalse(m_run._run_checks())

    def test_run_checks_true(self):
        m_run = FirstTimeRun()
        m_run.add_check(self.fake_check_true)

        self.assertTrue(m_run._run_checks())

    def test_run_checks_all_false(self):
        m_run = FirstTimeRun()
        m_run.add_check(self.fake_check_false)
        m_run.add_check(self.fake_check_true)

        self.assertFalse(m_run._run_checks(all_to_init=True))

    def test_run_checks_all_true(self):
        m_run = FirstTimeRun()
        m_run.add_check(self.fake_check_true)
        m_run.add_check(self.fake_check_true)

        self.assertTrue(m_run._run_checks(all_to_init=True))

    def test_run_tasks(self):
        # Crate a mocked method
        m_method = mock.Mock()
        m_run = FirstTimeRun()

        m_run.add_task(self.fake_task)
        # Force mocked method into the tasks list
        m_run._tasks.append(m_method)

        m_run._run_tasks()

        m_method.assert_called_once()

    @mock.patch.object(first_time_run, 'LOG')
    def test_run_tasks_error(self, m_log):
        # Crate a mocked method
        m_method = mock.Mock()
        m_method.side_effect = Exception("Whoops")
        m_run = FirstTimeRun()

        m_run.add_task(self.fake_task)
        # Force mocked method into the tasks list
        m_run._tasks.append(m_method)

        m_run._run_tasks()

        m_method.assert_called_once()
        m_log.error.assert_called_once()

    def test_constructor(self):
        m_method = mock.Mock()

        self.assertEqual(0, len(FirstTimeRun._tasks))
        self.assertEqual(0, len(FirstTimeRun._checks))

        FirstTimeRun.add_check(self.fake_check_true)
        FirstTimeRun.add_check(self.fake_check_false)
        FirstTimeRun.add_task(self.fake_task())
        FirstTimeRun._tasks.append(m_method)

        construct = FirstTimeRun()

        m_method.assert_called_once()

