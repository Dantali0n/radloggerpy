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

from sqlalchemy import Column, Integer, ForeignKey, String, Enum
from sqlalchemy.orm import relationship

from radloggerpy.database.declarative_base import base
from radloggerpy.types.serial_bytesize import SerialBytesizeTypes
from radloggerpy.types.serial_parity import SerialParityTypes
from radloggerpy.types.serial_stopbit import SerialStopbitTypes


class SerialDevice(base):
    id = Column(Integer(), primary_key=True)
    base_id = Column(Integer, ForeignKey('device.id'))

    port = Column(String, unique=True)
    baudrate = Column(Integer())
    bytesize = Column(Enum(SerialBytesizeTypes))
    parity = Column(Enum(SerialParityTypes))
    stopbits = Column(Enum(SerialStopbitTypes))
    timeout = Column(Integer())

    base_device = relationship(
        "Device", back_populates="serial")
