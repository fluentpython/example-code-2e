def tree(cls, level=0, last_sibling=True):
    yield cls, level, last_sibling
    subclasses = cls.__subclasses__()
    if subclasses:
        last = subclasses[-1]
    for sub_cls in subclasses:
        yield from tree(sub_cls, level+1, sub_cls is last)


def display(cls):
    for cls, level, _ in tree(cls):
        indent = ' ' * 4 * level
        print(f'{indent}{cls.__name__}')


if __name__ == '__main__':
    display(BaseException)
