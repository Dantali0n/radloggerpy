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

from oslo_log import log
from radloggerpy import config

from collections import OrderedDict
import futurist
import multiprocessing

from radloggerpy._i18n import _
from radloggerpy.devices import arduino_geiger_pcb as agp
from radloggerpy.types import device_types as dt


LOG = log.getLogger(__name__)
CONF = config.CONF


class DeviceManager(object):
    """Factory for device creation and management

    The following theory of operation is not finalized and alternative
    solutions are not only welcome but encouraged:

    Each device is run on the threadpool and gets scheduled and descheduled
    in accordance to the number of concurrent workers. Devices are expected
    to check for data and subsequently return to sleep upon waking up. The
    amount of time in between wake-ups should be long enough to give other
    devices time to retrieve data but short enough to have relevant timing
    data.

    Devices are expected to run in a endless loop, upon returning they will
    NOT get automatically rescheduled back into the queue of the threadpool.
    Since all devices inherit the Device super class this class will provide
    methods to store data. The storage and retrieval methods for data can
    be assumed to be thread-safe by the device.

    The polling rate of DeviceManager to retrieve data from devices depends
    on the /systems/ used to store data permanently. Some online platforms
    do not allow to specify timestamps while uploading data. This in turn
    requires a high polling rate to be able to ensure measurements get
    uploaded with accurate time information.

    """

    """Map DeviceType enum to their equivalent classes"""
    DEVICE_MAP = OrderedDict([
        (dt.DeviceTypes.arduino_geiger_pcb, agp.ArduinoGeigerPCB)
    ])

    def __init__(self):
        num_workers = CONF.devices.concurrent_worker_amount

        if num_workers == -1:
            num_workers = multiprocessing.cpu_count()
            LOG.info(_("Configured device manager for %d workers")
                     % num_workers)

        self._threadpool = futurist.GreenThreadPoolExecutor(
            max_workers=num_workers)
