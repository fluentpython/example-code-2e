#!/usr/bin/env python3

import asyncio
import sys
from keyword import kwlist

from netaddr import multi_probe


async def main(tld: str) -> None:
    names = (f'{w}.{tld}'.lower() for w in kwlist if len(w) <= 4)
    async for name, found in multi_probe(sorted(names)):
        mark = '.' if found else '?\t\t'
        print(f'{mark} {name}')


if __name__ == '__main__':
    if len(sys.argv) == 2:
        asyncio.run(main(sys.argv[1]))
    else:
        print('Please provide a TLD.', f'Example: {sys.argv[0]} COM.BR')
