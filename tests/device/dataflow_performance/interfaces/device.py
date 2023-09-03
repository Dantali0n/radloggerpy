# Copyright (C) 2023 Dantali0n
# SPDX-License-Identifier: Apache-2.0

import abc
from typing import Type

from tests.device.dataflow_performance.interfaces.data import DataInterface
from tests.device.dataflow_performance.interfaces.queue import QueueInterface


class DeviceInterface(abc.ABC):

    def __init__(self, queue: QueueInterface, data_type: Type[DataInterface]):
        self.queue = queue
        self.data_type = data_type

    @abc.abstractmethod
    def produce(self):
        pass
