# Copyright 2010 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# Copyright (C) 2023 Dantali0n
# SPDX-License-Identifier: Apache-2.0

from oslo_config import cfg
from oslo_log import _options
from oslo_log import log

from radloggerpy import __package_folder__ as package_name
from radloggerpy import __version__
from radloggerpy._i18n import _
from radloggerpy import config


LOG = log.getLogger(__name__)
CONF = config.CONF

"""Handles service like methods such as setting the correct log levels and
parsing command line arguments."""

_DEFAULT_LOG_LEVELS = [
    "sqlalchemy=WARN",
    "stevedore=INFO",
    "iso8601=WARN",
    "requests=WARN",
]


def setup_config_and_logging(argv=(), conf=cfg.CONF):
    """register logging config options and parse commandline arguments"""
    log.register_options(conf)

    has_config = parse_config_args(argv)
    # Set log levels for external libraries
    cfg.set_defaults(_options.log_opts, default_log_levels=_DEFAULT_LOG_LEVELS)
    log.setup(conf, package_name)

    if not has_config:
        LOG.warning(
            _("Failed to find config file looked in %s") % cfg._get_config_dirs(
                project=package_name
            )
        )

    # Write all configuration options and values to log
    conf.log_opt_values(LOG, log.DEBUG)


def parse_config_args(
    argv, default_config_files=None, default_config_dirs=None
):
    """Load information into config and allow program arguments to override"""

    default_config_files = default_config_files or cfg.find_config_files(
        project=package_name
    )
    default_config_dirs = default_config_dirs or cfg.find_config_dirs(
        project=package_name
    )

    cfg.CONF(
        argv[1:],
        project=package_name,
        version=__version__,
        default_config_dirs=default_config_dirs,
        default_config_files=default_config_files,
    )

    if not default_config_files and not default_config_dirs:
        return False

    return True


def list_opts():
    """Required method by opts for oslo-config-generator"""
    return []
