# Copyright (C) 2020 Dantali0n
# SPDX-License-Identifier: Apache-2.0

from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship

from radloggerpy.database.declarative_base import base


class Measurement(base):
    id = Column(Integer, primary_key=True)
    device_id = Column(Integer, ForeignKey("device.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)

    cpm = Column(Integer, nullable=True)
    svh = Column(Float, nullable=True)

    bq = Column(Integer, nullable=True)
    cpkg = Column(Integer, nullable=True)
    gray = Column(Integer, nullable=True)

    base_device = relationship("Device", single_parent=True)
