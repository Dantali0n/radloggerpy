# Copyright (C) 2023 Dantali0n
# SPDX-License-Identifier: Apache-2.0

import abc

from tests.device.dataflow_performance.interfaces.data import DataInterface
from tests.device.dataflow_performance.interfaces.endpoint import \
    EndpointInterface


class BrokerInterface(abc.ABC):

    @abc.abstractmethod
    def subscribe(self, endpoint: EndpointInterface, topic: any):
        pass

    @abc.abstractmethod
    def publish(self, data: DataInterface, topic: any):
        pass
