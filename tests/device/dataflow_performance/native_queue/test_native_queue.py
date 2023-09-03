# Copyright (C) 2023 Dantali0n
# SPDX-License-Identifier: Apache-2.0

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
