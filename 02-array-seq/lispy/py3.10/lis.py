################ Lispy: Scheme Interpreter in Python 3.10

## (c) Peter Norvig, 2010-18; See http://norvig.com/lispy.html
## Minor edits for Fluent Python, Second Edition (O'Reilly, 2021)
## by Luciano Ramalho, adding type hints and pattern matching.

################ Imports and Types

import math
import operator as op
from collections import ChainMap
from collections.abc import MutableMapping, Iterator
from itertools import chain
from typing import Any, TypeAlias

Symbol: TypeAlias = str
Atom: TypeAlias = float | int | Symbol
Expression: TypeAlias = Atom | list

Environment: TypeAlias = MutableMapping[Symbol, object]


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
            '+': op.add,
            '-': op.sub,
            '*': op.mul,
            '/': op.truediv,
            '//': op.floordiv,
            '>': op.gt,
            '<': op.lt,
            '>=': op.ge,
            '<=': op.le,
            '=': op.eq,
            'abs': abs,
            'append': lambda *args: list(chain(*args)),
            'apply': lambda proc, args: proc(*args),
            'begin': lambda *x: x[-1],
            'car': lambda x: x[0],
            'cdr': lambda x: x[1:],
            'cons': lambda x, y: [x] + y,
            'eq?': op.is_,
            'equal?': op.eq,
            'filter': lambda *args: list(filter(*args)),
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
    "A prompt-read-evaluate-print loop."
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

# tag::EVALUATE[]
def evaluate(exp: Expression, env: Environment) -> Any:
    "Evaluate an expression in an environment."
    match exp:
        case int(x) | float(x):
            return x
        case Symbol(var):
            return env[var]
        case []:
            return []
        case ['quote', exp]:
            return exp
        case ['if', test, consequence, alternative]:
            if evaluate(test, env):
                return evaluate(consequence, env)
            else:
                return evaluate(alternative, env)
        case ['define', Symbol(var), value_exp]:
            env[var] = evaluate(value_exp, env)
        case ['define', [Symbol(name), *parms], *body]:
            env[name] = Procedure(parms, body, env)
        case ['lambda', [*parms], *body]:
            return Procedure(parms, body, env)
        case [op, *args]:
            proc = evaluate(op, env)
            values = [evaluate(arg, env) for arg in args]
            return proc(*values)
        case _:
            raise SyntaxError(repr(exp))
# end::EVALUATE[]


################ non-interactive execution


def run_lines(source: str) -> Iterator[Any]:
    global_env: Environment = standard_env()
    tokens = tokenize(source)
    while tokens:
        exp = read_from_tokens(tokens)
        yield evaluate(exp, global_env)


def run(source: str) -> Any:
    for result in run_lines(source):
        pass
    return result
