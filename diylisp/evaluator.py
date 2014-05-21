# -*- coding: utf-8 -*-

from types import Environment, LispError, Closure
from ast import is_boolean, is_atom, is_symbol, is_list, is_closure, is_integer
from asserts import assert_exp_length, assert_valid_definition, assert_boolean
from parser import unparse
import re as re
from operator import add, sub, mul, div, gt, lt, ge, le, mod

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

    # evaluating atoms
    if is_symbol(ast):
        return env.lookup(ast)
    if is_boolean(ast):
        return ast
    if is_integer(ast):
        return ast

    if is_list(ast):

        if ast[0] == "quote":
            return ast[1]
        # functions

        if is_closure(ast[0]):
            closure = ast[0]
            arguments = ast[1:]
            params = closure.params
            number_of_arguments = len(arguments)
            number_of_params = len(params)

            if number_of_arguments != number_of_params:
                raise LispError("wrong number of arguments, expected %(param)d got %(arg)d" %
                                {"arg": number_of_arguments, "param": number_of_params})
            variables = {}
            for i in range(number_of_arguments):
                arg = evaluate(arguments[i], env)
                param = params[i]
                variables.update({param: arg})
            environment = closure.env.extend(variables)

            return evaluate(closure.body, environment)

        if ast[0] == "cons":
            if len(ast) != 3:
                raise LispError
            else:
                value = evaluate(ast[1], env)
                list = evaluate(ast[2], env)
                new_list = [value]
                for i in list:
                    new_list.append(i)
                return new_list

        if ast[0] == "lambda":
            if not is_list(ast[1]):
                raise LispError
            if len(ast) == 3:
                return Closure(env, ast[1], ast[2])
            else:
                raise LispError("number of arguments")

        # defining variables
        if ast[0] == "define":
            if is_symbol(ast[1]):
                if len(ast) == 3:
                    return env.set(ast[1], evaluate(ast[2], env))
                else:
                    raise LispError("Wrong number of arguments")
            else:
                raise LispError("non-symbol")

        #typechecks
        if ast[0] == "atom":
            return is_atom(evaluate(ast[1], env))
        if ast[0] == "eq":
            return evaluate(ast[1], env) == evaluate(ast[2], env) and \
                   is_atom(evaluate(ast[1], env)) and is_atom(evaluate(ast[2], env))

        #arithmetic:
        # elif is_arith_op(ast[0]):
        #     try:
        #         return arith_ops[ast[0]](evaluate(ast[1], env), evaluate(ast[2], env))
        # make dicitonary of these operators

        if ast[0] == "+":
            if is_integer(evaluate(ast[1], env)) and is_integer(evaluate(ast[2], env)):
                return evaluate(ast[1], env) + evaluate(ast[2], env)
            else:
                raise LispError
        if ast[0] == "-":
            if is_integer(evaluate(ast[1], env)) and is_integer(evaluate(ast[2], env)):
                return evaluate(ast[1], env) - evaluate(ast[2], env)
            else:
                raise LispError
        if ast[0] == "*":
            if is_integer(evaluate(ast[1], env)) and is_integer(evaluate(ast[2], env)):
                return evaluate(ast[1], env) * evaluate(ast[2], env)
            else:
                raise LispError
        if ast[0] == "/":
            if is_integer(evaluate(ast[1], env)) and is_integer(evaluate(ast[2], env)):
                return evaluate(ast[1], env) / evaluate(ast[2], env)
            else:
                raise LispError
        if ast[0] == "mod":
            if is_integer(evaluate(ast[1], env)) and is_integer(evaluate(ast[2], env)):
                return evaluate(ast[1], env) % evaluate(ast[2], env)
            else:
                raise LispError

        # boolean operators
        if ast[0] == ">":
            return evaluate(ast[1], env) > evaluate(ast[2], env)
        if ast[0] == "<":
            return evaluate(ast[1], env) < evaluate(ast[2], env)

        # control-flow
        if ast[0] == 'if':
            pred = ast[1]
            then = ast[2]
            elsee = ast[3]
            if evaluate(pred, env):
                return evaluate(then, env)
            else:
                return evaluate(elsee, env)

        if is_symbol(ast[0]) or is_list(ast[0]):
            closure = evaluate(ast[0], env)
            return evaluate([closure] + ast[1:], env)

        else:
            raise LispError("not a function")


