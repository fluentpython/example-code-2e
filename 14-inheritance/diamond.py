"""
diamond1.py: Demo of diamond-shaped class graph.

# tag::LEAF_MRO[]
>>> Leaf.__mro__  # doctest:+NORMALIZE_WHITESPACE
    (<class 'diamond1.Leaf'>, <class 'diamond1.A'>, <class 'diamond1.B'>,
     <class 'diamond1.Root'>, <class 'object'>)

# end::LEAF_MRO[]

# tag::DIAMOND_CALLS[]
    >>> leaf1 = Leaf()  # <1>
    >>> leaf1.ping()    # <2>
    <instance of Leaf>.ping() in Leaf
    <instance of Leaf>.ping() in A
    <instance of Leaf>.ping() in B
    <instance of Leaf>.ping() in Root

    >>> leaf1.pong()   # <3>
    <instance of Leaf>.pong() in A
    <instance of Leaf>.pong() in B

# end::DIAMOND_CALLS[]
"""

# tag::DIAMOND_CLASSES[]
class Root:  # <1>
    def ping(self):
        print(f'{self}.ping() in Root')

    def pong(self):
        print(f'{self}.pong() in Root')

    def __repr__(self):
        cls_name = type(self).__name__
        return f'<instance of {cls_name}>'


class A(Root):  # <2>
    def ping(self):
        print(f'{self}.ping() in A')
        super().ping()

    def pong(self):
        print(f'{self}.pong() in A')
        super().pong()


class B(Root):  # <3>
    def ping(self):
        print(f'{self}.ping() in B')
        super().ping()

    def pong(self):
        print(f'{self}.pong() in B')


class Leaf(A, B):  # <4>
    def ping(self):
        print(f'{self}.ping() in Leaf')
        super().ping()
# end::DIAMOND_CLASSES[]
