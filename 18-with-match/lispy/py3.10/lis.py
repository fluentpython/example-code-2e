#!/usr/bin/env python

################ Lispy: Scheme Interpreter in Python 3.10

## (c) Peter Norvig, 2010-18; See http://norvig.com/lispy.html
## Minor edits for Fluent Python, Second Edition (O'Reilly, 2021)
## by Luciano Ramalho, adding type hints and pattern matching.


################ Imports and Types

# tag::IMPORTS[]
import math
import operator as op
from collections import ChainMap
from itertools import chain
from typing import Any, TypeAlias, NoReturn

Symbol: TypeAlias = str
Atom: TypeAlias = float | int | Symbol
Expression: TypeAlias = Atom | list
# end::IMPORTS[]


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


################ Global Environment

# tag::ENV_CLASS[]
class Environment(ChainMap[Symbol, Any]):
    "A ChainMap that allows changing an item in-place."

    def change(self, key: Symbol, value: Any) -> None:
        "Find where key is defined and change the value there."
        for map in self.maps:
            if key in map:
                map[key] = value  # type: ignore[index]
                return
        raise KeyError(key)
# end::ENV_CLASS[]

def standard_env() -> Environment:
    "An environment with some Scheme standard procedures."
    env = Environment()
    env.update(vars(math))   # sin, cos, sqrt, pi, ...
    env.update({
            '+': op.add,
            '-': op.sub,
            '*': op.mul,
            '/': op.truediv,
            'quotient': op.floordiv,
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
            'display': lambda x: print(lispstr(x)),
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


################ Interaction: A REPL

# tag::REPL[]
def repl(prompt: str = 'lis.py> ') -> NoReturn:
    "A prompt-read-eval-print loop."
    global_env = Environment({}, standard_env())
    while True:
        ast = parse(input(prompt))
        val = evaluate(ast, global_env)
        if val is not None:
            print(lispstr(val))

def lispstr(exp: object) -> str:
    "Convert a Python object back into a Lisp-readable string."
    if isinstance(exp, list):
        return '(' + ' '.join(map(lispstr, exp)) + ')'
    else:
        return str(exp)
# end::REPL[]


################ Evaluator

# tag::EVALUATE[]
KEYWORDS = ['quote', 'if', 'lambda', 'define', 'set!']

def evaluate(exp: Expression, env: Environment) -> Any:
    "Evaluate an expression in an environment."
    match exp:
        case int(x) | float(x):
            return x
        case Symbol(var):
            return env[var]
        case ['quote', x]:
            return x
        case ['if', test, consequence, alternative]:
            if evaluate(test, env):
                return evaluate(consequence, env)
            else:
                return evaluate(alternative, env)
        case ['lambda', [*parms], *body] if body:
            return Procedure(parms, body, env)
        case ['define', Symbol(name), value_exp]:
            env[name] = evaluate(value_exp, env)
        case ['define', [Symbol(name), *parms], *body] if body:
            env[name] = Procedure(parms, body, env)
        case ['set!', Symbol(name), value_exp]:
            env.change(name, evaluate(value_exp, env))
        case [func_exp, *args] if func_exp not in KEYWORDS:
            proc = evaluate(func_exp, env)
            values = [evaluate(arg, env) for arg in args]
            return proc(*values)
        case _:
            raise SyntaxError(lispstr(exp))
# end::EVALUATE[]

# tag::PROCEDURE[]
class Procedure:
    "A user-defined Scheme procedure."

    def __init__(  # <1>
        self, parms: list[Symbol], body: list[Expression], env: Environment
    ):
        self.parms = parms  # <2>
        self.body = body
        self.env = env

    def __call__(self, *args: Expression) -> Any:  # <3>
        local_env = dict(zip(self.parms, args))  # <4>
        env = Environment(local_env, self.env)  # <5>
        for exp in self.body:  # <6>
            result = evaluate(exp, env)
        return result  # <7>
# end::PROCEDURE[]


################ command-line interface

def run(source: str) -> Any:
    global_env = Environment({}, standard_env())
    tokens = tokenize(source)
    while tokens:
        exp = read_from_tokens(tokens)
        result = evaluate(exp, global_env)
    return result

def main(args: list[str]) -> None:
    if len(args) == 1:
        with open(args[0]) as fp:
            run(fp.read())
    else:
        repl()

if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
