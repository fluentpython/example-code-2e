#!/usr/bin/env python3
from curio import run, TaskGroup
from curio.socket import getaddrinfo, gaierror
from keyword import kwlist

MAX_KEYWORD_LEN = 4  # <1>


async def probe(domain: str) -> tuple[str, bool]:  # <2>
    try:
        await getaddrinfo(domain, None)  # <4>
    except gaierror:
        return (domain, False)
    return (domain, True)


async def main() -> None:  # <5>
    names = (kw for kw in kwlist if len(kw) <= MAX_KEYWORD_LEN)  # <6>
    domains = (f'{name}.dev'.lower() for name in names)  # <7>
    async with TaskGroup() as group:
        for domain in domains:
            await group.spawn(probe, domain)
        async for task in group:  # <9>
            domain, found = task.result  # <10>
            mark = '+' if found else ' '
            print(f'{mark} {domain}')


if __name__ == '__main__':
    run(main())  # <11>
