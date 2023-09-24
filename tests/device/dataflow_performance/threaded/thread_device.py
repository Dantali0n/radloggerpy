# Copyright (C) 2023 Dantali0n
# SPDX-License-Identifier: Apache-2.0

from concurrent.futures import ThreadPoolExecutor
from typing import Optional
from typing import Type

from typing_extensions import override

from tests.device.dataflow_performance.interfaces.data import DataInterface
from tests.device.dataflow_performance.interfaces.device import DeviceCallable
from tests.device.dataflow_performance.interfaces.device import DeviceInterface
from tests.device.dataflow_performance.interfaces.queue import QueueInterface


class ThreadDevice(DeviceInterface):

    def __init__(
        self,
        queue: QueueInterface,
        data_type: Type[DataInterface],
        hook: Optional[DeviceCallable] = None
    ):
        super().__init__(queue=queue, data_type=data_type, hook=hook)
        self.thread = ThreadPoolExecutor(max_workers=1)

    def _produce(self):
        super().produce()
        self.queue.put(self.data_type())

    @override
    def produce(self):
        self.thread.submit(self._produce)
