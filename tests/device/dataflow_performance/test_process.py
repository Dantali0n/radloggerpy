# Copyright (C) 2023 Dantali0n
# SPDX-License-Identifier: Apache-2.0

import logging
import multiprocessing
from multiprocessing import Queue

from tests.base import TestCase
from tests.device.dataflow_performance.base import NUM_OPERATIONS
from tests.device.dataflow_performance.base import PerformanceTimer


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def put(queue: Queue, operations: int):
    for i in range(operations):
        queue.put("Hello World!")


def get(queue: Queue, operations: int):
    for i in range(operations):
        queue.get()


class ProcessPerformanceTestCase(TestCase):

    def setUp(self):
        super().setUp()
        self.timer = PerformanceTimer()

    def test_process_send_receive(self):
        """Test end-to-end message passing performance"""

        multiprocessing.set_start_method('spawn')

        q = multiprocessing.Queue()

        p1 = multiprocessing.Process(
            target=put, args=(q, multiprocessing.Value('d', NUM_OPERATIONS))
        )
        p2 = multiprocessing.Process(
            target=get, args=(q, multiprocessing.Value('d', NUM_OPERATIONS))
        )

        self.timer.start_timer()
        p1.start()
        p2.start()

        p1.join()
        p2.join()
        result = self.timer.stop_timer()
        logger.info("Result: %s", result)
