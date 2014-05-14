# -*- coding: utf-8 -*-

from types import Environment, LispError, Closure
from ast import is_boolean, is_atom, is_symbol, is_list, is_closure, is_integer
from asserts import assert_exp_length, assert_valid_definition, assert_boolean
from parser import unparse
import re as re

"""
This is the Evaluator module. The `evaluate` function below is the heart
of your language, and the focus for most of parts 2 through 6.

A score of useful functions is provided for you, as per the above imports, 
making your work a bit easier. (We're supposed to get through this thing 
in a day, after all.)
"""

integer = re.compile('[0-9]+')
symbol = re.compile('[a-zA-Z*<>+=-]+')



def evaluate(ast, env):
    """Evaluate an Abstract Syntax Tree in the specified environment."""

    # evaluating booleans
    if is_boolean(ast):
        return ast
    if is_integer(ast):
        return ast
    if ast[0] == "quote":
        return ast[1]
    if ast[0] == "atom":
        return is_atom(evaluate(ast[1], env))
    if ast[0] == "eq":
        return evaluate(ast[1], env) == evaluate(ast[2], env) and \
               is_atom(evaluate(ast[1], env)) and is_atom(evaluate(ast[2], env))




