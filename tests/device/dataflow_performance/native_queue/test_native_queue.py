# Copyright (C) 2023 Dantali0n
# SPDX-License-Identifier: Apache-2.0

import unittest

from tests.device.dataflow_performance.base import DataFlowPerformanceTestContainer
from tests.device.dataflow_performance.native_queue.native_queue import NativeQueue


class NativeQueueDataflowPerformance(
    DataFlowPerformanceTestContainer.DataflowPerformanceTestCase
):

    def setUp(self):
        super().setUp(
            broker=None,
            consumer=None,
            device=None,
            endpoint=None,
            queue=NativeQueue
        )

    @unittest.skip
    def test_measure_end_to_end_one_device_one_endpoint(self):
        pass

    @unittest.skip
    def test_measure_end_to_end_one_device_one_endpoint__no_load(self):
        pass

    @unittest.skip
    def test_measure_end_to_end_one_device_one_endpoint_sleep_load(self):
        pass
