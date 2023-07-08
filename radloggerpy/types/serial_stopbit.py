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
