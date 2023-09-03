# Copyright (C) 2023 Dantali0n
# SPDX-License-Identifier: Apache-2.0

from tests.device.dataflow_performance.interfaces.broker import BrokerInterface
from tests.device.dataflow_performance.interfaces.data import DataInterface
from tests.device.dataflow_performance.interfaces.endpoint import \
    EndpointInterface


class SequentialBroker(BrokerInterface):

    def __init__(self):
        self.topics = {}

    def subscribe(self, endpoint: EndpointInterface, topic: str):
        if topic not in self.topics:
            self.topics[topic] = []

        self.topics[topic].append(endpoint)

    def publish(self, data: DataInterface, topic: str):
        if topic not in self.topics:
            return

        for subscriber in self.topics[topic]:
            subscriber.deliver(data)
