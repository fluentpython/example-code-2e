import asyncio
import socket
from collections.abc import Iterable, AsyncIterator
from typing import NamedTuple


class Result(NamedTuple):
    domain: str
    found: bool


async def probe(loop: asyncio.AbstractEventLoop, domain: str) -> Result:
    try:
        await loop.getaddrinfo(domain, None)
    except socket.gaierror:
        return Result(domain, False)
    return Result(domain, True)


async def multi_probe(domains: Iterable[str]) -> AsyncIterator[Result]:
    loop = asyncio.get_running_loop()
    coros = [probe(loop, domain) for domain in domains]
    for coro in asyncio.as_completed(coros):
        result = await coro
        yield result
