#!/usr/bin/env python3

import json
import re
import sys
from pathlib import Path
from typing import Any, Sequence

class char(str):
    pass

def cstr(value: str):
    return json.dumps(value)

def cchar(value: char):
    return "'{}'".format(value[0])

def cbool(value: bool):
    return str(value).lower()

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
    fn = crepr_functions[type(val)]

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
