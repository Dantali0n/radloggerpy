# Copyright (C) 2019 Dantali0n
# SPDX-License-Identifier: Apache-2.0

from oslo_config import cfg

from radloggerpy.config import database
from radloggerpy.config import devices

CONF = cfg.CONF

devices.register_opts(CONF)
database.register_opts(CONF)
