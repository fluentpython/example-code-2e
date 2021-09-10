# tag::BUILDERLIB_TOP[]
print('@ builderlib module start')

class Builder:  # <1>
    print('@ Builder body')

    def __init_subclass__(cls):  # <2>
        print(f'@ Builder.__init_subclass__({cls!r})')

        def inner_0(self):  # <3>
            print(f'@ SuperA.__init_subclass__:inner_0({self!r})')

        cls.method_a = inner_0

    def __init__(self):
        super().__init__()
        print(f'@ Builder.__init__({self!r})')


def deco(cls):  # <4>
    print(f'@ deco({cls!r})')

    def inner_1(self):  # <5>
        print(f'@ deco:inner_1({self!r})')

    cls.method_b = inner_1
    return cls  # <6>
# end::BUILDERLIB_TOP[]

# tag::BUILDERLIB_BOTTOM[]
class Descriptor:  # <1>
    print('@ Descriptor body')

    def __init__(self):  # <2>
        print(f'@ Descriptor.__init__({self!r})')

    def __set_name__(self, owner, name):  # <3>
        args = (self, owner, name)
        print(f'@ Descriptor.__set_name__{args!r}')

    def __set__(self, instance, value):  # <4>
        args = (self, instance, value)
        print(f'@ Descriptor.__set__{args!r}')

    def __repr__(self):
        return '<Descriptor instance>'


print('@ builderlib module end')
# end::BUILDERLIB_BOTTOM[]
