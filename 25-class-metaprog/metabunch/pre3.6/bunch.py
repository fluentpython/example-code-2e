import collections
import warnings

class MetaBunch(type):
    def __prepare__(name, *bases, **kwargs):
        return collections.OrderedDict()

    def __new__(meta_cls, cls_name, bases, cls_dict):
        def __init__(self, **kw):
            for k in self.__defaults__:
                setattr(self, k, self.__defaults__[k])
            for k in kw:
                setattr(self, k, kw[k])

        def __repr__(self):
            rep = ['{}={!r}'.format(k, getattr(self, k))
                    for k in self.__defaults__
                    if getattr(self, k) != self.__defaults__[k]
                  ]
            return '{}({})'.format(cls_name, ', '.join(rep))

        new_dict = { '__slots__':[], 
            '__defaults__':collections.OrderedDict(),
            '__init__':__init__, '__repr__':__repr__, }

        for k in cls_dict:
            if k.startswith('__') and k.endswith('__'):
                if k in new_dict:
                    warnings.warn(
                        "Can't set attr {!r} in bunch-class {!r}".
                        format(k, cls_name))
                else:
                    new_dict[k] = cls_dict[k]
            else:
                new_dict['__slots__'].append(k)
                new_dict['__defaults__'][k] = cls_dict[k]

        return super().__new__(meta_cls, cls_name, bases, new_dict)

class Bunch(metaclass=MetaBunch):
    pass
