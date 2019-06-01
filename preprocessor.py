#!/usr/bin/env python3

import json
import re
import sys
from pathlib import Path
from typing import Any, Sequence

class char(str):
    def __init__(self, value):
        super().__init__(value)

        if len(self) != 1:
            raise ValueError(f"char instance with multiple character: '{value}'")

def cstr(value: str):
    if not isinstance(value, str):
        raise TypeError(f"Given a value of type '{type(value)}', expected str.")

    return json.dumps(value)

def cchar(value: char):
    if not isinstance(value, str):
        # Allowing 'str' on purpose, so literrals are accepted
        raise TypeError(f"Given a value of type '{type(value)}, expected char.'")
    if len(value) != 1:
        raise ValueError(f"Expected a single character, got '{value}'.")

    return "'{}'".format(value)

def cbool(value: bool):
    return str(bool(value)).lower()

def clist(value: Sequence[Any]):
    return "{" + ", ".join(map(repr, value)) + "}"

crepr_functions = {
    bool:   cbool,
    str:    cstr,
    char:   cchar,
    int:    str,
    float:  str,
    list:   clist,
    map:    clist,
    #dict: ???,
}

def crepr(val):
    try:
        fn = crepr_functions[type(val)]
    except KeyError:
        raise TypeError(f"'{type(val)}' isn't a supported crepr type.")

    return repr(fn(val))

def call(fn: str, *args):
    return "{}({})".format(fn, repr(clist(args))[1:-1])

def import_macros(code):
    lines = code.split("\n")
    lines = filter(lambda x: x.startswith("#pragma pymacros"), lines)

    for line in lines:
        pragma, pymacros, fname = line.replace('"', "").split(" ")
        filename = Path(fname)
        sys.path.insert(0, Path(filename, "..").resolve())
        exec("from {} import *".format(filename.stem), globals())

def apply_macros(code, filename):
    import_macros(code)
    chunks = re.findall("[a-zA-Z0-9_]+!\(.+\)", code)

    for chunk in chunks:
        (name, args) = re.findall(r"(.*)?!\((.*)\)", chunk)[0]
        result = eval("{}({})".format(name, args))
        code = code.replace(chunk, str(result))

    return code

if __name__ == "__main__":
    filename = sys.argv[1]
    with open(filename) as f:
        code = f.read()
    print(apply_macros(code, filename))
