# Copyright (C) 2023 Dantali0n
# SPDX-License-Identifier: Apache-2.0

from concurrent.futures import ThreadPoolExecutor
from typing import Optional

from typing_extensions import override

from tests.device.dataflow_performance.interfaces.data import DataInterface
from tests.device.dataflow_performance.interfaces.endpoint import EndpointCallable
from tests.device.dataflow_performance.interfaces.endpoint import EndpointInterface


class ThreadEndpoint(EndpointInterface):

    def __init__(self, hook: Optional[EndpointCallable] = None):
        super().__init__(hook)
        self.thread = ThreadPoolExecutor(max_workers=1)

    def _deliver(self, data: DataInterface):
        super().deliver(data)

    @override
    def deliver(self, data: DataInterface):
        self.thread.submit(self._deliver, data=data)
