# tag::METALIB_TOP[]
print('% metalib module start')

import collections

class NosyDict(collections.UserDict):
    def __setitem__(self, key, value):
        args = (self, key, value)
        print(f'% NosyDict.__setitem__{args!r}')
        super().__setitem__(key, value)

    def __repr__(self):
        return '<NosyDict instance>'
# end::METALIB_TOP[]

# tag::METALIB_BOTTOM[]
class MetaKlass(type):
    print('% MetaKlass body')

    @classmethod  # <1>
    def __prepare__(meta_cls, cls_name, bases):  # <2>
        args = (meta_cls, cls_name, bases)
        print(f'% MetaKlass.__prepare__{args!r}')
        return NosyDict()  # <3>

    def __new__(meta_cls, cls_name, bases, cls_dict):  # <4>
        args = (meta_cls, cls_name, bases, cls_dict)
        print(f'% MetaKlass.__new__{args!r}')
        def inner_2(self):
            print(f'% MetaKlass.__new__:inner_2({self!r})')

        cls = super().__new__(meta_cls, cls_name, bases, cls_dict.data)  # <5>

        cls.method_c = inner_2  # <6>

        return cls  # <7>

    def __repr__(cls):  # <8>
        cls_name = cls.__name__
        return f"<class {cls_name!r} built by MetaKlass>"

print('% metalib module end')
# end::METALIB_BOTTOM[]
