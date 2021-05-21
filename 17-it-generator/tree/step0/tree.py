def tree(cls):
    yield cls.__name__


def display(cls):
    for cls_name in tree(cls):
        print(cls_name)


if __name__ == '__main__':
    display(BaseException)
