# -*- encoding: utf-8 -*-
# Copyright (c) 2019 Dantali0n
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from enum import Enum
from enum import unique


@unique
class SerialParityTypes(Enum):
    """Enum listing all possible supported types of serial parity"""
    PARITY_NONE = 'N'
    PARITY_EVEN = 'E'
    PARITY_ODD = 'O'
    PARITY_MARK = 'M'
    PARITY_SPACE = 'S'


PARITY_CHOICES = {
    SerialParityTypes.PARITY_NONE: "none",
    SerialParityTypes.PARITY_ODD: "odd",
    SerialParityTypes.PARITY_EVEN: "even",
    SerialParityTypes.PARITY_MARK: "mark",
    SerialParityTypes.PARITY_SPACE: "space"
}

PARITY_CHOICES_R = {value: key for (key, value) in
                    PARITY_CHOICES.items()}
