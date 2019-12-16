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

from radloggerpy.database.models.serial_device import SerialDevice
from radloggerpy.database.objects.device import DeviceObject
from radloggerpy.types.serial_bytesize import BYTESIZE_CHOICES
from radloggerpy.types.serial_parity import PARITY_CHOICES
from radloggerpy.types.serial_stopbit import STOPBIT_CHOICES


class SerialDeviceObject(DeviceObject):
    """Abstract database object providing abstract CRUD interfaces

    When using SQLAlchemy database sessions all interactions with these
    sessions should be achieved using object which implement
    :py:class:`~.DatabaseObject`. These objects provide CRUD methods to handle
    interactions allowing to obfuscate that many of the objects in the database
    are consistent of multiple models.

    to commit an object to the database one would call:
    `object.add(session)`
    """

    "Device serial model attributes"
    port = None
    baudrate = None
    bytesize = None
    parity = None
    stopbits = None
    timeout = None

    m_serial_device = None

    def _build_object(self):
        super(SerialDeviceObject, self)._build_object()

        self.m_serial_device = SerialDevice()
        self.m_serial_device.base_device = self.m_device

        if self.port:
            self.m_serial_device.port = self.port
        if self.baudrate:
            self.m_serial_device.baudrate = self.baudrate

        if self.bytesize in BYTESIZE_CHOICES.keys():
            self.m_serial_device.bytesize = self.bytesize
        elif self.bytesize in BYTESIZE_CHOICES.values():
            index = list(BYTESIZE_CHOICES.values()).index(self.bytesize)
            self.m_serial_device.bytesize = \
                list(BYTESIZE_CHOICES.keys())[index]

        if self.parity in PARITY_CHOICES.keys():
            self.m_serial_device.parity = self.parity
        elif self.parity in PARITY_CHOICES.values():
            index = list(PARITY_CHOICES.values()).index(self.parity)
            self.m_serial_device.parity = \
                list(PARITY_CHOICES.keys())[index]

        if self.stopbits in STOPBIT_CHOICES.keys():
            self.m_serial_device.stopbits = self.stopbits
        elif self.stopbits in STOPBIT_CHOICES.values():
            index = list(STOPBIT_CHOICES.values()).index(self.stopbits)
            self.m_serial_device.stopbits = \
                list(STOPBIT_CHOICES.keys())[index]

        if self.timeout:
            self.m_serial_device.timeout = self.timeout

    @staticmethod
    def add(session, reference):
        reference._build_object()

        session.add(reference.m_device)

        session.add(reference.m_serial_device)

        try:
            return session.commit()
        except Exception as e:
            session.rollback()
            # TODO(Dantali0n): These errors are horrendous for users to
            #                  understand an error abstraction is needed.
            raise

    @staticmethod
    def update(session, reference, base, allow_multiple=False):
        NotImplementedError()

    @staticmethod
    def delete(session, reference, allow_multiple=False):
        NotImplementedError()

    @staticmethod
    def find(session, reference, allow_multiple=True):
        NotImplementedError()

    @staticmethod
    def find_all(session, references):
        NotImplementedError()

    @staticmethod
    def add_all(session, references):
        NotImplementedError()
