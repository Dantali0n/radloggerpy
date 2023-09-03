# Copyright (C) 2023 Dantali0n
# SPDX-License-Identifier: Apache-2.0

import abc

from typing import Callable
from typing import Optional
from typing import Type

from tests.device.dataflow_performance.interfaces.data import DataInterface
from tests.device.dataflow_performance.interfaces.queue import QueueInterface

DeviceCallable = Callable[[], None]


class DeviceInterface(abc.ABC):

    def __init__(
        self,
        queue: QueueInterface,
        data_type: Type[DataInterface],
        hook: Optional[DeviceCallable] = None
    ):
        self.queue = queue
        self.data_type = data_type

        if hook:
            self.hook = hook
        else:
            self.hook = lambda: {}

    @abc.abstractmethod
    def produce(self):
        self.hook()
