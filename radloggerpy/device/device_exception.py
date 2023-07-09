# Copyright (C) 2021 Dantali0n
# SPDX-License-Identifier: Apache-2.0

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
