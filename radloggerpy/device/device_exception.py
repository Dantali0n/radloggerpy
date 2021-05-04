# Copyright (c) 2021 Dantali0n
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

from oslo_log import log
from radloggerpy import config

from radloggerpy.common.exception import RadLoggerPyException

LOG = log.getLogger(__name__)
CONF = config.CONF


class DeviceException(RadLoggerPyException):
    """Exception to be used by devices indicating handled exceptions.

    Used by devices to halt the execution of that device while informing
    DeviceManager that the exception has already been handled / logged etc.
    """
