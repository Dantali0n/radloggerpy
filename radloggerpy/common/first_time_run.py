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

import inspect

from oslo_log import log
from radloggerpy import config

from radloggerpy._i18n import _

LOG = log.getLogger(__name__)
CONF = config.CONF


class FirstTimeRun(object):
    """Handles service wide first time initialization

    FirstTimeRun should not be instantiated until all checks and tasks have
    been added. The FirstTimeRun will perform checks and if necessary perform
    all tasks upon construction.

    Individual tasks should do basic checks before performing that task as it
    could otherwise potentially re-initialize. This is due to a limitation in
    FirstTimeRun were there is no correlation between tasks and checks. The
    result is that even though it can be determined initialization is in
    order it can not be determined due to which check.

    Tasks and checks can be added globally by typing:
        FirstTimeRun.add_task(task)
        FirstTimeRun.add_check(check)

    If stronger coupling between tasks and checks is required use:
        FirstTimeRun.add_check_task(check, task)

    Since these can only be defined after the definition of class methods it
    might be necessary to add the statements to the bottom of the file. Take
    into account that these global statements are only executed if the file in
    which the reside is included in the main file.

    Alternatively, a separate file can be created to handle all these
    registrations. This has as advance that all registrations can be observed
    in one overview. Additionally, it will provide cleaner imports since only
    the declaring files has all the combinations of imports. This has the
    potential to solve circular dependencies.

    Finally, if unused imports are undesired all the registrations can be
    performed in the main file.
    """

    class CheckTask(object):
        """Wrapper for associative check and task pair"""

        def __init__(self, check, task):
            self.check = check
            self.task = task

        task = None
        check = None

    # All checks that have associated tasks.
    _check_tasks = list()

    # All calls that will be made if first time init is required.
    _tasks = list()

    # All checks to be performed to determine if initialization is required.
    _checks = list()

    def __init__(self):
        """Run all checks and if required all initialization tasks"""

        if self._run_checks():
            LOG.info(_("Performing first time initialization"))
            self._run_tasks()

        self._run_check_tasks()

    def _run_check_tasks(self):
        """Run each of the checks and tasks as a pair"""
        for check_task in self._check_tasks:
            try:
                if check_task.check():
                    check_task.task()
            except Exception as e:
                LOG.error(_("Encountered error during execution of "
                            "CheckTask: %s") % e)

    def _run_tasks(self):
        """Will try to execute all calls from the internal list"""

        for task in self._tasks:
            try:
                task()
                LOG.info(_("Ran task: %s") % task)
            except Exception as e:
                LOG.error(_("Encountered error during first time"
                            "initialization with task: %s") % e)

    def _run_checks(self, all_to_init=False):
        """Run all checks from the internal list

        :param all_to_init: True if all checks are required to init False if
                            one check is sufficient
        :return True if first time init should be run False otherwise
        """

        # store return values for all checks
        values = list()

        for check in self._checks:
            try:
                values.append(check())
            except Exception as e:
                LOG.error(_("Encountered error while performing check for"
                            "first time init: %s") % e)

        has_true = False
        for v in values:
            if v:
                has_true = True
            if v and not all_to_init:
                return True
            elif not v and all_to_init:
                return False
        return has_true

    @staticmethod
    def _validate_check_task(obj):
        """Validate the object as much as possible

        Has the limitation that it does not verify check() return type
        to be boolean.
        """
        return inspect.ismethod(obj) or inspect.isfunction(obj)

    @staticmethod
    def add_check_task(check, task):
        if not FirstTimeRun._validate_check_task(check):
            LOG.warning(_("Check %s was not of type method") % check)
            return
        if not FirstTimeRun._validate_check_task(task):
            LOG.warning(_("Task %s was not of type method") % task)
            return
        FirstTimeRun._check_tasks.append(FirstTimeRun.CheckTask(check, task))

    @staticmethod
    def add_task(task):
        if FirstTimeRun._validate_check_task(task):
            FirstTimeRun._tasks.append(task)
        else:
            LOG.warning(_("Task %s was not of type method") % task)

    @staticmethod
    def add_check(check):
        if FirstTimeRun._validate_check_task(check):
            FirstTimeRun._checks.append(check)
        else:
            LOG.warning(_("Check %s was not of type method") % check)
