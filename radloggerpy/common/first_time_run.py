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
    """Handles service wide first time initialization"""

    # all calls that will be made if first time init is required
    _tasks = list()

    # all checks to be performed to determine if initialization is required
    _checks = list()

    def __init__(self):
        """Run all checks and if required all initialization tasks"""

        if self._run_checks():
            LOG.info(_("Performing first time initialization"))
            self._run_tasks()

    def _run_tasks(self):
        """Will try to execute all calls from the internal list"""

        for task in self._tasks:
            try:
                task()
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
        values = list

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
    def add_task(task):
        if inspect.ismethod(task):
            FirstTimeRun._tasks.append(task)
        else:
            LOG.warning(_("Task %s was not of type method") % task)
