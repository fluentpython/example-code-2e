def tree(cls, level=0):
    yield cls.__name__, level
    for sub_cls in cls.__subclasses__():
        yield from tree(sub_cls, level + 1)


if __name__ == '__main__':
    for cls_name, level in tree(BaseException):
        indent = ' ' * 4 * level
        print(f'{indent}{cls_name}')
