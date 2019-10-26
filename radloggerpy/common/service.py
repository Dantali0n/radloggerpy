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

from oslo_config import cfg
from oslo_log import _options
from oslo_log import log

from radloggerpy import config
from radloggerpy.config import config as configurator

LOG = log.getLogger(__name__)
CONF = config.CONF

"""Handles service like methods such as setting the correct log levels and
parsing command line arguments."""

_DEFAULT_LOG_LEVELS = ['sqlalchemy=WARN', 'stevedore=INFO', 'iso8601=WARN',
                       'requests=WARN']


def prepare_service(argv=(), conf=cfg.CONF):
    """"""
    log.register_options(conf)

    configurator.parse_args(argv)
    cfg.set_defaults(_options.log_opts,
                     default_log_levels=_DEFAULT_LOG_LEVELS)
    log.setup(conf, 'radloggerpy')
    conf.log_opt_values(LOG, log.DEBUG)
