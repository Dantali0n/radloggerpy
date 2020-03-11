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

    As an example, to commit an object to the database one would call:
    ``DatabaseObject.add(session, object)``

    Classes implementing these interfaces should implement at least
    :py:func:`~add`, :py:func:`~update`, :py:func:`~delete` and
    :py:func:`~find`, however, also implementing :py:func:`~find_all` and
    :py:func:`~add_all` is preferred.

    All reference objects used as parameter by static methods should be
    instances of the implementing class itself. Likewise, find and find_all
    should only return objects which are instances of the class itself.

    Below is a demonstration of how interactions should look:
    ``dbo = DatabaseObject(**{field1: value1, field2: value2})``
    ``result = DatabaseObject.find(session, dbo)``
    ``print(result.field1)``

    For models using enums or choicetypes the values should be set as object
    attributes while the keys should be used for internal models.
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
        """Build the object with its given attributes for internal models"""
        pass

    @staticmethod
    def _filter(filter_object):
        """Filters the object depending on it's set attributes

        **Does not remove any undesired attributes of object**
        Returns a dictionary with all attributes that are not None

        TODO(Dantali0n): Make this remove relationship attributes from models?
        """

        return {key: name for (key, name) in vars(filter_object).items()
                if hasattr(filter_object.__class__, key)}

    @staticmethod
    @abc.abstractmethod
    def add(session, reference):
        """Add the reference object to the database

        :param session: an active :py:class:`sqlalchemy.orm.session.Session`
        :param reference: add database entries based on this object
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def update(session, reference, base, allow_multiple=False):
        """Find the reference(s) in the database and update with own state

        :param session: an active :py:class:`sqlalchemy.orm.session.Session`
        :param reference: the object with the desired changes
        :param base: current state of the object in the database
        :param allow_multiple: if updating multiple database items is allowed
        :raises MultipleResultsFound: if multiple results were found with
            allow_multiple as False of type
            :py:class:`sqlalchemy.orm.exc.MultipleResultsFound`
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def delete(session, reference, allow_multiple=False):
        """Remove the object(s) that match the reference

        :param session: an active :py:class:`sqlalchemy.orm.session.Session`
        :param reference: remove database entries based on this object
        :param allow_multiple: if updating multiple database items is allowed
        :raises MultipleResultsFound: if multiple results were found with
            allow_multiple as False of type
            :py:class:`sqlalchemy.orm.exc.MultipleResultsFound`
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def find(session, reference, allow_multiple=True):
        """Return object(s) that match the reference

        :param session: an active :py:class:`sqlalchemy.orm.session.Session`
        :param reference: find database results based on this object
        :param allow_multiple: if updating multiple database items is allowed
        :raises MultipleResultsFound: if multiple results were found with
            allow_multiple as False of type
            :py:class:`sqlalchemy.orm.exc.MultipleResultsFound`
        :return: A single object, list of objects or none, all objects will be
            instances of the class.
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def find_all(session, references):
        """For every specified object find all its matching database objects

        :param session: an active :py:class:`sqlalchemy.orm.session.Session`
        :param references: find database results based on these objects
        :return: list of objects or none, all objects will be instances of the
            class.
        """
        pass

    @staticmethod
    @abc.abstractmethod
    def add_all(session, references):
        """Add all specified objects to the database

        :param session: an active :py:class:`sqlalchemy.orm.session.Session`
        :param references: add all these objects to the database
        """
        pass
