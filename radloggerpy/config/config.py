# -*- encoding: utf-8 -*-
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

from radloggerpy import version


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
