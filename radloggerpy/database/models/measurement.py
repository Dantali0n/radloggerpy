# -*- encoding: utf-8 -*-
# Copyright (c) 2020 Dantali0n
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

from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship

from radloggerpy.database.declarative_base import base


class Measurement(base):
    id = Column(Integer, primary_key=True)
    device_id = Column(Integer, ForeignKey('device.id'))
    timestamp = Column(DateTime, default=datetime.utcnow)

    cpm = Column(Integer, nullable=True)
    svh = Column(Float, nullable=True)

    bq = Column(Integer, nullable=True)
    cpkg = Column(Integer, nullable=True)
    gray = Column(Integer, nullable=True)

    base_device = relationship("Device", single_parent=True)
