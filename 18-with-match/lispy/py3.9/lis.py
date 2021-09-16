################ Lispy: Scheme Interpreter in Python 3.9

## (c) Peter Norvig, 2010-18; See http://norvig.com/lispy.html
## Minor edits for Fluent Python, Second Edition (O'Reilly, 2021)
## by Luciano Ramalho, adding type hints and pattern matching.

################ Imports and Types

import math
import operator as op
from collections import ChainMap
from collections.abc import MutableMapping, Iterator
from itertools import chain
from typing import Any, Union

Symbol = str
Atom = Union[float, int, Symbol]
Expression = Union[Atom, list]

Environment = MutableMapping[Symbol, object]


class Procedure:
    "A user-defined Scheme procedure."

    def __init__(self, parms: list[Symbol], body: list[Expression], env: Environment):
        self.parms = parms
        self.body = body
        self.env = env

    def __call__(self, *args: Expression) -> Any:
        local_env = dict(zip(self.parms, args))
        env: Environment = ChainMap(local_env, self.env)
        for exp in self.body:
            result = evaluate(exp, env)
        return result


################ Global Environment

def standard_env() -> Environment:
    "An environment with some Scheme standard procedures."
    env: Environment = {}
    env.update(vars(math))   # sin, cos, sqrt, pi, ...
    env.update({
        '+':op.add, '-':op.sub, '*':op.mul, '/':op.truediv,
        '>':op.gt, '<':op.lt, '>=':op.ge, '<=':op.le, '=':op.eq,
        'abs':     abs,
        'append':  op.add,
        'apply':   lambda proc, args: proc(*args),
        'begin':   lambda *x: x[-1],
        'car':     lambda x: x[0],
        'cdr':     lambda x: x[1:],
        'cons':    lambda x,y: [x] + y,
        'eq?':     op.is_,
        'equal?':  op.eq,
        'length':  len,
        'list':    lambda *x: list(x),
        'list?':   lambda x: isinstance(x,list),
        'map':     lambda *args: list(map(*args)),
        'max':     max,
        'min':     min,
        'not':     op.not_,
        'null?':   lambda x: x == [],
        'number?': lambda x: isinstance(x, (int, float)),
        'procedure?': callable,
        'round':   round,
        'symbol?': lambda x: isinstance(x, Symbol),
    })
    return env

################ Parsing: parse, tokenize, and read_from_tokens

def parse(program: str) -> Expression:
    "Read a Scheme expression from a string."
    return read_from_tokens(tokenize(program))


def tokenize(s: str) -> list[str]:
    "Convert a string into a list of tokens."
    return s.replace('(', ' ( ').replace(')', ' ) ').split()


def read_from_tokens(tokens: list[str]) -> Expression:
    "Read an expression from a sequence of tokens."
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF while reading')
    token = tokens.pop(0)
    if '(' == token:
        exp = []
        while tokens[0] != ')':
            exp.append(read_from_tokens(tokens))
        tokens.pop(0)  # discard ')'
        return exp
    elif ')' == token:
        raise SyntaxError('unexpected )')
    else:
        return parse_atom(token)


def parse_atom(token: str) -> Atom:
    "Numbers become numbers; every other token is a symbol."
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return Symbol(token)


################ Interaction: A REPL

def repl(prompt: str = 'lis.py> ') -> None:
    "A prompt-read-eval-print loop."
    global_env = standard_env()
    while True:
        val = evaluate(parse(input(prompt)), global_env)
        if val is not None:
            print(lispstr(val))


def lispstr(exp: object) -> str:
    "Convert a Python object back into a Lisp-readable string."
    if isinstance(exp, list):
        return '(' + ' '.join(map(lispstr, exp)) + ')'
    else:
        return str(exp)


################ eval

def evaluate(x: Expression, env: Environment) -> Any:
    "Evaluate an expression in an environment."
    if isinstance(x, Symbol):      # variable reference
        return env[x]
    elif not isinstance(x, list):  # constant literal
        return x
    elif x[0] == 'quote':          # (quote exp)
        (_, exp) = x
        return exp
    elif x[0] == 'if':             # (if test conseq alt)
        (_, test, consequence, alternative) = x
        if evaluate(test, env):
            return evaluate(consequence, env)
        else:
            return evaluate(alternative, env)
    elif x[0] == 'define':         # (define name exp)
        (_, name, exp) = x
        env[name] = evaluate(exp, env)
    elif x[0] == 'lambda':         # (lambda (parm…) body)
        (_, parms, *body) = x
        return Procedure(parms, body, env)
    else:                          # (proc arg…)
        proc = evaluate(x[0], env)
        args = [evaluate(exp, env) for exp in x[1:]]
        return proc(*args)
