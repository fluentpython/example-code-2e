from typing import Optional

from pytest import mark, fixture

from lis import parse, evaluate, Expression, Environment, standard_env

############################################################# tests for parse

@mark.parametrize( 'source, expected', [
    ('7', 7),
    ('x', 'x'),
    ('(sum 1 2 3)', ['sum', 1, 2, 3]),
    ('(+ (* 2 100) (* 1 10))', ['+', ['*', 2, 100], ['*', 1, 10]]),
    ('99 100', 99),  # parse stops at the first complete expression
    ('(a)(b)', ['a']),
])
def test_parse(source: str, expected: Expression) -> None:
    got = parse(source)
    assert got == expected


########################################################## tests for evaluate

# Norvig's tests are not isolated: they assume the
# same environment from first to last test.
global_env_for_first_test = standard_env()

@mark.parametrize( 'source, expected', [
    ("(quote (testing 1 (2.0) -3.14e159))", ['testing', 1, [2.0], -3.14e159]),
    ("(+ 2 2)", 4),
    ("(+ (* 2 100) (* 1 10))", 210),
    ("(if (> 6 5) (+ 1 1) (+ 2 2))", 2),
    ("(if (< 6 5) (+ 1 1) (+ 2 2))", 4),
    ("(define x 3)", None),
    ("x", 3),
    ("(+ x x)", 6),
    ("((lambda (x) (+ x x)) 5)", 10),
    ("(define twice (lambda (x) (* 2 x)))", None),
    ("(twice 5)", 10),
    ("(define compose (lambda (f g) (lambda (x) (f (g x)))))", None),
    ("((compose list twice) 5)", [10]),
    ("(define repeat (lambda (f) (compose f f)))", None),
    ("((repeat twice) 5)", 20),
    ("((repeat (repeat twice)) 5)", 80),
    ("(define fact (lambda (n) (if (<= n 1) 1 (* n (fact (- n 1))))))", None),
    ("(fact 3)", 6),
    ("(fact 50)", 30414093201713378043612608166064768844377641568960512000000000000),
    ("(define abs (lambda (n) ((if (> n 0) + -) 0 n)))", None),
    ("(list (abs -3) (abs 0) (abs 3))", [3, 0, 3]),
    ("""(define combine (lambda (f)
            (lambda (x y)
                (if (null? x) (quote ())
                    (f (list (car x) (car y))
                        ((combine f) (cdr x) (cdr y)))))))""", None),
    ("(define zip (combine cons))", None),
    ("(zip (list 1 2 3 4) (list 5 6 7 8))", [[1, 5], [2, 6], [3, 7], [4, 8]]),
    ("""(define riff-shuffle (lambda (deck)
            (begin
                (define take (lambda (n seq) (if (<= n 0) (quote ()) (cons (car seq) (take (- n 1) (cdr seq))))))
                (define drop (lambda (n seq) (if (<= n 0) seq (drop (- n 1) (cdr seq)))))
                (define mid (lambda (seq) (/ (length seq) 2)))
                ((combine append) (take (mid deck) deck) (drop (mid deck) deck)))))""", None),
    ("(riff-shuffle (list 1 2 3 4 5 6 7 8))", [1, 5, 2, 6, 3, 7, 4, 8]),
    ("((repeat riff-shuffle) (list 1 2 3 4 5 6 7 8))",  [1, 3, 5, 7, 2, 4, 6, 8]),
    ("(riff-shuffle (riff-shuffle (riff-shuffle (list 1 2 3 4 5 6 7 8))))", [1,2,3,4,5,6,7,8]),
])
def test_evaluate(source: str, expected: Optional[Expression]) -> None:
    got = evaluate(parse(source), global_env_for_first_test)
    assert got == expected


@fixture
def std_env() -> Environment:
    return standard_env()

# tests for cases in evaluate

def test_evaluate_variable() -> None:
    env = Environment({'x': 10})
    source = 'x'
    expected = 10
    got = evaluate(parse(source), env)
    assert got == expected


def test_evaluate_literal(std_env: Environment) -> None:
    source = '3.3'
    expected = 3.3
    got = evaluate(parse(source), std_env)
    assert got == expected


def test_evaluate_quote(std_env: Environment) -> None:
    source = '(quote (1.1 is not 1))'
    expected = [1.1, 'is', 'not', 1]
    got = evaluate(parse(source), std_env)
    assert got == expected


def test_evaluate_if_true(std_env: Environment) -> None:
    source = '(if 1 10 no-such-thing)'
    expected = 10
    got = evaluate(parse(source), std_env)
    assert got == expected


def test_evaluate_if_false(std_env: Environment) -> None:
    source = '(if 0 no-such-thing 20)'
    expected = 20
    got = evaluate(parse(source), std_env)
    assert got == expected


def test_define(std_env: Environment) -> None:
    source = '(define answer (* 6 7))'
    got = evaluate(parse(source), std_env)
    assert got is None
    assert std_env['answer'] == 42


def test_lambda(std_env: Environment) -> None:
    source = '(lambda (a b) (if (>= a b) a b))'
    func = evaluate(parse(source), std_env)
    assert func.parms == ['a', 'b']
    assert func.body == [['if', ['>=', 'a', 'b'], 'a', 'b']]
    assert func.env is std_env
    assert func(1, 2) == 2
    assert func(3, 2) == 3


def test_begin(std_env: Environment) -> None:
    source = """
        (begin
            (define x (* 2 3))
            (* x 7)
        )
        """
    got = evaluate(parse(source), std_env)
    assert got == 42


def test_invocation_builtin_car(std_env: Environment) -> None:
    source = '(car (quote (11 22 33)))'
    got = evaluate(parse(source), std_env)
    assert got == 11


def test_invocation_builtin_append(std_env: Environment) -> None:
    source = '(append (quote (a b)) (quote (c d)))'
    got = evaluate(parse(source), std_env)
    assert got == ['a', 'b', 'c', 'd']


def test_invocation_builtin_map(std_env: Environment) -> None:
    source = '(map (lambda (x) (* x 2)) (quote (1 2 3))))'
    got = evaluate(parse(source), std_env)
    assert got == [2, 4, 6]


def test_invocation_user_procedure(std_env: Environment) -> None:
    source = """
        (begin
            (define max (lambda (a b) (if (>= a b) a b)))
            (max 22 11)
        )
        """
    got = evaluate(parse(source), std_env)
    assert got == 22


def test_define_function(std_env: Environment) -> None:
    source = '(define (max a b) (if (>= a b) a b))'
    got = evaluate(parse(source), std_env)
    assert got is None
    max_fn = std_env['max']
    assert max_fn.parms == ['a', 'b']
    assert max_fn.body == [['if', ['>=', 'a', 'b'], 'a', 'b']]
    assert max_fn.env is std_env
    assert max_fn(1, 2) == 2
    assert max_fn(3, 2) == 3
