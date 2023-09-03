# Copyright (C) 2023 Dantali0n
# SPDX-License-Identifier: Apache-2.0
from queue import Empty

from tests.device.dataflow_performance.interfaces.consumer import ConsumerInterface
from tests.device.dataflow_performance.interfaces.data import DataInterface
from tests.device.dataflow_performance.interfaces.queue import QueueInterface


class SequentialQueue(QueueInterface):

    def __init__(self):
        super().__init__()
        self.queue = []
        self.index = 0

    def put(self, data: DataInterface):
        self.queue.append(data)

    def get(self) -> DataInterface:
        if self.qsize() <= self.index:
            raise Empty()

        data = self.queue[self.index]
        self.index += 1

        if self.index >= 100:
            self.queue = self.queue[self.index:]
            self.index = 0

        return data

    def qsize(self) -> int:
        return len(self.queue)

    def register_consumer(self, consumer: ConsumerInterface):
        raise NotImplementedError()
