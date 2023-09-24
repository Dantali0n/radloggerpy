# Copyright (C) 2023 Dantali0n
# SPDX-License-Identifier: Apache-2.0

import functools
import inspect
import logging
import socket
from threading import Thread
import time
from typing import Type

from tests.device.dataflow_performance.data import DummyData
from tests.device.dataflow_performance.interfaces.broker import BrokerInterface
from tests.device.dataflow_performance.interfaces.consumer import ConsumerInterface
from tests.device.dataflow_performance.interfaces.data import DataInterface
from tests.device.dataflow_performance.interfaces.device import DeviceCallable
from tests.device.dataflow_performance.interfaces.device import DeviceInterface
from tests.device.dataflow_performance.interfaces.endpoint import EndpointCallable
from tests.device.dataflow_performance.interfaces.endpoint import EndpointInterface
from tests.device.dataflow_performance.interfaces.queue import QueueInterface

from tests.base import TestCase


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# NUM_OPERATIONS: int = 2000000
NUM_OPERATIONS: int = 50000


def timing_decorator(func):
    """Use timing_decorator to measure tests end-to-end"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        end_time = time.time()
        total_time = end_time - start_time
        logger.info(
            "Method ran in %f seconds (%d operations / second)",
            total_time,
            (NUM_OPERATIONS / total_time)
        )

    return wrapper


class PerformanceTimer:

    def __init__(self):
        self.start_time: float = 0.0
        self.stop_time: float = 0.0
        self.total_time = None

    def start_timer(self):
        self.start_time = time.time()

    def stop_timer(self) -> float:
        self.stop_time = time.time()
        self.total_time = self.stop_time - self.start_time
        return self.total_time

    def get_time(self) -> float:
        if not self.total_time:
            raise RuntimeError(
                "Need to call start_timer() & stop_timer() prior to get_time()"
            )

        return self.total_time

    @staticmethod
    def get_measured_method(diff_from_current_call: int) -> str:
        return inspect.stack()[diff_from_current_call + 1][0].f_code.co_name

    @staticmethod
    def log_results(this: object, result: float, diff_from_current_call: int = 0):
        """Log the measured execution time"""
        inspect.stack()[0][0].f_code.co_name
        logger.info(
            "%s:%s Execution time: %f (%d operations / second)",
            this.__class__.__name__,
            PerformanceTimer.get_measured_method(diff_from_current_call + 1),
            result, (NUM_OPERATIONS / result)
        )


class DataFlowPerformanceTestContainer:
    """Contain DataflowPerformanceTestCase to prevent direct execution"""

    class DataflowPerformanceTestCase(TestCase):
        """Base test case for all dataflow performance evaluations"""

        def __init__(self, *args, **kwargs):
            super(TestCase, self).__init__(*args, **kwargs)
            self.timer = PerformanceTimer()

            self.broker = None
            self.consumer = None
            self.device = None
            self.endpoint = None
            self.queue = None

        def setUp(
            self,
            broker: Type[BrokerInterface],
            consumer: Type[ConsumerInterface],
            device: Type[DeviceInterface],
            endpoint: Type[EndpointInterface],
            queue: Type[QueueInterface]
        ):
            super().setUp()
            self.broker = broker
            self.consumer = consumer
            self.device = device
            self.endpoint = endpoint
            self.queue = queue

        def test_verify_queue_insert_get(self):
            """Verify data put into the queue can be retrieved"""

            queue = self.queue()

            for i in range(NUM_OPERATIONS):
                data = DummyData()
                queue.put(data)
                self.assertEqual(data, queue.get())

        def test_verify_queue_fifo(self):
            """Verify data from queue retrieved in FIFO order"""

            queue = self.queue()

            internal_data = []
            for i in range(NUM_OPERATIONS):
                data = DummyData()
                internal_data.append(data)
                queue.put(data)

            for i in range(NUM_OPERATIONS):
                self.assertEqual(internal_data[i], queue.get())

        def test_verify_queue_length(self):
            """Verify data reported by queue matches actual length"""

            queue = self.queue()

            for i in range(NUM_OPERATIONS):
                self.assertEqual(i, queue.qsize())
                queue.put(DummyData())
                self.assertEqual(i + 1, queue.qsize())

        def test_measure_queue_insertion(self):
            """Test insertion performance"""
            queue = self.queue()

            self.timer.start_timer()
            for i in range(NUM_OPERATIONS):
                queue.put(DummyData())
            result = self.timer.stop_timer()
            self.timer.log_results(self, result)

        def test_measure_queue_insert_retrieve(self):
            """Test insertion and immediate retrieval"""
            queue = self.queue()

            self.timer.start_timer()
            for i in range(NUM_OPERATIONS):
                queue.put(DummyData())
                queue.get()
            result = self.timer.stop_timer()
            self.timer.log_results(self, result)

        def test_measure_queue_fill_drain(self):
            """Fill the entire queue consecutively then drain it completely"""
            queue = self.queue()

            self.timer.start_timer()
            for i in range(NUM_OPERATIONS):
                queue.put(DummyData())

            for i in range(NUM_OPERATIONS):
                queue.get()

            result = self.timer.stop_timer()
            self.timer.log_results(self, result)

        def measure_queue_insert_thread(self, num_threads: int):
            ops_per_thread_slice = int(NUM_OPERATIONS / num_threads)
            ops_remainder = NUM_OPERATIONS % num_threads
            ops_per_thread = []
            for n in range(num_threads):
                if n == 0:
                    ops_per_thread.append(ops_per_thread_slice + ops_remainder)
                else:
                    ops_per_thread.append(ops_per_thread_slice)
            queue = self.queue()

            def insert_data(data_type: Type[DataInterface], elements: int):
                for i in range(elements):
                    queue.put(data_type())

            threads = []
            self.timer.start_timer()
            for n in range(num_threads):
                t = Thread(
                    target=insert_data, args=(DummyData, ops_per_thread[n])
                )
                threads.append(t)
                t.start()

            for t in threads:
                t.join()

            self.assertEqual(NUM_OPERATIONS, queue.qsize())

            result = self.timer.stop_timer()
            self.timer.log_results(self, result, 1)

        def test_measure_queue_insert_thread_2(self):
            self.measure_queue_insert_thread(2)

        def test_measure_queue_insert_thread_4(self):
            self.measure_queue_insert_thread(4)

        def test_measure_queue_insert_thread_8(self):
            self.measure_queue_insert_thread(8)

        def test_measure_queue_insert_thread_16(self):
            self.measure_queue_insert_thread(16)

        def test_measure_queue_insert_thread_32(self):
            self.measure_queue_insert_thread(32)

        def measure_end_to_end_one_device_one_endpoint(
            self,
            device_hook: DeviceCallable = None,
            endpoint_hook: EndpointCallable = None
        ):
            """Test end to end throughput with one device and endpoint"""

            broker = self.broker()
            endpoint = self.endpoint(hook=endpoint_hook)
            queue = self.queue()
            device = self.device(queue, DummyData, hook=device_hook)
            broker.subscribe(endpoint, "data")

            self.timer.start_timer()
            for n in range(NUM_OPERATIONS):
                device.produce()
                broker.publish(queue.get(), "data")

            result = self.timer.stop_timer()
            self.timer.log_results(self, result, 1)

        def test_measure_end_to_end_one_device_one_endpoint__no_load(self):
            self.measure_end_to_end_one_device_one_endpoint()

        def test_measure_end_to_end_one_device_one_endpoint_sleep_load(self):
            def device_hook():
                time.sleep(0.00005)

            def endpoint_hook(data: DataInterface):
                time.sleep(0.00005)

            self.measure_end_to_end_one_device_one_endpoint(
                device_hook, endpoint_hook
            )

        def test_measure_end_to_end_one_device_one_endpoint_compute_load(self):
            def device_hook():
                y = 0
                for x in range(2000):
                    y *= x / 10

            def endpoint_hook(data: DataInterface):
                y = 0
                for x in range(2000):
                    y *= x / 10

            self.measure_end_to_end_one_device_one_endpoint(
                device_hook, endpoint_hook
            )

        @staticmethod
        def udp_message(data: DataInterface = None):
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
            sock.sendto(bytes("Very Long Message 4 Test", "utf-8"), ("localhost", 9999))

        def test_measure_end_to_end_one_device_one_endpoint_udp_load(self):

            self.measure_end_to_end_one_device_one_endpoint(
                self.udp_message, self.udp_message
            )
