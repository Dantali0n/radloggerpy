# Copyright (C) 2023 Dantali0n
# SPDX-License-Identifier: Apache-2.0

import abc
from typing import Callable
from typing import Optional

from tests.device.dataflow_performance.interfaces.data import DataInterface

EndpointCallable = Callable[[DataInterface], None]


class EndpointInterface(abc.ABC):

    def __init__(self, hook: Optional[EndpointCallable] = None):
        if hook:
            self.hook = hook
        else:
            self.hook = lambda x: {}

    @abc.abstractmethod
    def deliver(self, data: DataInterface):
        self.hook(data)
