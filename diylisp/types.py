# -*- coding: utf-8 -*-

"""
This module holds some types we'll have use for along the way.

It's your job to implement the Closure and Environment types.
The LispError class you can have for free :)
"""

class LispError(Exception): 
    """General lisp error class."""
    pass

class Closure:
    
    def __init__(self, env, params, body):
        raise NotImplementedError("DIY")

    def __str__(self):
        return "<closure/%d>" % len(self.params)

class Environment:

    def __init__(self, variables=None):
        self.variables = variables if variables else {}

    def lookup(self, symbol):
        """Lookup returns the corresponding value of some variable."""
        if self.variables.get(symbol) != None:
            return self.variables.get(symbol)
        else: raise LispError (symbol)

    def extend(self, variables):
        """Extend lets you extend the environment with variables."""
        new = self.variables.copy()
        new.update(variables)
        return Environment(new)


    def set(self, symbol, value):
        """Set lets you add a key, value pair to the environment"""
        if self.variables.get(symbol) == None:
            return self.variables.update({symbol : value})
        else: raise LispError("already defined")
