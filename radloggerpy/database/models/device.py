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

from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType

from radloggerpy.database.declarative_base import base
from radloggerpy.types.device_implementations import IMPLEMENTATION_CHOICES
from radloggerpy.types.device_types import DeviceTypes


class Device(base):
    id = Column(Integer, primary_key=True)

    name = Column(String, unique=True)

    type = Column(Enum(DeviceTypes))

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
