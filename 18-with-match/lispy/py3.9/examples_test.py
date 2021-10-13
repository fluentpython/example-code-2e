"""
Doctests for `parse`
--------------------

# tag::PARSE[]
>>> from lis import parse
>>> parse('1.5')
1.5
>>> parse('ni!')
'ni!'
>>> parse('(gcd 18 45)')
['gcd', 18, 45]
>>> parse('''
... (define double
...     (lambda (n)
...         (* n 2)))
... ''')
['define', 'double', ['lambda', ['n'], ['*', 'n', 2]]]

# end::PARSE[]

Doctest for `Environment`
-------------------------

# tag::ENVIRONMENT[]
>>> from lis import Environment
>>> inner_env = {'a': 2}
>>> outer_env = {'a': 0, 'b': 1}
>>> env = Environment(inner_env, outer_env)
>>> env['a'] = 111  # <1>
>>> env['c'] = 222
>>> env
Environment({'a': 111, 'c': 222}, {'a': 0, 'b': 1})
>>> env.change('b', 333)  # <2>
>>> env
Environment({'a': 111, 'c': 222}, {'a': 0, 'b': 333})

# end::ENVIRONMENT[]

Doctests for `evaluate`
-----------------------

# tag::EVAL_NUMBER[]
>>> from lis import parse, evaluate, standard_env
>>> evaluate(parse('1.5'), {})
1.5

# end::EVAL_NUMBER[]

# tag::EVAL_SYMBOL[]
>>> from lis import standard_env
>>> evaluate(parse('+'), standard_env())
<built-in function add>
>>> evaluate(parse('ni!'), standard_env())
Traceback (most recent call last):
    ...
KeyError: 'ni!'

# end::EVAL_SYMBOL[]


# tag::EVAL_QUOTE[]
>>> evaluate(parse('(quote no-such-name)'), standard_env())
'no-such-name'
>>> evaluate(parse('(quote (99 bottles of beer))'), standard_env())
[99, 'bottles', 'of', 'beer']
>>> evaluate(parse('(quote (/ 10 0))'), standard_env())
['/', 10, 0]

# end::EVAL_QUOTE[]

# tag::EVAL_IF[]
>>> evaluate(parse('(if (= 3 3) 1 0))'), standard_env())
1
>>> evaluate(parse('(if (= 3 4) 1 0))'), standard_env())
0

# end::EVAL_IF[]


# tag::EVAL_LAMBDA[]
>>> expr = '(lambda (a b) (* (/ a b) 100))'
>>> f = evaluate(parse(expr), standard_env())
>>> f  # doctest: +ELLIPSIS
<lis.Procedure object at 0x...>
>>> f(15, 20)
75.0

# end::EVAL_LAMBDA[]

# tag::EVAL_DEFINE[]
>>> global_env = standard_env()
>>> evaluate(parse('(define answer (* 7 6))'), global_env)
>>> global_env['answer']
42

# end::EVAL_DEFINE[]

# tag::EVAL_DEFUN[]
>>> global_env = standard_env()
>>> percent = '(define (% a b) (* (/ a b) 100))'
>>> evaluate(parse(percent), global_env)
>>> global_env['%']  # doctest: +ELLIPSIS
<lis.Procedure object at 0x...>
>>> global_env['%'](170, 200)
85.0

# end::EVAL_DEFUN[]

function call:

# tag::EVAL_CALL[]
>>> evaluate(parse('(% (* 12 14) (- 500 100))'), global_env)
42.0

# end::EVAL_CALL[]

# tag::EVAL_SYNTAX_ERROR[]
>>> evaluate(parse('(lambda is not like this)'), standard_env())
Traceback (most recent call last):
    ...
SyntaxError: (lambda is not like this)

# end::EVAL_SYNTAX_ERROR[]

"""

import math

from lis import run


fact_src = """
(define (! n)
    (if (< n 2)
        1
        (* n (! (- n 1)))
    )
)
(! 42)
"""
def test_factorial():
    got = run(fact_src)
    assert got == 1405006117752879898543142606244511569936384000000000
    assert got == math.factorial(42)


gcd_src = """
(define (mod m n)
    (- m (* n (quotient m n))))
(define (gcd m n)
    (if (= n 0)
        m
        (gcd n (mod m n))))
(display (gcd 18 45))
"""
def test_gcd(capsys):
    run(gcd_src)
    captured = capsys.readouterr()
    assert captured.out == '9\n'


quicksort_src = """
(define (quicksort lst)
    (if (null? lst)
        lst
        (begin
            (define pivot (car lst))
            (define rest (cdr lst))
            (append
                (quicksort
                    (filter (lambda (x) (< x pivot)) rest))
                (list pivot)
                (quicksort
                    (filter (lambda (x) (>= x pivot)) rest)))
        )
    )
)
(quicksort (list 2 1 6 3 4 0 8 9 7 5))
"""
def test_quicksort():
    got = run(quicksort_src)
    assert got == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


# Example from Structure and Interpretation of Computer Programs
# https://mitpress.mit.edu/sites/default/files/sicp/full-text/sicp/book/node12.html

newton_src = """
(define (sqrt x)
    (sqrt-iter 1.0 x))
(define (sqrt-iter guess x)
    (if (good-enough? guess x)
        guess
        (sqrt-iter (improve guess x) x)))
(define (good-enough? guess x)
    (< (abs (- (* guess guess) x)) 0.001))
(define (improve guess x)
    (average guess (/ x guess)))
(define (average x y)
    (/ (+ x y) 2))
(sqrt 123454321)
"""
def test_newton():
    got = run(newton_src)
    assert math.isclose(got, 11111)


closure_src = """
(define (make-adder increment)
    (lambda (x) (+ increment x))
)
(define inc (make-adder 1))
(inc 99)
"""
def test_closure():
    got = run(closure_src)
    assert got == 100

closure_with_change_src = """
(define (make-counter)
    (define n 0)
    (lambda ()
        (set! n (+ n 1))
        n)
)
(define counter (make-counter))
(display (counter))
(display (counter))
(display (counter))
"""
def test_closure_with_change(capsys):
    run(closure_with_change_src)
    captured = capsys.readouterr()
    assert captured.out == '1\n2\n3\n'



# tag::RUN_AVERAGER[]
closure_averager_src = """
(define (make-averager)
    (define count 0)
    (define total 0)
    (lambda (new-value)
        (set! count (+ count 1))
        (set! total (+ total new-value))
        (/ total count)
    )
)
(define avg (make-averager))
(avg 10)
(avg 11)
(avg 15)
"""
def test_closure_averager():
    got = run(closure_averager_src)
    assert got == 12.0
# end::RUN_AVERAGER[]
