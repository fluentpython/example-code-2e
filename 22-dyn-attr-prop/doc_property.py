"""
Example of property documentation

    >>> f = Foo()
    >>> f.bar = 77
    >>> f.bar
    77
    >>> Foo.bar.__doc__
    'The bar attribute'
"""

# tag::DOC_PROPERTY[]
class Foo:

    @property
    def bar(self):
        """The bar attribute"""
        return self.__dict__['bar']

    @bar.setter
    def bar(self, value):
        self.__dict__['bar'] = value
# end::DOC_PROPERTY[]
