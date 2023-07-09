# Copyright (C) 2019 Dantali0n
# SPDX-License-Identifier: Apache-2.0

from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from radloggerpy.database.declarative_base import base


class DeviceAttribute(base):
    id = Column(Integer, primary_key=True)
    base_id = Column(Integer, ForeignKey("device.id"))

    key = Column(String)
    value = Column(String)

    base_device = relationship("Device", back_populates="attributes")
