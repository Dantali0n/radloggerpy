# Copyright (C) 2019 Dantali0n
# SPDX-License-Identifier: Apache-2.0

from enum import Enum
from enum import unique


@unique
class SerialStopbitTypes(Enum):
    """Enum listing all possible supported types of serial stopbits"""

    STOPBITS_ONE = 1
    STOPBITS_ONE_POINT_FIVE = 1.5
    STOPBITS_TWO = 2


STOPBIT_CHOICES = {
    SerialStopbitTypes.STOPBITS_ONE: 1,
    SerialStopbitTypes.STOPBITS_ONE_POINT_FIVE: 1.5,
    SerialStopbitTypes.STOPBITS_TWO: 2,
}
