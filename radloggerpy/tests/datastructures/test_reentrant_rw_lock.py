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

import time

from oslo_log import log
from radloggerpy import config

import futurist
from futurist import waiters

from concurrent.futures import ThreadPoolExecutor

# for when we deprecate python 2.7
# from readerwriterlock import rwlock

from radloggerpy.datastructures.reentrant_rw_lock import ReentrantReadWriteLock
from radloggerpy.tests import base

LOG = log.getLogger(__name__)
CONF = config.CONF


class TestReentrantReadWriteLock(base.TestCase):

    shared_counter = 0

    # def get_read_ext(self, rrwlock):
    #     lock = rrwlock.gen_rlock()
    #     try:
    #         did_acquire = lock.acquire()
    #         if did_acquire:
    #             self.shared_counter += 1
    #         return did_acquire
    #     except Exception as e:
    #         LOG.exception(e)
    #     finally:
    #         lock.release()
    #
    # def get_write_ext(self, rrwlock):
    #     lock = rrwlock.gen_wlock()
    #     try:
    #         did_acquire = lock.acquire()
    #         if did_acquire:
    #             self.shared_counter += 1
    #         return did_acquire
    #     except Exception as e:
    #         LOG.exception(e)
    #     finally:
    #         lock.release()
    #
    # def get_read_ext_hold(self, rrwlock):
    #     lock = rrwlock.gen_rlock()
    #     try:
    #         did_acquire = lock.acquire()
    #         if did_acquire:
    #             self.shared_counter += 1
    #         return did_acquire
    #     except Exception as e:
    #         LOG.exception(e)

    def get_read_native(self, rrwlock):
        try:
            lock = rrwlock.read_acquire()
            if lock:
                self.shared_counter += 1
            return lock
        except Exception as e:
            LOG.exception(e)
        finally:
            rrwlock.read_release()

    def get_read_native_hold(self, rrwlock):
        try:
            lock = rrwlock.read_acquire()
            if lock:
                self.shared_counter += 1
            return lock
        except Exception as e:
            LOG.exception(e)

    def get_read_native_reentrant(self, rrwlock):
        try:
            rrwlock.read_acquire()
            lock = rrwlock.read_acquire()
            if lock:
                self.shared_counter += 1
            return lock
        except Exception as e:
            LOG.exception(e)
        finally:
            rrwlock.read_release()
            rrwlock.read_release()

    def get_write_native(self, rrwlock):
        try:
            lock = rrwlock.write_acquire()
            if lock:
                self.shared_counter += 1
            return lock
        except Exception as e:
            LOG.exception(e)
        finally:
            rrwlock.write_release()

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

    def test_mutual_exclusion_write_read_block(self):
        rrwlock = ReentrantReadWriteLock()
        self.assertTrue(rrwlock.write_acquire())
        self.assertFalse(rrwlock.read_acquire(False))

    def test_mutual_exclusion_concurrent_read_write_native(self):
        rrwlock = ReentrantReadWriteLock()

        self.shared_counter = 0

        futures = []
        futures.append(self._threadpool.submit(self.get_read_native, rrwlock))
        futures.append(self._threadpool.submit(self.get_write_native, rrwlock))

        results = waiters.wait_for_all(futures)
        self.assertTrue(results[0].pop().result)
        self.assertTrue(results[0].pop().result)
        self.assertEqual(2, self.shared_counter)

    def test_mutual_exclusion_concurrent_read_write_no_futurist(self):
        rrwlock = ReentrantReadWriteLock()

        self.shared_counter = 0

        executor = ThreadPoolExecutor(max_workers=2)

        futures = list()
        futures.append(executor.submit(self.get_read_native, rrwlock))
        futures.append(executor.submit(self.get_write_native, rrwlock))

        while len(futures) > 0:
            for f in futures:
                if f.done():
                    futures.remove(f)
                    self.assertTrue(f.result())
            time.sleep(1)

        self.assertEqual(2, self.shared_counter)

    def test_mutual_exclusion_concurrent_read_read(self):
        rrwlock = ReentrantReadWriteLock()

        self.shared_counter = 0

        futures = []
        futures.append(
            self._threadpool.submit(self.get_read_native_hold, rrwlock))
        futures.append(
            self._threadpool.submit(self.get_read_native_hold, rrwlock))
        results = waiters.wait_for_all(futures)

        self.assertTrue(results[0].pop().result)
        self.assertTrue(results[0].pop().result)
        self.assertEqual(2, self.shared_counter)

    def test_mutual_exclusion_concurrent_read_reentrant(self):
        rrwlock = ReentrantReadWriteLock()

        self.shared_counter = 0

        futures = []
        futures.append(
            self._threadpool.submit(self.get_read_native_reentrant, rrwlock))
        futures.append(
            self._threadpool.submit(self.get_write_native, rrwlock))
        results = waiters.wait_for_all(futures)

        self.assertTrue(results[0].pop().result)
        self.assertTrue(results[0].pop().result)
        self.assertEqual(2, self.shared_counter)

    # def test_mutual_exclusion_concurrent_read_write_ext(self):
    #     rrwlock = rwlock.RWLockRead()
    #
    #     self.shared_counter = 0
    #
    #     futures = []
    #     futures.append(self._threadpool.submit(self.get_read_ext, rrwlock))
    #     futures.append(self._threadpool.submit(self.get_write_ext, rrwlock))
    #
    #     results = waiters.wait_for_all(futures)
    #     self.assertTrue(results[0].pop().result)
    #     self.assertTrue(results[0].pop().result)
    #     self.assertEqual(2, self.shared_counter)
