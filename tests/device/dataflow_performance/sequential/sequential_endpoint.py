# Copyright (C) 2023 Dantali0n
# SPDX-License-Identifier: Apache-2.0

from tests.device.dataflow_performance.interfaces.data import DataInterface
from tests.device.dataflow_performance.interfaces.endpoint import EndpointInterface


class SequentialEndpoint(EndpointInterface):

    def deliver(self, data: DataInterface):
        super().deliver(data)
