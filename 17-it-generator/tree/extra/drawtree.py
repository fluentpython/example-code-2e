from tree import tree

SP    = '\N{SPACE}'
HLIN  = '\N{BOX DRAWINGS LIGHT HORIZONTAL}' * 2 + SP        # ──
VLIN  = '\N{BOX DRAWINGS LIGHT VERTICAL}' + SP * 3          # │
TEE   = '\N{BOX DRAWINGS LIGHT VERTICAL AND RIGHT}' + HLIN  # ├──
ELBOW = '\N{BOX DRAWINGS LIGHT UP AND RIGHT}' + HLIN        # └──


def subclasses(cls):
    try:
        return cls.__subclasses__()
    except TypeError:  # handle the `type` type
        return cls.__subclasses__(cls)


def tree(cls, level=0, last_sibling=True):
    yield cls, level, last_sibling
    children = subclasses(cls)
    if children:
        last = children[-1]
        for child in children:
            yield from tree(child, level+1, child is last)


def render_lines(tree_iter):
    cls, _, _ = next(tree_iter)
    yield cls.__name__
    prefix = ''

    for cls, level, last in tree_iter:
        prefix = prefix[:4 * (level - 1)]
        prefix = prefix.replace(TEE, VLIN).replace(ELBOW, SP * 4)
        prefix += ELBOW if last else TEE
        yield prefix + cls.__name__


def draw(cls):
    for line in render_lines(tree(cls)):
        print(line)


if __name__ == '__main__':
    draw(BaseException)
