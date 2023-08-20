# Copyright (C) 2020 Dantali0n
# SPDX-License-Identifier: Apache-2.0

from sqlalchemy import Column, Integer, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship

from radloggerpy.database.declarative_base import base


class UsbDevice(base):
    id = Column(Integer, primary_key=True)
    base_id = Column(Integer, ForeignKey("device.id"))

    vendor_id = Column(LargeBinary(length=2))
    product_id = Column(LargeBinary(length=2))

    base_device = relationship("Device", back_populates="usb", single_parent=True)
