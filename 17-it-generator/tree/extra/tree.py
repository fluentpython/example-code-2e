def tree(cls, level=0, last_in_level=True):
    yield cls.__name__, level, last_in_level
    subclasses = cls.__subclasses__()
    if subclasses:
    	last = subclasses[-1]
    for sub_cls in subclasses:
        yield from tree(sub_cls, level+1, sub_cls is last)


if __name__ == '__main__':
    for cls_name, level, _ in tree(BaseException):
        indent = ' ' * 4 * level
        print(f'{indent}{cls_name}')
