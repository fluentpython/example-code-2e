#!/usr/bin/env python3

import itertools
from collections.abc import Iterator


def load_redirects():
    redirects = {}
    targets = {}
    for filename in ('custom.htaccess', 'short.htaccess'):
        with open(filename) as fp:
            for line in fp:
                if line.startswith('RedirectTemp'):
                    _, short, long = line.split()
                    short = short[1:]  # Remove leading slash
                    assert short not in redirects, f"{filename}: duplicate redirect from {short}"
                    # custom is live since 2022, we cannot change it remove duplicate targets
                    if not filename.startswith('custom'):
                        assert long not in targets, f"{filename}: Duplicate redirect to {long}"
                    redirects[short] = long
                    targets[long] = short
    return redirects, targets


SDIGITS = '23456789abcdefghjkmnpqrstvwxyz'


def gen_short() -> Iterator[str]:
    """
    Generate every possible sequence of SDIGITS.
    """
    length = 1
    while True:
        for short in itertools.product(SDIGITS, repeat=length):
            yield ''.join(short)
        length += 1


def shorten(n: int) -> str:
    """
    Get Nth short URL made from SDIGITS, where 0 is the first.
    """
    iter_short = gen_short()
    for i in range(n+1):
        short = next(iter_short)
        if i == n:
            return short


def gen_free_short(redirects: dict) -> Iterator[str]:
    """
    Generate next available short URL.
    """
    for short in gen_short():
        if short not in redirects:
            yield short


def new_urls(urls: list[str], redirects: dict, targets: dict) -> None:
    iter_short = gen_free_short(redirects)
    with open('short.htaccess', 'a') as fp:
        for url in urls:
            assert 'fpy.li' not in url, f"{url} is a fpy.li URL"
            if url in targets:
                continue
            short = next(iter_short)
            redirects[short] = url
            targets[url] = short
            fp.write(f"RedirectTemp /{short} {url}\n")


def main():
    from random import randrange
    urls = [f'https://example.com/{randrange(100000)}.html' for n in range(7)]

    redirects, targets = load_redirects()
    new_urls(urls, redirects, targets)


if __name__ == '__main__':
    main()
