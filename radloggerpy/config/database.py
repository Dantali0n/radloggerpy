# Copyright (C) 2019 Dantali0n
# SPDX-License-Identifier: Apache-2.0

from oslo_config import cfg

database = cfg.OptGroup(name="database", title="Configuration Options for database")

DATABASE_OPTS = [
    cfg.StrOpt("filename", default="radlogger.sqlite", help="Name of database file")
]


def register_opts(conf):
    conf.register_group(database)
    conf.register_opts(DATABASE_OPTS, group=database)


def list_opts():
    return [(database, DATABASE_OPTS)]
