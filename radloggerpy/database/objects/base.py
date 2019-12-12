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

import abc
import six


@six.add_metaclass(abc.ABCMeta)
class DatabaseObject(object):
    """Abstract database object providing abstract CRUD interfaces

    When using SQLAlchemy database sessions all interactions with these
    sessions should be achieved using object which implement
    :py:class:`~.DatabaseObject`. These objects provide CRUD methods to handle
    interactions allowing to obfuscate that many of the objects in the database
    are consistent of multiple models.

    to commit an object to the database one would call:
    `object.add(session)`
    """

    def __init__(self, **kwargs):
        """Initialize the object matching its arguments

        :param kwargs: named arguments
        """

        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    @abc.abstractmethod
    def _build_object(self):
        """Build the object with its given attributes for matching models"""
        pass

    @abc.abstractmethod
    def add(self, session):
        """Add the current state of the object to the database

        :param session: an active :py:class:`sqlalchemy.orm.session.Session`
        """
        pass

    @abc.abstractmethod
    def update(self, session, reference, allow_multiple=False):
        """Find the reference(s) in the database and update with own state

        :param session: an active :py:class:`sqlalchemy.orm.session.Session`
        :param reference: the reference to find to apply the update to
        :param allow_multiple: if updating multiple database items is allowed
        """
        pass

    @abc.abstractmethod
    def remove(self, session, allow_multiple=False):
        """Remove the object(s) that match the current state

        :param session: an active :py:class:`sqlalchemy.orm.session.Session`
        :param allow_multiple: if updating multiple database items is allowed
        """
        pass

    @abc.abstractmethod
    def find(self, session, allow_multiple=True):
        """Return object(s) that match the current state

        :param session: an active :py:class:`sqlalchemy.orm.session.Session`
        :param allow_multiple: if updating multiple database items is allowed
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def find_all(session, objects):
        """For every specified object find all its matching database objects

        :param session: an active :py:class:`sqlalchemy.orm.session.Session`
        :param objects: find database results based on these objects
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def add_all(session, objects):
        """Add all specified objects to the database

        :param session: an active :py:class:`sqlalchemy.orm.session.Session`
        :param objects: add all these objects to the database
        """
        pass
