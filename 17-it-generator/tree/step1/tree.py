def tree(cls):
    yield cls.__name__, 0                        # <1>
    for sub_cls in cls.__subclasses__():         # <2>
        yield sub_cls.__name__, 1                # <3>


if __name__ == '__main__':
    for cls_name, level in tree(BaseException):
        indent = ' ' * 4 * level                 # <4>
        print(f'{indent}{cls_name}')
