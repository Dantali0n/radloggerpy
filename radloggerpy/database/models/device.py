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

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Enum
from sqlalchemy import Integer
from sqlalchemy.orm import relationship
from sqlalchemy import String
from sqlalchemy_utils import ChoiceType

from radloggerpy.database.declarative_base import base
from radloggerpy.types.device_implementations import IMPLEMENTATION_CHOICES
from radloggerpy.types.device_interfaces import DeviceInterfaces
from radloggerpy.types.device_types import DeviceTypes


class Device(base):
    id = Column(Integer, primary_key=True)

    name = Column(String, unique=True)

    enabled = Column(Boolean, default=True, nullable=False)

    type = Column(Enum(DeviceTypes))
    """Type stores redundant information that could be extrapolated from
        implementation, however, storing type allows for more efficient
        queries."""

    interface = Column(Enum(DeviceInterfaces))
    """Interface stores redundant information that could be extrapolated
        implementation, however, storing interface allows for more efficient
        queries."""

    implementation = Column(ChoiceType(IMPLEMENTATION_CHOICES))

    attributes = relationship(
        "DeviceAttribute", back_populates="base_device",
        cascade="all, delete-orphan")
    ethernet = relationship(
        "EthernetDevice", back_populates="base_device", single_parent=True,
        cascade="all, delete-orphan")
    serial = relationship(
        "SerialDevice", back_populates="base_device", single_parent=True,
        cascade="all, delete-orphan")
    usb = relationship(
        "UsbDevice", back_populates="base_device", single_parent=True,
        cascade="all, delete-orphan")
