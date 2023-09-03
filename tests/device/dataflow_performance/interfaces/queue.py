# Copyright (C) 2023 Dantali0n
# SPDX-License-Identifier: Apache-2.0

import abc

from tests.device.dataflow_performance.interfaces.consumer import \
    ConsumerInterface
from tests.device.dataflow_performance.interfaces.data import DataInterface


class QueueInterface(abc.ABC):

    @abc.abstractmethod
    def put(self, data: DataInterface):
        pass

    @abc.abstractmethod
    def get(self) -> DataInterface:
        pass

    @abc.abstractmethod
    def qsize(self) -> int:
        pass

    @abc.abstractmethod
    def register_consumer(self, consumer: ConsumerInterface):
        pass
