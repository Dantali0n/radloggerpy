# Copyright (C) 2019 Dantali0n
# SPDX-License-Identifier: Apache-2.0

from enum import Enum
from enum import unique


@unique
class AccountTypes(Enum):
    """Enum listing all possible supported types of accounts"""

    RADMON = 1
    GMCMAP = 2
