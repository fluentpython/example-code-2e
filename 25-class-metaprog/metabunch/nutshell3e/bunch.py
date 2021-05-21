import collections
import warnings

class MetaBunch(type):
    """
    Metaclass for new and improved "Bunch": implicitly defines
    __slots__, __init__ and __repr__ from variables bound in
    class scope.
    A class statement for an instance of MetaBunch (i.e., for a
    class whose metaclass is MetaBunch) must define only
    class-scope data attributes (and possibly special methods, but
    NOT __init__ and __repr__).  MetaBunch removes the data
    attributes from class scope, snuggles them instead as items in
    a class-scope dict named __dflts__, and puts in the class a
    __slots__ with those attributes' names, an __init__ that takes
    as optional named arguments each of them (using the values in
    __dflts__ as defaults for missing ones), and a __repr__ that
    shows the repr of each attribute that differs from its default
    value (the output of __repr__ can be passed to __eval__ to make
    an equal instance, as per usual convention in the matter, if
    each non-default-valued attribute respects the convention too).

    In v3, the order of data attributes remains the same as in the
    class body; in v2, there is no such guarantee.
    """
    def __prepare__(name, *bases, **kwargs):
        # precious in v3—harmless although useless in v2
        return collections.OrderedDict()

    def __new__(mcl, classname, bases, classdict):
        """ Everything needs to be done in __new__, since
            type.__new__ is where __slots__ are taken into account.
        """
        # define as local functions the __init__ and __repr__ that
        # we'll use in the new class
        def __init__(self, **kw):
            """ Simplistic __init__: first set all attributes to
                default values, then override those explicitly
                passed in kw.
            """
            for k in self.__dflts__:
                setattr(self, k, self.__dflts__[k])
            for k in kw:
                setattr(self, k, kw[k])
        def __repr__(self):
            """ Clever __repr__: show only attributes that differ
                from default values, for compactness.
            """
            rep = ['{}={!r}'.format(k, getattr(self, k))
                    for k in self.__dflts__
                    if getattr(self, k) != self.__dflts__[k]
                  ]
            return '{}({})'.format(classname, ', '.join(rep))
        # build the newdict that we'll use as class-dict for the
        # new class
        newdict = { '__slots__':[], 
            '__dflts__':collections.OrderedDict(),
            '__init__':__init__, '__repr__':__repr__, }
        for k in classdict:
            if k.startswith('__') and k.endswith('__'):
                # dunder methods: copy to newdict, or warn
                # about conflicts
                if k in newdict:
                    warnings.warn(
                        "Can't set attr {!r} in bunch-class {!r}".
                        format(k, classname))
                else:
                    newdict[k] = classdict[k]
            else:
                # class variables, store name in __slots__, and
                # name and value as an item in __dflts__
                newdict['__slots__'].append(k)
                newdict['__dflts__'][k] = classdict[k]
        # finally delegate the rest of the work to type.__new__
        return super(MetaBunch, mcl).__new__(
                     mcl, classname, bases, newdict)

class Bunch(metaclass=MetaBunch):
    """ For convenience: inheriting from Bunch can be used to get
        the new metaclass (same as defining metaclass= yourself).

        In v2, remove the (metaclass=MetaBunch) above and add
        instead __metaclass__=MetaBunch as the class body.
    """
    pass
