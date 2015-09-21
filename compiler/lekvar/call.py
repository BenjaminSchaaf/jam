from contextlib import ExitStack

from ..errors import *

from .state import State
from .core import Context, Object, BoundObject, Type
from .function import FunctionType
from .dependent import DependentTarget

class Call(Object):
    called = None
    values = None
    return_type = None
    function = None

    def __init__(self, called:Object, values:[Object], return_type:Type = None, tokens = None):
        super().__init__(tokens)
        self.called = called
        self.values = values
        self.return_type = return_type
        self.function = None

    def verify(self):
        self.called.verify()

        # Verify arguments and create the function type of the call
        arg_types = []
        for value in self.values:
            value.verify()
            value_type = value.resolveType()

            if value_type is None:
                raise TypeError("Cannot pass nothing as an argument", value.tokens)
            arg_types.append(value_type)

        call_type = FunctionType(arg_types, self.return_type)
        call_type.verify()

        # Resolve the call
        with State.type_switch():
            self.function = self.called.resolveCall(call_type)

    def resolveType(self):
        # Hack for dependent types
        context = self.function.target() if isinstance(self.function, DependentTarget) else ExitStack()
        with context:
            type = self.function.resolveType().return_type
            return type.resolveValue() if type is not None else None

    def __repr__(self):
        return "{}({})".format(self.called, ", ".join(repr(val) for val in self.values))
