# Copyright (C) 2019 Dantali0n
# SPDX-License-Identifier: Apache-2.0

from sqlalchemy import Column, Integer, ForeignKey, String, Enum
from sqlalchemy.orm import relationship

from radloggerpy.database.declarative_base import base
from radloggerpy.types.serial_bytesize import SerialBytesizeTypes
from radloggerpy.types.serial_parity import SerialParityTypes
from radloggerpy.types.serial_stopbit import SerialStopbitTypes


class SerialDevice(base):
    id = Column(Integer(), primary_key=True)
    base_id = Column(Integer, ForeignKey("device.id"))

    port = Column(String, unique=True)
    baudrate = Column(Integer())
    bytesize = Column(Enum(SerialBytesizeTypes))
    parity = Column(Enum(SerialParityTypes))
    stopbits = Column(Enum(SerialStopbitTypes))
    timeout = Column(Integer())

    base_device = relationship("Device", back_populates="serial", single_parent=True)
