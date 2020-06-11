#!/usr/bin/env python3

import sys
from array import array
from typing import Mapping, MutableSequence, Callable, Iterable, Sequence, Union, Any


OPERATORS: Mapping[str, Callable[[float, float], float]] = {
    '+': lambda a, b: a + b,
    '-': lambda a, b: a - b,
    '*': lambda a, b: a * b,
    '/': lambda a, b: a / b,
    '^': lambda a, b: a ** b,
}


Stack = MutableSequence[float]


def parse_token(token: str) -> Union[str, float]:
    try:
        return float(token)
    except ValueError:
        return token


def evaluate(tokens: Iterable[str], stack: Stack) -> None:
    for token in tokens:
        atom = parse_token(token)
        if isinstance(atom, float):
            stack.append(atom)
        else:  # not float, must be operator
            op = OPERATORS[atom]
            x, y = stack.pop(), stack.pop()
            result = op(y, x)
            stack.append(result)


def display(s: Stack) -> str:
    items = (repr(n) for n in s)
    return ' │ '.join(items) + ' →'


def repl(input_fn: Callable[[Any], str] = input) -> None:
    """Read-Eval-Print-Loop"""

    print('Use CTRL+C to quit.', file=sys.stderr)
    stack: Stack = array('d')

    while True:
        try:
            line = input_fn('> ')              # Read
        except (EOFError, KeyboardInterrupt):
            break
        try:
            evaluate(line.split(), stack)      # Eval
        except IndexError:
            print('*** Not enough arguments.', file=sys.stderr)
        except KeyError as exc:
            print('*** Unknown operator:', exc.args[0], file=sys.stderr)
        print(display(stack))                  # Print

    print()


if __name__ == '__main__':
    repl()
