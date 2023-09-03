# Copyright (C) 2023 Dantali0n
# SPDX-License-Identifier: Apache-2.0

import time

from tests.device.dataflow_performance.interfaces.data import DataInterface


class DummyData(DataInterface):
    """Data container that does nothing and has no members"""

    def __init__(self):
        super().__init__()


class TimestampData(DataInterface):
    """Data container that keeps track of when it was created

    Can be used to measure end-to-end latency
    """

    def __init__(self):
        super().__init__()
        self.start_time = time.time()
