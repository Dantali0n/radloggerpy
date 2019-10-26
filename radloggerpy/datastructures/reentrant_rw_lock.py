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

    def read_acquire(self, blocking=True):
        """Acquire a reentrant read lock

        Allows reentrant and multiple concurrent readers

        :param blocking: If the method is allowed to block or not
        :return: True if the lock was acquired false otherwise
        """
        int_lock = False
        try:
            if self._read_lock.acquire(blocking):
                int_lock = True
                while self._wants_write:
                    if not blocking:
                        return False
                    with self._condition:
                        self._condition.wait()
                self._num_readers += 1
                return True
            return False
        finally:
            if int_lock:
                self._read_lock.release()

    def read_release(self):
        """Release reentrant read lock

        Does not validate that a lock was previously acquired by the same
        caller.
        """
        int_lock = False
        try:
            if self._read_lock.acquire():
                int_lock = True
                self._num_readers -= 1
                with self._condition:
                    self._condition.notifyAll()
        finally:
            if int_lock:
                self._read_lock.release()

    def write_acquire(self, blocking=True):
        """Acquire a reentrant write lock

        Allows reentrant writers.

        :param blocking: If the method is allowed to block or not
        :return: True if the lock was acquired false otherwise
        """
        int_lock = False
        try:
            if self._write_lock.acquire(blocking):
                int_lock = True
                while self._num_readers > 0 or self._wants_write:
                    if not blocking:
                        return False
                    with self._condition:
                        self._condition.wait()
                self._wants_write = True
                return True
            return False
        finally:
            if int_lock:
                self._write_lock.release()

    def write_release(self):
        int_lock = False
        try:
            if self._write_lock.acquire():
                int_lock = True
                self._wants_write = False
                with self._condition:
                    self._condition.notifyAll()
        finally:
            if int_lock:
                self._write_lock.release()