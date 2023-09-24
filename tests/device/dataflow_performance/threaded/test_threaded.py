# Copyright (C) 2023 Dantali0n
# SPDX-License-Identifier: Apache-2.0

import unittest

from typing_extensions import override

from tests.device.dataflow_performance.base import DataFlowPerformanceTestContainer
from tests.device.dataflow_performance.threaded.thread_device import ThreadDevice
from tests.device.dataflow_performance.threaded.thread_endpoint import ThreadEndpoint
from tests.device.dataflow_performance.threaded.threadsafe_broker import ThreadSafeBroker
from tests.device.dataflow_performance.threaded.threadsafe_queue import ThreadSafeQueue


class ThreadedDataflowPerformance(
    DataFlowPerformanceTestContainer.DataflowPerformanceTestCase
):

    def setUp(self):
        super().setUp(
            broker=ThreadSafeBroker,
            consumer=None,
            device=ThreadDevice,
            endpoint=ThreadEndpoint,
            queue=ThreadSafeQueue
        )
