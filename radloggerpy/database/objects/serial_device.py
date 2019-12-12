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
from radloggerpy.types.serial_bytesize_types import SerialBytesizeTypes
from radloggerpy.types.serial_parity_types import SerialParityTypes
from radloggerpy.types.serial_stopbit_types import SerialStopbitTypes


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

    BYTESIZE_CHOICES = {
        5: SerialBytesizeTypes.FIVEBITS,
        6: SerialBytesizeTypes.SIXBITS,
        7: SerialBytesizeTypes.SEVENBITS,
        8: SerialBytesizeTypes.EIGHTBITS,
    }

    PARITY_CHOICES = {
        "none": SerialParityTypes.PARITY_NONE,
        "odd": SerialParityTypes.PARITY_ODD,
        "even": SerialParityTypes.PARITY_EVEN,
        "mark": SerialParityTypes.PARITY_MARK,
        "space": SerialParityTypes.PARITY_SPACE
    }

    STOPBIT_CHOICES = {
        1: SerialStopbitTypes.STOPBITS_ONE,
        1.5: SerialStopbitTypes.STOPBITS_ONE_POINT_FIVE,
        2: SerialStopbitTypes.STOPBITS_TWO,
    }

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

        if self.BYTESIZE_CHOICES[self.bytesize]:
            self.m_serial_device.bytesize = \
                self.BYTESIZE_CHOICES[self.bytesize]
        elif self.bytesize:
            self.m_serial_device.bytesize = self.bytesize

        if self.PARITY_CHOICES[self.parity]:
            self.m_serial_device.parity = \
                self.PARITY_CHOICES[self.parity]
        elif self.parity:
            self.m_serial_device.parity = self.parity

        if self.STOPBIT_CHOICES[self.stopbits]:
            self.m_serial_device.stopbits = \
                self.STOPBIT_CHOICES[self.stopbits]
        elif self.stopbits:
            self.m_serial_device.stopbits = self.stopbits

        if self.timeout:
            self.m_serial_device.timeout = self.timeout

    def add(self, session):
        """Add the current state of the object to the database

        :param session: an active :py:class:`sqlalchemy.orm.session.Session`
        """

        self._build_object()

        session.add(self.m_device)

        session.add(self.m_serial_device)

        try:
            session.commit()
        except Exception as e:
            session.rollback()
            # TODO(Dantali0n): These errors are horrendous for users to
            #                  understand an error abstraction is needed.
            raise

    def update(self, session, reference, allow_multiple=False):
        """Find the reference(s) in the database and update with own state

        :param session: an active :py:class:`sqlalchemy.orm.session.Session`
        :param reference: the reference to find to apply the update to
        :param allow_multiple: if updating multiple database items is allowed
        """
        pass

    def remove(self, session, allow_multiple=False):
        """Remove the object(s) that match the current state

        :param session: an active :py:class:`sqlalchemy.orm.session.Session`
        :param allow_multiple: if updating multiple database items is allowed
        """
        pass

    def find(self, session, allow_multiple=True):
        """Return object(s) that match the current state

        :param session: an active :py:class:`sqlalchemy.orm.session.Session`
        :param allow_multiple: if updating multiple database items is allowed
        """
        pass

    @staticmethod
    def find_all(session, objects):
        """For every specified object find all its matching database objects

        :param session: an active :py:class:`sqlalchemy.orm.session.Session`
        :param objects: find database results based on these objects
        """
        pass

    @staticmethod
    def add_all(session, objects):
        """Add all specified objects to the database

        :param session: an active :py:class:`sqlalchemy.orm.session.Session`
        :param objects: add all these objects to the database
        """
        pass
