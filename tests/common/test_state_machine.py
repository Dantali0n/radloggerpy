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

from enum import Enum
from enum import unique

from oslo_log import log
from radloggerpy import config

from radloggerpy.common.state_machine import StateMachine

from tests import base

LOG = log.getLogger(__name__)
CONF = config.CONF


@unique
class DummyEnum(Enum):
    __order__ = 'EXP DUMMY'
    EXP = 1
    DUMMY = 2


class TestStateMachine(base.TestCase):

    dummy_transitions = {
        DummyEnum.EXP: {DummyEnum.EXP},
        DummyEnum.DUMMY: {DummyEnum.EXP, DummyEnum.DUMMY}
    }

    class DummyStateMachine(StateMachine):

        POSSIBLE_STATES = DummyEnum.EXP

    class FalseStateMachine(StateMachine):
        """FalseStateMachine does not define POSSIBLE_STATES"""

    def setUp(self):
        super(TestStateMachine, self).setUp()

    def test_init_variable(self):
        m_machine = self.DummyStateMachine(self.dummy_transitions)

        self.assertEqual(DummyEnum.EXP, m_machine.get_state())

    def test_init_error(self):
        """FalseStateMachine raise error on construction without states param

        Test that constructing a StateMachine object raises an error if both
        the POSSIBLE_STATES attribute and states parameter are None.
        """

        self.assertRaises(RuntimeError, self.FalseStateMachine,
                          self.dummy_transitions)

    def test_verify_error(self):

        transitions = {
            DummyEnum.EXP: {DummyEnum.EXP}
        }

        self.assertRaises(RuntimeError, self.DummyStateMachine, transitions)

    def test_verify_type_error(self):

        transitions = {
            DummyEnum.EXP: {None},
            DummyEnum.DUMMY: {}
        }

        self.assertRaises(RuntimeError, self.DummyStateMachine, transitions)

    def test_init_argument(self):
        m_machine = self.DummyStateMachine(
            self.dummy_transitions, DummyEnum.DUMMY)

        self.assertEqual(DummyEnum.DUMMY, m_machine.get_state())

    def test_transition(self):
        m_machine = self.DummyStateMachine(
            self.dummy_transitions, DummyEnum.DUMMY)

        m_machine.transition(DummyEnum.EXP)
        self.assertEqual(DummyEnum.EXP, m_machine.get_state())

    def test_transition_error(self):
        m_machine = self.DummyStateMachine(
            self.dummy_transitions, DummyEnum.EXP)

        self.assertRaises(
            RuntimeWarning, m_machine.transition, DummyEnum.DUMMY)

    def test_transition_type_error(self):
        m_machine = self.DummyStateMachine(
            self.dummy_transitions, DummyEnum.EXP)

        self.assertRaises(RuntimeWarning, m_machine.transition, None)

    def test_reset(self):
        m_machine = self.DummyStateMachine(
            self.dummy_transitions, DummyEnum.DUMMY)

        m_machine.transition(DummyEnum.EXP)
        m_machine.reset_state()
        self.assertEqual(DummyEnum.DUMMY, m_machine.get_state())
