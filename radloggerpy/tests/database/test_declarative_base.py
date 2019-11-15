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

from oslo_log import log

from radloggerpy import config

from radloggerpy.database.declarative_base import Base
from radloggerpy.database.declarative_base import base as decl_base_inst
from radloggerpy.tests import base

LOG = log.getLogger(__name__)
CONF = config.CONF


class TestDeclarativeBase(base.TestCase):

    # class FakeBase(object):
    #     @declared_attr
    #     def __tablename__(cls):
    #         return cls.__name__.lower()

    def setUp(self):
        super(TestDeclarativeBase, self).setUp()

        # self.p_base = mock.patch.object(
        #     declarative, 'declarative_base',
        #     new=declarative.declarative_base)
        # self.m_decl_base = self.p_base.start()
        # self.addCleanup(self.p_base.stop)

    def test_base_cls_base(self):
        """The sqlalchemy declarative_base passed base object"""

        self.assertEqual(Base.__doc__, decl_base_inst.__doc__)

    # @mock.patch.object(decl_base_module, 'base')
    # def test_base_tablename_lower(self, m_base_instance):
    #     """Assert that the baseclass tablename lower gets applied"""
    #
    #     # Create a in memory sqlite database using a declarative_base
    #     m_base = self.m_decl_base(cls=TestDeclarativeBase.FakeBase)
    #     m_engine = create_engine('sqlite:///:memory:', echo=True)
    #
    #     # This model wil be added to the declarative_base
    #     class TestModel(m_base):
    #         id = Column(Integer, primary_key=True)
    #
    #     # Create all tables for the in memory database
    #     m_base.metadata.create_all(bind=m_engine)
    #
    #     # Create a ORM session and add an instance of model to the database
    #     m_session = sessionmaker(bind=m_engine)
    #     m_session = m_session()
    #     m_model = TestModel()
    #     m_session.add(m_model)
    #     m_session.commit()
    #     m_session.close()
    #
    #     # Create a Core connection and fetch instances using plain SQL
    #     m_conn = m_engine.connect()
    #     m_text = text("SELECT * FROM testmodel")
    #     result = m_conn.execute(m_text).fetchall()
    #     m_conn.close()
    #
    #     # Check that the inserted element could be retrieved from the
    #     # database using the lowercase name of the model class.
    #     self.assertEqual(1, len(result))
