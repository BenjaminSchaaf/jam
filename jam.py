#!/usr/bin/env python3

import os
import sys
import logging
import argparse
from io import StringIO

from compiler.jam import compiler

parser = argparse.ArgumentParser(
    prog = "jam",
    description = "The Jam Compiler",
)
parser.add_argument("input",
    help="The source file to compile.",
    metavar="FILE",
    type=argparse.FileType('r'),
)
parser.add_argument("--verbose", "-v",
    help="Enable debug logging at a specific level.",
    action='count',
    required=False,
    default=0,
)
parser.add_argument("--output", "-o",
    help="The file to compile to.",
    type=argparse.FileType('w'),
    required=False,
    default=None,
)
parser.add_argument("--norun", "-r",
    help="Only compile the file, don't run it. Use in conjunction with -o to compile to a target.",
    action='store_true',
    required=False,
)
parser.add_argument("--version",
    help="Prints the version of the program.",
    action='version',
    version="Jam Compiler V0.1a",
)

def main():
    args = parser.parse_args()

    output = args.output or open(os.devnull, "w")

    compile = compiler.compile if args.norun else compiler.compileRun

    logging.basicConfig(level=logging.WARNING - args.verbose*10, stream=sys.stdout)

    with args.input, output:
        print(compile(args.input, output))

if __name__ == "__main__":
    main()
