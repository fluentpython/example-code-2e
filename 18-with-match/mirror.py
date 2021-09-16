"""
A "mirroring" ``stdout`` context.

While active, the context manager reverses text output to
``stdout``::

# tag::MIRROR_DEMO_1[]

    >>> from mirror import LookingGlass
    >>> with LookingGlass() as what:  # <1>
    ...      print('Alice, Kitty and Snowdrop')  # <2>
    ...      print(what)
    ...
    pordwonS dna yttiK ,ecilA
    YKCOWREBBAJ
    >>> what  # <3>
    'JABBERWOCKY'
    >>> print('Back to normal.')  # <4>
    Back to normal.

# end::MIRROR_DEMO_1[]


This exposes the context manager operation::

# tag::MIRROR_DEMO_2[]

    >>> from mirror import LookingGlass
    >>> manager = LookingGlass()  # <1>
    >>> manager  # doctest: +ELLIPSIS
    <mirror.LookingGlass object at 0x...>
    >>> monster = manager.__enter__()  # <2>
    >>> monster == 'JABBERWOCKY'  # <3>
    eurT
    >>> monster
    'YKCOWREBBAJ'
    >>> manager  # doctest: +ELLIPSIS
    >... ta tcejbo ssalGgnikooL.rorrim<
    >>> manager.__exit__(None, None, None)  # <4>
    >>> monster
    'JABBERWOCKY'

# end::MIRROR_DEMO_2[]

The context manager can handle and "swallow" exceptions.

# tag::MIRROR_DEMO_3[]

    >>> from mirror import LookingGlass
    >>> with LookingGlass():
    ...      print('Humpty Dumpty')
    ...      x = 1/0  # <1>
    ...      print('END')  # <2>
    ...
    ytpmuD ytpmuH
    Please DO NOT divide by zero!
    >>> with LookingGlass():
    ...      print('Humpty Dumpty')
    ...      x = no_such_name  # <1>
    ...      print('END')  # <2>
    ...
    Traceback (most recent call last):
      ...
    NameError: name 'no_such_name' is not defined

# end::MIRROR_DEMO_3[]

"""


# tag::MIRROR_EX[]
import sys

class LookingGlass:

    def __enter__(self):  # <1>
        self.original_write = sys.stdout.write  # <2>
        sys.stdout.write = self.reverse_write  # <3>
        return 'JABBERWOCKY'  # <4>

    def reverse_write(self, text):  # <5>
        self.original_write(text[::-1])

    def __exit__(self, exc_type, exc_value, traceback):  # <6>
        sys.stdout.write = self.original_write  # <7>
        if exc_type is ZeroDivisionError:  # <8>
            print('Please DO NOT divide by zero!')
            return True  # <9>
        # <10>
# end::MIRROR_EX[]
