# Copyright (C) 2023 Dantali0n
# SPDX-License-Identifier: Apache-2.0

from queue import Queue

from tests.device.dataflow_performance.interfaces.consumer import ConsumerInterface
from tests.device.dataflow_performance.interfaces.data import DataInterface
from tests.device.dataflow_performance.interfaces.queue import QueueInterface


class NativeQueue(QueueInterface):

    def __init__(self):
        super().__init__()
        self.queue = Queue()

    def put(self, data: DataInterface):
        self.queue.put(data)

    def get(self) -> DataInterface:
        return self.queue.get()

    def qsize(self) -> int:
        return self.queue.qsize()

    def register_consumer(self, consumer: ConsumerInterface):
        raise NotImplementedError()
