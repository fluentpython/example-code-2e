from collections.abc import Mapping

NAMES = {
    'aqua': 65535,
    'black': 0,
    'blue': 255,
    'fuchsia': 16711935,
    'gray': 8421504,
    'green': 32768,
    'lime': 65280,
    'maroon': 8388608,
    'navy': 128,
    'olive': 8421376,
    'purple': 8388736,
    'red': 16711680,
    'silver': 12632256,
    'teal': 32896,
    'white': 16777215,
    'yellow': 16776960,
}

def rgb2hex(color: tuple[int, int, int]) -> str:
    if any(c not in range(256) for c in color):
        raise ValueError('Color components must be in range(256)')
    values = (f'{n % 256:02x}' for n in color)
    return '#' + ''.join(values)

HEX_ERROR = "Color must use format '#0099ff', got: {!r}"

def hex2rgb(color: str) -> tuple[int, int, int]:
    if len(color) != 7 or color[0] != '#':
        raise ValueError(HEX_ERROR.format(color))
    try:
        r, g, b = (int(color[i:i+2], 16) for i in range(1, 6, 2))
    except ValueError as exc:
        raise ValueError(HEX_ERROR.format(color)) from exc
    return r, g, b

def name2hex(name: str, color_map: Mapping[str, int]) -> str:
    try:
        code = color_map[name]
    except KeyError as exc:
        raise KeyError(f'Color {name!r} not found.') from exc
    return f'#{code:06x}'


def demo():
    c = (255, 255, 0)
    h = rgb2hex(c)
    r = hex2rgb(h)
    print(c, h, r)
    c = (255, 165, 0)
    h = rgb2hex(c)
    r = hex2rgb(h)
    print(c, h, r)
    c = (512, 165, 0)
    try:
        h = rgb2hex(c)
    except ValueError as exc:
        print(c, repr(exc))
    try:
        r = hex2rgb('bla')
    except ValueError as exc:
        print(c, repr(exc))
    try:
        r = hex2rgb('#nonono')
    except ValueError as exc:
        print(c, repr(exc))
    n = 'yellow'
    print(n, name2hex(n, NAMES))
    n = 'blue'
    print(n, name2hex(n, NAMES))
    from collections import OrderedDict
    o = OrderedDict(black=0, white=0xffffff)
    n = 'white'
    print(n, name2hex(n, o))


if __name__ == '__main__':
    demo()
