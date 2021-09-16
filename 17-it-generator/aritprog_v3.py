# tag::ARITPROG_ITERTOOLS[]
import itertools


def aritprog_gen(begin, step, end=None):
    first = type(begin + step)(begin)
    ap_gen = itertools.count(first, step)
    if end is None:
        return ap_gen
    return itertools.takewhile(lambda n: n < end, ap_gen)
# end::ARITPROG_ITERTOOLS[]
