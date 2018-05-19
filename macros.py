from preprocessor import *

def array_literal(*values):
    return clist(values)

def repeat(value, length):
    return [value] * length

def buffer(value, length):
    return array_literal(*repeat(char(value), length - 1), 0)
