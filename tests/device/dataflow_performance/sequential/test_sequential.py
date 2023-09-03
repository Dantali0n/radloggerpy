# Copyright (C) 2023 Dantali0n
# SPDX-License-Identifier: Apache-2.0

# import unittest


from tests.device.dataflow_performance.base import \
    DataFlowPerformanceTestContainer
from tests.device.dataflow_performance.sequential.sequential_broker import \
    SequentialBroker
from tests.device.dataflow_performance.sequential.sequential_device import \
    SequentialDevice
from tests.device.dataflow_performance.sequential.sequential_endpoint import \
    SequentialEndpoint
from tests.device.dataflow_performance.sequential.sequential_queue import \
    SequentialQueue


class SequentialDataflowPerformance(
    DataFlowPerformanceTestContainer.DataflowPerformanceTestCase
):

    def setUp(self):
        super().setUp(
            broker=SequentialBroker,
            consumer=None,
            device=SequentialDevice,
            endpoint=SequentialEndpoint,
            queue=SequentialQueue
        )

    # @unittest.skip
    # def test_queue_fifo(self):
    #     pass
