# Copyright (C) 2023 Dantali0n
# SPDX-License-Identifier: Apache-2.0

from typing import Type

from tests.device.dataflow_performance.interfaces.data import DataInterface
from tests.device.dataflow_performance.interfaces.device import DeviceInterface
from tests.device.dataflow_performance.interfaces.queue import QueueInterface


class SequentialDevice(DeviceInterface):

    def __init__(self, queue: QueueInterface, data_type: Type[DataInterface]):
        super().__init__(queue=queue, data_type=data_type)

    def produce(self):
        self.queue.put(self.data_type())
