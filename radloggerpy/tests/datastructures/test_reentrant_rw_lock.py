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

import futurist
# from futurist import waiters

from radloggerpy.datastructures.reentrant_rw_lock import ReentrantReadWriteLock

from radloggerpy.tests import base


class TestReentrantReadWriteLock(base.TestCase):

    def get_read(self, rrwlock):
        return rrwlock.read_acquire()

    def get_write(self, rrwlock):
        return rrwlock.write_acquire()

    def setUp(self):
        super(TestReentrantReadWriteLock, self).setUp()
        self._threadpool = futurist.GreenThreadPoolExecutor(max_workers=4)

    def test_read_write(self):
        rrwlock = ReentrantReadWriteLock()
        self.assertTrue(rrwlock.read_acquire())
        rrwlock.read_release()
        self.assertTrue(rrwlock.write_acquire())

    def test_write_read(self):
        rrwlock = ReentrantReadWriteLock()
        self.assertTrue(rrwlock.write_acquire())
        rrwlock.write_release()
        self.assertTrue(rrwlock.read_acquire())

    def test_read_read(self):
        rrwlock = ReentrantReadWriteLock()
        self.assertTrue(rrwlock.read_acquire())
        self.assertTrue(rrwlock.read_acquire())

    def test_mutual_exclusion_read_write_block(self):
        rrwlock = ReentrantReadWriteLock()
        self.assertTrue(rrwlock.read_acquire())
        self.assertFalse(rrwlock.write_acquire(False))

    def test_mutual_exclusion_read_write_timeout(self):
        rrwlock = ReentrantReadWriteLock()
        self.assertTrue(rrwlock.read_acquire())
        self.assertFalse(rrwlock.write_acquire(timeout=1))

    def test_mutual_exclusion_write_read_block(self):
        rrwlock = ReentrantReadWriteLock()
        self.assertTrue(rrwlock.write_acquire())
        self.assertFalse(rrwlock.read_acquire(False))

    def test_mutual_exclusion_write_read_timeout(self):
        rrwlock = ReentrantReadWriteLock()
        self.assertTrue(rrwlock.write_acquire())
        self.assertFalse(rrwlock.read_acquire(timeout=1))

    # def test_mutual_exclusion_concurrent_read_write(self):
    #     rrwlock = ReentrantReadWriteLock()
    #
    #     # Attempt to concurrent read and writes
    #     futures = []
    #     futures.append(self._threadpool.submit(self.get_read, rrwlock))
    #     futures.append(self._threadpool.submit(self.get_write, rrwlock))
    #
    #     # Get the results and verify only one of the calls succeeded
    #     # assert that the other call is still pending
    #     results = waiters.wait_for_any([futures[0]])
    #     self.assertTrue(results[0].pop().result)
    #     # .assertEqual(1, len(results[1]))
    #
    # def test_mutual_exclusion_concurrent_read_read(self):
    #     rrwlock = ReentrantReadWriteLock()
    #
    #     futures = []
    #     futures.append(self._threadpool.submit(self.get_read, rrwlock))
    #     futures.append(self._threadpool.submit(self.get_read, rrwlock))
    #     results = waiters.wait_for_all(futures)
    #
    #     self.assertTrue(results[0].pop().result)
    #     self.assertTrue(results[0].pop().result)
