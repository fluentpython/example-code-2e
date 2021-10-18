from tree import tree

SP = '\N{SPACE}'
HLIN  = '\N{BOX DRAWINGS LIGHT HORIZONTAL}'                       # ─
ELBOW = f'\N{BOX DRAWINGS LIGHT UP AND RIGHT}{HLIN*2}{SP}'        # └──
TEE   = f'\N{BOX DRAWINGS LIGHT VERTICAL AND RIGHT}{HLIN*2}{SP}'  # ├──
PIPE  = f'\N{BOX DRAWINGS LIGHT VERTICAL}{SP*3}'                  # │


def render_lines(tree_iter):
    cls, _, _ = next(tree_iter)
    yield cls.__name__
    prefix = ''

    for cls, level, last in tree_iter:
        prefix = prefix[:4 * (level-1)]
        prefix = prefix.replace(TEE, PIPE).replace(ELBOW, SP*4)
        prefix += ELBOW if last else TEE
        yield prefix + cls.__name__


def draw(cls):
    for line in render_lines(tree(cls)):
        print(line)


if __name__ == '__main__':
    draw(BaseException)
