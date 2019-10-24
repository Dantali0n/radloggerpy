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

from oslo_log import log
from radloggerpy import config

from threading import Condition
from threading import RLock

LOG = log.getLogger(__name__)
CONF = config.CONF


class ReentrantReadWriteLock(object):
    """Dual lock wrapper to facilitate reentrant read / write lock pattern

    Implements second reader-writer problem (writer preference).

    Once python 2,7 is officially deprecated use this instead:
    https://pypi.org/project/readerwriterlock/

    """

    def __init__(self):

        self._read_lock = RLock()
        self._write_lock = RLock()
        self._condition = Condition()
        self._num_readers = 0
        self._wants_write = False

    def read_acquire(self, blocking=True, timeout=-1):
        waitout = None if timeout == -1 else timeout
        first_it = True
        try:
            if self._read_lock.acquire(blocking, timeout):
                while self._wants_write:
                    if not blocking or not first_it:
                        return False
                    with self._condition:
                        self._condition.wait(waitout)
                    first_it = False
                self._num_readers += 1
                return True
            return False
        finally:
            self._read_lock.release()

    def read_release(self):
        try:
            if self._read_lock.acquire():
                self._num_readers -= 1
                if self._num_readers == 0:
                    with self._condition:
                        self._condition.notifyAll()
        finally:
            self._read_lock.release()

    def write_acquire(self, blocking=True, timeout=-1):
        waitout = None if timeout == -1 else timeout
        first_it = True
        try:
            if self._write_lock.acquire(blocking, timeout):
                while self._num_readers > 0 or self._wants_write:
                    if not blocking or not first_it:
                        return False
                    with self._condition:
                        self._condition.wait(waitout)
                    first_it = False
                self._wants_write = True
                return True
            return False
        finally:
            self._write_lock.release()

    def write_release(self):
        try:
            if self._write_lock.acquire():
                self._wants_write = False
                with self._condition:
                    self._condition.notifyAll()
        finally:
            self._write_lock.release()
