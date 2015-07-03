from ..errors import *

from .state import State
from .core import Context, Object, BoundObject, Type
from .function import Function
from .module import Module

#
# Loop
#

class Loop(Object):
    function = None
    instructions = None

    def __init__(self, instructions, tokens = None):
        super().__init__(tokens)

        self.instructions = instructions

    def copy(self):
        return Loop(self.instructions)

    def verify(self):
        if not isinstance(State.scope, (Function, Module)):
            raise SyntaxError("Cannot loop here", self.tokens)
        self.function = State.scope

        with State.scoped(self, soft = True, analys = True) as state:
            for instruction in self.instructions:
                instruction.verify()

        # Update scope state
        State.soft_scope_state.imerge_or(state)

    def resolveType(self):
        raise InternalError("Loop objects do not have a type")

#
# Break
#

class Break(Object):
    loop = None

    def __init__(self, tokens = None):
        super().__init__(tokens)

    def copy(self):
        return Break()

    def verify(self):
        self.loop = State.getSoftScope(lambda a: isinstance(a, Loop))
        if self.loop is None:
            raise SyntaxError("Cannot `break` outside loop", self.tokens)

    def resolveType(self):
        raise InternalError("Break objects do not have a type")

#
# Branch
#

class Branch(Object):
    function = None
    condition = None
    true_instructions = None
    false_instructions = None

    def __init__(self, condition, true_instructions, false_instructions, tokens = None):
        super().__init__(tokens)

        self.condition = condition
        self.true_instructions = true_instructions
        self.false_instructions = false_instructions

    def copy(self):
        return Branch(self.condition, self.true_instructions, self.false_instructions)

    def verify(self):
        if not isinstance(State.scope, (Function, Module)):
            raise SyntaxError("Cannot branch here", self.tokens)
        self.function = State.scope

        self.condition.verify()

        with State.scoped(self, soft = True, analys = True) as tstate:
            for instruction in self.true_instructions:
                instruction.verify()

        with State.scoped(self, soft = True, analys = True) as fstate:
            for instruction in self.false_instructions:
                instruction.verify()

        # Update scope state
        State.soft_scope_state.imerge_and(tstate.merge_or(fstate))

    def resolveType(self):
        raise InternalError("Branch objects do not have a type")
