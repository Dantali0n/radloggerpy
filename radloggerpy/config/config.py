# Copyright 2010 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# Copyright 2012 Red Hat, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from oslo_config import cfg
from oslo_log import _options
from oslo_log import log

from radloggerpy import config
from radloggerpy import version

LOG = log.getLogger(__name__)
CONF = config.CONF

"""Handles service like methods such as setting the correct log levels and
parsing command line arguments."""

_DEFAULT_LOG_LEVELS = ['sqlalchemy=WARN', 'stevedore=INFO', 'iso8601=WARN',
                       'requests=WARN']


def setup_config_and_logging(argv=(), conf=cfg.CONF):
    """register logging config options and parse commandline arguments"""
    log.register_options(conf)

    parse_args(argv)
    # Set log levels for external libraries
    cfg.set_defaults(_options.log_opts,
                     default_log_levels=_DEFAULT_LOG_LEVELS)
    log.setup(conf, 'radloggerpy')
    # Write all configuration options and values to log
    conf.log_opt_values(LOG, log.DEBUG)


def parse_args(argv, default_config_files=None, default_config_dirs=None):
    """Load information into config and allow program arguments to override"""
    default_config_files = (default_config_files or
                            cfg.find_config_files(project='RadLoggerPy'))
    default_config_dirs = (default_config_dirs or
                           cfg.find_config_dirs(project='RadLoggerPy'))
    cfg.CONF(argv[1:],
             project='RadLoggerPy',
             version=version.version_info.release_string(),
             default_config_dirs=default_config_dirs,
             default_config_files=default_config_files)


def list_opts():
    """Required method by opts for oslo-config-generator"""
    return []
