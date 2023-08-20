# Copyright (C) 2020 Dantali0n
# SPDX-License-Identifier: Apache-2.0

import abc
import enum
from typing import Dict
from typing import Optional
from typing import Set
from typing import Type


from radloggerpy._i18n import _

from oslo_log import log
from radloggerpy import config

LOG = log.getLogger(__name__)
CONF = config.CONF


class StateMachine(metaclass=abc.ABCMeta):
    """Abstract class to provide a state machine to any object"""

    _U = Dict[enum.Enum, Set[enum.Enum]]
    """Transition dictionary structure type"""

    _state: enum.Enum
    """Internal state object to maintain the current state"""

    _sclass: Type[enum.Enum]
    """Enum class used for states"""

    POSSIBLE_STATES: Optional[enum.Enum] = None
    """
    Set to a enum that has an item for all desired possible states the initial
    value of this variable is the initial state.

    Super classes implementing StateMachine should consider overriding this
    variable.
    """

    transitions: _U = dict()
    """
    Dictionary with sets as values were the key indicates the current state and
    the elements in the set describe valid transitions.

    Super classes should not override this variable and instead rely on
    `super().__init__(transitions)`. This ensures that the structure of
    transitions is valid.
    """

    def __init__(self, transitions: _U, states: enum.Enum = None):
        if states and isinstance(states, enum.Enum):
            self.POSSIBLE_STATES = states
        elif not isinstance(self.POSSIBLE_STATES, enum.Enum):
            raise RuntimeError(
                _("Neither POSSIBLE_STATES nor states are of" "type Enum")
            )

        self._sclass = self.POSSIBLE_STATES.__class__

        self.transitions = transitions
        self._verify_transitions()

        self.reset_state()

    def _verify_transitions(self):
        """Iterate the TRANSITIONS dictionary and validate its completeness"""

        for t in self._sclass:
            if t not in self.transitions:
                raise RuntimeError(
                    _("Not all states have required valid transition set")
                )
            for s in self.transitions[t]:
                if not isinstance(s, self._sclass):
                    raise RuntimeError(
                        _(
                            "Not all members of transition set "
                            "are of same type as state"
                        )
                    )

    def reset_state(self):
        """Reset state to the initial state"""
        self._state = self.POSSIBLE_STATES

    def get_state(self):
        return self._state

    def transition(self, state: enum.Enum):
        """Transition from the current state to a new desired state

        :param state: The new desired state
        :raises RuntimeWarning: This warning is raised when the new desired
                state requires an illegal transition
        """

        if not isinstance(state, self._sclass):
            raise RuntimeWarning(_("State is not of same type as POSSIBLE_STATES"))

        if state in self.transitions[self._state]:
            self._state = state
        else:
            raise RuntimeWarning(
                _("Transition from %(initial)s to %(to)s state is not valid")
                % {"initial": self._state, "to": state}
            )
