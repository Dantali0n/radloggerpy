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

devices = cfg.OptGroup(
    name="devices", title="Configuration Options for measuring devices"
)

DEVICES_OPTS = [
    cfg.IntOpt(
        "concurrent_worker_amount",
        default=-1,
        min=-1,
        help="Number of concurrent workers to use in addition to the "
        "main thread. Setting this to -1 means the value will be"
        "based on nproc which returns the number of available"
        "concurrent threads (not cores).",
    ),
    cfg.IntOpt(
        "minimal_polling_delay",
        default=1000,
        min=0,
        help="Minimum time in between a device pulling for data, going "
        "to sleep and pulling for data again. Value is expressed "
        "in milliseconds (1/1000 second).",
    ),
    cfg.BoolOpt(
        "restart_on_error",
        default=True,
        help="Should the device manager restart devices upon " "encountering an error.",
    ),
    cfg.IntOpt(
        "min_restart_delay",
        default=30,
        min=-1,
        help="Minimal amount of time in seconds before a device should"
        "be restarted after it has entered error state. -1 for no"
        "minimal delay.",
    ),
    cfg.IntOpt(
        "max_consecutive_restart",
        default=3,
        min=-1,
        help="Maximum amount of consecutive device restarts without "
        "the device returning any measurements. -1 for unlimited."
        "This option is ignored when restart_on_error is false.",
    ),
]


def register_opts(conf):
    conf.register_group(devices)
    conf.register_opts(DEVICES_OPTS, group=devices)


def list_opts():
    return [(devices, DEVICES_OPTS)]
