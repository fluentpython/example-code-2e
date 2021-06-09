################ Lispy: Scheme Interpreter in Python 3.9

## (c) Peter Norvig, 2010-18; See http://norvig.com/lispy.html
## Minor edits for Fluent Python, Second Edition (O'Reilly, 2021)
## by Luciano Ramalho, adding type hints and pattern matching.

################ Imports and Types

import math
import operator as op
from collections import ChainMap
from collections.abc import MutableMapping
from typing import Any, TypeAlias

Atom: TypeAlias = float | int | str
Expression: TypeAlias = Atom | list

Environment: TypeAlias = MutableMapping[str, object]


class Procedure:
    "A user-defined Scheme procedure."

    def __init__(self, parms: list[str], body: Expression, env: Environment):
        self.parms, self.body, self.env = parms, body, env

    def __call__(self, *args: Expression) -> Any:
        env: Environment = ChainMap(dict(zip(self.parms, args)), self.env)
        return evaluate(self.body, env)


################ Global Environment


def standard_env() -> Environment:
    "An environment with some Scheme standard procedures."
    env: Environment = {}
    env.update(vars(math))   # sin, cos, sqrt, pi, ...
    env.update(
        {
            '+': op.add,
            '-': op.sub,
            '*': op.mul,
            '/': op.truediv,
            '>': op.gt,
            '<': op.lt,
            '>=': op.ge,
            '<=': op.le,
            '=': op.eq,
            'abs': abs,
            'append': op.add,
            'apply': lambda proc, args: proc(*args),
            'begin': lambda *x: x[-1],
            'car': lambda x: x[0],
            'cdr': lambda x: x[1:],
            'cons': lambda x, y: [x] + y,
            'eq?': op.is_,
            'equal?': op.eq,
            'length': len,
            'list': lambda *x: list(x),
            'list?': lambda x: isinstance(x, list),
            'map': lambda *args: list(map(*args)),
            'max': max,
            'min': min,
            'not': op.not_,
            'null?': lambda x: x == [],
            'number?': lambda x: isinstance(x, (int, float)),
            'procedure?': callable,
            'round': round,
            'symbol?': lambda x: isinstance(x, str),
        }
    )
    return env


global_env: Environment = standard_env()

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
        L = []
        while tokens[0] != ')':
            L.append(read_from_tokens(tokens))
        tokens.pop(0)   # pop off ')'
        return L
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
            return str(token)


################ Interaction: A REPL


def repl(prompt: str = 'lis.py> ') -> None:
    "A prompt-read-evaluate-print loop."
    while True:
        val = evaluate(parse(input(prompt)))
        if val is not None:
            print(lispstr(val))


def lispstr(exp: object) -> str:
    "Convert a Python object back into a Lisp-readable string."
    if isinstance(exp, list):
        return '(' + ' '.join(map(lispstr, exp)) + ')'
    else:
        return str(exp)


################ eval


def evaluate(x: Expression, env: Environment = global_env) -> Any:
    "Evaluate an expression in an environment."
    match x:
        case str():                               # variable reference
            return env[x]
        case literal if not isinstance(x, list):  # constant literal
            return literal
        case ['quote', exp]:                      # (quote exp)
            return exp
        case ['if', test, conseq, alt]:           # (if test conseq alt)
            exp = conseq if evaluate(test, env) else alt
            return evaluate(exp, env)
        case ['define', var, exp]:                # (define var exp)
            env[var] = evaluate(exp, env)
        case ['lambda', parms, body]:             # (lambda (var...) body)
            return Procedure(parms, body, env)
        case [op, *args]:                         # (proc arg...)
            proc = evaluate(op, env)
            values = (evaluate(arg, env) for arg in args)
            return proc(*values)
