# Copyright (C) 2019 Dantali0n
# SPDX-License-Identifier: Apache-2.0

from oslo_log import log
from radloggerpy import config

from radloggerpy._i18n import _
from radloggerpy.models import timestamp

LOG = log.getLogger(__name__)
CONF = config.CONF


class RadiationReading(timestamp.TimeStamp):
    _cpm = 0

    def __init__(self):
        super().__init__()

    def set_cpm(self, cpm: int):
        """Set the counts per minute to the new value

        :param cpm: Counts per minute
        :type cpm: int
        """

        if cpm < 0:
            LOG.warning(_("RadiationReading can not have negative cpm"))
            return

        self._cpm = cpm

    def get_cpm(self) -> int:
        """Get the current counts per minute

        :return: The current internal counts per minute
        :rtype: int
        """
        return self._cpm
