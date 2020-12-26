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

import abc
import enum

from radloggerpy._i18n import _

from oslo_log import log
from radloggerpy import config

LOG = log.getLogger(__name__)
CONF = config.CONF


class StateMachine(metaclass=abc.ABCMeta):
    """Abstract class to provide a state machine to any object"""

    _state = None
    """Internal state object to maintain the current state"""

    _sclass = None
    """enum class used for states"""

    POSSIBLE_STATES = None
    """
    Set to a enum that has an item for all desired possible states the initial
    value of this variable is the initial state.
    """

    TRANSITIONS = dict()
    """
    Dictionary with sets as values were the key indicates the current state and
    the elements in the set describe valid transitions.
    """

    def __init__(self, transitions: dict, states: enum = None):
        if states:
            self.POSSIBLE_STATES = states
        self._sclass = self.POSSIBLE_STATES.__class__

        self.TRANSITIONS = transitions
        self._verify_transitions()

        self.reset_state()

    def _verify_transitions(self):
        """Iterate the TRANSITIONS dictionary and validate its completeness"""

        for t in self._sclass:
            if t not in self.TRANSITIONS:
                raise RuntimeError(
                    _("Not all states have required valid transition set"))
            for s in self.TRANSITIONS[t]:
                if not isinstance(s, self._sclass):
                    raise RuntimeError(_("Not all members of transition set "
                                         "are of same type as state"))

    def reset_state(self):
        """Reset state to the initial state"""
        self._state = self.POSSIBLE_STATES

    def get_state(self):
        return self._state

    def transition(self, state: enum = None):
        """Transition from the current state to a new desired state

        :param state: The new desired state
        :raises RuntimeWarning: This warning is raised when the new desired
                state requires an illegal transition
        """

        if not isinstance(state, self._sclass):
            raise RuntimeWarning(
                _("State is not of same type as POSSIBLE_STATES"))

        if state in self.TRANSITIONS[self._state]:
            self._state = state
        else:
            raise RuntimeWarning(
                _("Transition from %(initial)s to %(to)s state is not valid") %
                {'initial': self._state, 'to': state})
