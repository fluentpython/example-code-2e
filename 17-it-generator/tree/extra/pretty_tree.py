from tree import tree

SPACES = ' ' * 4
HLINE = '\u2500'            # ─ BOX DRAWINGS LIGHT HORIZONTAL
HLINE2 = HLINE * 2
ELBOW = f'\u2514{HLINE2} '  # └ BOX DRAWINGS LIGHT UP AND RIGHT
TEE   = f'\u251C{HLINE2} '  # ├ BOX DRAWINGS LIGHT VERTICAL AND RIGHT
PIPE  = f'\u2502   '        # │ BOX DRAWINGS LIGHT VERTICAL


def render_lines(tree_iter):
    name, _, _ = next(tree_iter)
    yield name
    prefix = ''

    for name, level, last in tree_iter:
        if last:
            connector = ELBOW
        else:
            connector = TEE

        prefix = prefix[:4 * (level-1)]
        prefix = prefix.replace(TEE, PIPE).replace(ELBOW, SPACES)
        prefix += connector

        yield prefix + name


if __name__ == '__main__':
    for line in render_lines(tree(BaseException)):
        print(line)