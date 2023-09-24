# Copyright (C) 2023 Dantali0n
# SPDX-License-Identifier: Apache-2.0

import logging
import multiprocessing
from multiprocessing import Queue
import sys

from tests.base import TestCase
from tests.device.dataflow_performance.base import NUM_OPERATIONS
from tests.device.dataflow_performance.base import PerformanceTimer


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def put(queue: Queue, operations: multiprocessing.Value):
    # logger.info(f"Going put: {operations.value}")
    # sys.stdout.flush()
    for i in range(operations.value):
        queue.put("Hello World!")


def get(queue: Queue, operations: multiprocessing.Value):
    # logger.info(f"Going get: {operations.value}")
    # sys.stdout.flush()
    for i in range(operations.value):
        queue.get()


# def spawn_do(queue: Queue, operations: multiprocessing.Value):
#     for i in range(operations.value):
#         queue.put("Hello World")


class ProcessPerformanceTestCase(TestCase):

    def setUp(self):
        super().setUp()
        self.timer = PerformanceTimer()

    # def test_spawn_process(self):
    #     context = multiprocessing.get_context('spawn')
    #     q = context.Queue()
    #     val = context.Value('i', NUM_OPERATIONS)
    #     p = context.Process(target=spawn_do, args=(q, val))
    #     p.start()
    #     for _ in range(NUM_OPERATIONS):
    #         self.assertEqual("Hello World", q.get())
    #     p.join()
    #
    #     self.assertEqual(0, p.exitcode)

    def process_measure_queue_insert_retrieve(self, method: str, num_process: int):
        """Test end-to-end message passing performance"""

        ops_per_process_slice = int(NUM_OPERATIONS / num_process)
        ops_remainder = NUM_OPERATIONS % num_process
        ops_per_process = []
        for n in range(num_process):
            if n == 0:
                ops_per_process.append(ops_per_process_slice + ops_remainder)
            else:
                ops_per_process.append(ops_per_process_slice)

        context = multiprocessing.get_context(method)
        q = context.Queue()

        putter = []
        ops = []
        for i in range(num_process):
            ops.append(context.Value('i', ops_per_process[i]))
            putter.append(
                context.Process(
                    target=put, args=(
                        q, ops[i]
                    )
                )
            )

        getter = []
        for i in range(num_process):
            getter.append(
                context.Process(
                    target=get, args=(
                        q, ops[i]
                    )
                )
            )

        self.timer.start_timer()
        for i in range(num_process):
            putter[i].start()
            getter[i].start()

        for i in range(num_process):
            putter[i].join()
            getter[i].join()
            self.assertEqual(0, putter[i].exitcode)
            self.assertEqual(0, getter[i].exitcode)

        result = self.timer.stop_timer()
        self.timer.log_results(self, result)

    def test_process_spawn_measure_queue_insert_retrieve_1(self):
        self.process_measure_queue_insert_retrieve("spawn", 1)

    def test_process_spawn_measure_queue_insert_retrieve_2(self):
        self.process_measure_queue_insert_retrieve("spawn", 2)

    def test_process_spawn_measure_queue_insert_retrieve_4(self):
        self.process_measure_queue_insert_retrieve("spawn", 4)

    def test_process_spawn_measure_queue_insert_retrieve_8(self):
        self.process_measure_queue_insert_retrieve("spawn", 8)

    def test_process_fork_measure_queue_insert_retrieve_1(self):
        self.process_measure_queue_insert_retrieve("fork", 1)

    def test_process_fork_measure_queue_insert_retrieve_2(self):
        self.process_measure_queue_insert_retrieve("fork", 2)

    def test_process_fork_measure_queue_insert_retrieve_4(self):
        self.process_measure_queue_insert_retrieve("fork", 4)

    def test_process_fork_measure_queue_insert_retrieve_8(self):
        self.process_measure_queue_insert_retrieve("fork", 8)
