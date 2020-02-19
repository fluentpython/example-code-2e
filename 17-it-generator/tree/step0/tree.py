def tree(cls):
    yield cls.__name__


if __name__ == '__main__':
    for cls_name in tree(BaseException):
        print(cls_name)
