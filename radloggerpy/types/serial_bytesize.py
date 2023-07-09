# Copyright (C) 2019 Dantali0n
# SPDX-License-Identifier: Apache-2.0

from enum import Enum
from enum import unique


@unique
class SerialBytesizeTypes(Enum):
    """Enum listing all possible supported types of serial byte sizes"""

    FIVEBITS = 5
    SIXBITS = 6
    SEVENBITS = 7
    EIGHTBITS = 8


BYTESIZE_CHOICES = {
    SerialBytesizeTypes.FIVEBITS: 5,
    SerialBytesizeTypes.SIXBITS: 6,
    SerialBytesizeTypes.SEVENBITS: 7,
    SerialBytesizeTypes.EIGHTBITS: 8,
}
