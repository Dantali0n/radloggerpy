# Copyright (C) 2019 Dantali0n
# SPDX-License-Identifier: Apache-2.0

from enum import Enum
from enum import unique


@unique
class SerialParityTypes(Enum):
    """Enum listing all possible supported types of serial parity"""

    PARITY_NONE = "N"
    PARITY_EVEN = "E"
    PARITY_ODD = "O"
    PARITY_MARK = "M"
    PARITY_SPACE = "S"


PARITY_CHOICES = {
    SerialParityTypes.PARITY_NONE: "none",
    SerialParityTypes.PARITY_ODD: "odd",
    SerialParityTypes.PARITY_EVEN: "even",
    SerialParityTypes.PARITY_MARK: "mark",
    SerialParityTypes.PARITY_SPACE: "space",
}

PARITY_CHOICES_R = {value: key for (key, value) in PARITY_CHOICES.items()}
