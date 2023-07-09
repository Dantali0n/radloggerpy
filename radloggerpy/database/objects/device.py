# Copyright (C) 2019 Dantali0n
# SPDX-License-Identifier: Apache-2.0

from radloggerpy.database.models.device import Device
from radloggerpy.database.objects.base import DatabaseObject

# from radloggerpy.database.objects.serial_device import SerialDeviceObject
from radloggerpy.types.device_interfaces import INTERFACE_CHOICES
from radloggerpy.types.device_types import DEVICE_TYPE_CHOICES


class DeviceObject(DatabaseObject):
    """device object with base model attributes"""

    id = None
    name = None
    enabled = None
    type = None
    interface = None
    implementation = None

    m_device = None

    def _build_object(self):
        self.m_device = Device()

        if self.id:
            self.m_device.id = self.id
        if self.name:
            self.m_device.name = self.name

        if self.enabled:
            self.m_device.enabled = self.enabled

        if self.type in DEVICE_TYPE_CHOICES.keys():
            self.m_device.type = self.type
        elif self.type in DEVICE_TYPE_CHOICES.values():
            index = list(DEVICE_TYPE_CHOICES.values()).index(self.type)
            self.m_device.type = list(DEVICE_TYPE_CHOICES.keys())[index]

        if self.interface in INTERFACE_CHOICES.keys():
            self.m_device.interface = self.interface
        elif self.interface in INTERFACE_CHOICES.values():
            index = list(INTERFACE_CHOICES.values()).index(self.interface)
            self.m_device.interface = list(INTERFACE_CHOICES.keys())[index]

        if self.implementation:
            self.m_device.implementation = self.implementation

    def _build_attributes(self):
        if self.m_device.id:
            self.id = self.m_device.id
        if self.m_device.name:
            self.name = self.m_device.name

        if self.m_device.enabled:
            self.enabled = self.m_device.enabled

        if self.m_device.type:
            self.type = DEVICE_TYPE_CHOICES[self.m_device.type]

        if self.m_device.interface:
            self.interface = INTERFACE_CHOICES[self.m_device.interface]

        if self.m_device.implementation:
            self.implementation = self.m_device.implementation.code

    @staticmethod
    def add(session, reference):
        NotImplementedError()

    @staticmethod
    def update(session, reference, base, allow_multiple=False):
        NotImplementedError()

    @staticmethod
    def delete(session, reference, allow_multiple=False):
        reference._build_object()

        filters = reference._filter(reference.m_device)
        query = session.query(Device).filter_by(**filters)

        if allow_multiple:
            results = query.all()

            if results is None:
                return None

            devs = list()

            for result in results:
                dev = DeviceObject()
                dev.m_device = result
                session.delete(result)
                dev._build_attributes()
                devs.append(dev)
        else:
            result = query.one_or_none()

            if result is None:
                return None

            dev = DeviceObject()
            dev.m_device = result
            dev._build_attributes()
            session.delete(result)

        try:
            session.commit()
        except Exception:
            session.rollback()
            # TODO(Dantali0n): These errors are horrendous for users to
            #                  understand an error abstraction is needed.
            raise

        if allow_multiple:
            return devs
        else:
            return dev

    @staticmethod
    def find(session, reference, allow_multiple=True):
        reference._build_object()

        filters = reference._filter(reference.m_device)
        query = session.query(Device).filter_by(**filters)

        if allow_multiple:
            results = query.all()

            if results is None:
                return None

            ret_results = list()
            for result in results:
                dev = DeviceObject()
                dev.m_device = result
                dev._build_attributes()
                ret_results.append(dev)

            return ret_results
        else:
            result = query.one_or_none()

            if result is None:
                return None

            dev = DeviceObject()
            dev.m_device = result
            dev._build_attributes()
            return dev

    @staticmethod
    def find_enabled(session):
        return DeviceObject.find(session, DeviceObject(**{"enabled": True}), True)

    # @staticmethod
    # def upgrade(session, reference):
    #     """Upgrade the basic DeviceObject to its specific interface object"""
    #
    #     if reference.interface is DeviceInterfaces.SERIAL:
    #         return SerialDeviceObject.find(session, reference)
    #     elif reference.interface is DeviceInterfaces.ETHERNET:
    #         raise NotImplementedError(_("Class EthernetDeviceObject not"
    #                                     "implemented yet."))

    @staticmethod
    def find_all(session, references):
        NotImplementedError()

    @staticmethod
    def add_all(session, references):
        NotImplementedError()
