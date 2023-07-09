# Copyright (C) 2021 Dantali0n
# SPDX-License-Identifier: Apache-2.0

from oslo_log import log
from radloggerpy import config

LOG = log.getLogger(__name__)
CONF = config.CONF


class RadLoggerPyException(Exception):
    """Base exception for all native RadLoggerPy exceptions

    All custom exceptions native to RadLoggerPy should implement this
    baseclass.
    """
