import httpx

def tree(cls, level=0):
    yield cls.__name__, level
    for sub_cls in cls.__subclasses__():
        yield from tree(sub_cls, level+1)


def display(cls):
    for cls_name, level in tree(cls):
        indent = ' ' * 4 * level
        print(f'{indent}{cls_name}')


def find_roots(module):
    exceptions = []
    for name in dir(module):
        obj = getattr(module, name)
        if isinstance(obj, type) and issubclass(obj, BaseException):
            exceptions.append(obj)
    roots = []
    for exc in exceptions:
        root = True
        for other in exceptions:
            if exc is not other and issubclass(exc, other):
                root = False
                break
        if root:
            roots.append(exc)
    return roots


def main():
    for exc in find_roots(httpx):
        display(exc)

if __name__ == '__main__':
    main()
