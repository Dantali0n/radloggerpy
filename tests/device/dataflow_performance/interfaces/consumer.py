# Copyright (C) 2023 Dantali0n
# SPDX-License-Identifier: Apache-2.0

import abc

from tests.device.dataflow_performance.interfaces.data import DataInterface


class ConsumerInterface(abc.ABC):

    @abc.abstractmethod
    def handle(self, data: DataInterface):
        pass
