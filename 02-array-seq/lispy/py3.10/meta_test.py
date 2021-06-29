import operator as op

from lis import run

env_scm = """
(define standard-env (list
    (list (quote +) +)
    (list (quote -) -)
))
standard-env
"""

def test_env_build():
    got = run(env_scm)
    assert got == [['+', op.add], ['-', op.sub]]

scan_scm = """
(define l (quote (a b c)))
(define (scan what where)
    (if (null? where)
        ()
        (if (eq? what (car where))
            what
            (scan what (cdr where))))
)
"""

def test_scan():
    source = scan_scm + '(scan (quote a) l )'
    got = run(source)
    assert got == 'a'


def test_scan_not_found():
    source = scan_scm + '(scan (quote z) l )'
    got = run(source)
    assert got == []


lookup_scm = """
(define env (list
    (list (quote +) +)
    (list (quote -) -)
))
(define (lookup what where)
    (if (null? where)
        ()
        (if (eq? what (car (car where)))
            (car (cdr (car where)))
            (lookup what (cdr where))))
)
"""

def test_lookup():
    source = lookup_scm + '(lookup (quote +) env)'
    got = run(source)
    assert got == op.add


def test_lookup_not_found():
    source = lookup_scm + '(lookup (quote z) env )'
    got = run(source)
    assert got == []

