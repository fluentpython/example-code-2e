# pseudocode for object construction
def make(the_class, *args, **kwargs):
    new_object = the_class.__new__(the_class, *args, **kwargs)
    if isinstance(new_object, the_class):
        the_class.__init__(new_object, *args, **kwargs)
    return new_object

# the following statements are roughly equivalent
x = Foo('bar')
x = make(Foo, 'bar')
