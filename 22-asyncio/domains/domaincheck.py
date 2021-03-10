#!/usr/bin/env python3
import asyncio
import sys
from keyword import kwlist

from domainlib import multi_probe


async def main(tld: str) -> None:
    tld = tld.strip('.')
    names = (kw for kw in kwlist if len(kw) <= 4)  # <1>
    domains = (f'{name}.{tld}'.lower() for name in names)  # <2>
    print('FOUND\t\tNOT FOUND')  # <3>
    print('=====\t\t=========')
    async for domain, found in multi_probe(domains):  # <4>
        indent = '' if found else '\t\t'  # <5>
        print(f'{indent}{domain}')


if __name__ == '__main__':
    if len(sys.argv) == 2:
        asyncio.run(main(sys.argv[1]))  # <6>
    else:
        print('Please provide a TLD.', f'Example: {sys.argv[0]} COM.BR')
