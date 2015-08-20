import logging
import subprocess
from tempfile import NamedTemporaryFile

from .. import lekvar
from ..errors import *

from .state import State
from .builtins import builtins
from . import emitter
from . import bindings

def emit(module:lekvar.Module, logger = logging.getLogger()):
    State.logger = logger.getChild("llvm")

    with State.begin("main", logger):
        module.emit()

    State.module.verify()
    return State.module.toString()

# Wrapping around lli
#TODO: Replace with direct calls to llvm
def run(source:bytes):
    try:
        return subprocess.check_output("lli",
            input = source,
            stderr = subprocess.STDOUT,
        )
    except subprocess.CalledProcessError as e:
        raise ExecutionError("lli error running source: {}".format(e.output))

# Wrapping around clang
#TODO: Replace with direct calls to llvm
def compile(source:bytes):
    try:
        with NamedTemporaryFile('wb', suffix=".ll") as f_in, NamedTemporaryFile('rb') as f_out:
            f_in.write(source)
            f_in.flush()
            subprocess.check_output(["clang", "-o", f_out.name, f_in.name],
                                    stderr = subprocess.STDOUT)
            return f_out.read()
    except subprocess.CalledProcessError as e:
        output = e.output.decode("UTF-8")
        raise ExecutionError("clang error compiling source {}".format(output))
