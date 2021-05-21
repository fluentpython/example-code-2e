import warnings

class metaMetaBunch(type):
    """
    metaclass for new and improved "Bunch": implicitly defines
    __slots__, __init__ and __repr__ from variables bound in class scope.

    An instance of metaMetaBunch (a class whose metaclass is metaMetaBunch)
    defines only class-scope variables (and possibly special methods, but
    NOT __init__ and __repr__!).  metaMetaBunch removes those variables from
    class scope, snuggles them instead as items in a class-scope dict named
    __dflts__, and puts in the class a __slots__ listing those variables'
    names, an __init__ that takes as optional keyword arguments each of
    them (using the values in __dflts__ as defaults for missing ones), and
    a __repr__ that shows the repr of each attribute that differs from its
    default value (the output of __repr__ can be passed to __eval__ to make
    an equal instance, as per the usual convention in the matter).
    """

    def __new__(cls, classname, bases, classdict):
        """ Everything needs to be done in __new__, since type.__new__ is
            where __slots__ are taken into account.
        """

        # define as local functions the __init__ and __repr__ that we'll
        # use in the new class

        def __init__(self, **kw):
            """ Simplistic __init__: first set all attributes to default
                values, then override those explicitly passed in kw.
            """
            for k in self.__dflts__: setattr(self, k, self.__dflts__[k])
            for k in kw: setattr(self, k, kw[k])

        def __repr__(self):
            """ Clever __repr__: show only attributes that differ from the
                respective default values, for compactness.
            """
            rep = [ '%s=%r' % (k, getattr(self, k)) for k in self.__dflts__
                    if getattr(self, k) != self.__dflts__[k]
                  ]
            return '%s(%s)' % (classname, ', '.join(rep))

        # build the newdict that we'll use as class-dict for the new class
        newdict = { '__slots__':[], '__dflts__':{},
            '__init__':__init__, '__repr__':__repr__, }

        for k in classdict:
            if k.startswith('__'):
                # special methods &c: copy to newdict, warn about conflicts
                if k in newdict:
                    warnings.warn("Can't set attr %r in bunch-class %r" % (
                        k, classname))
                else:
                    newdict[k] = classdict[k]
            else:
                # class variables, store name in __slots__ and name and
                # value as an item in __dflts__
                newdict['__slots__'].append(k)
                newdict['__dflts__'][k] = classdict[k]

        # finally delegate the rest of the work to type.__new__
        return type.__new__(cls, classname, bases, newdict)


class MetaBunch(metaclass=metaMetaBunch):
    """ For convenience: inheriting from MetaBunch can be used to get
        the new metaclass (same as defining __metaclass__ yourself).
    """
    __metaclass__ = metaMetaBunch
