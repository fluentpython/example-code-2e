import asyncio
import socket
from collections.abc import Iterable, AsyncIterator
from typing import NamedTuple, Optional


class Result(NamedTuple):  # <1>
    domain: str
    found: bool


OptionalLoop = Optional[asyncio.AbstractEventLoop]  # <2>


async def probe(domain: str, loop: OptionalLoop = None) -> Result:  # <3>
    if loop is None:
        loop = asyncio.get_running_loop()
    try:
        await loop.getaddrinfo(domain, None)
    except socket.gaierror:
        return Result(domain, False)
    return Result(domain, True)


async def multi_probe(domains: Iterable[str]) -> AsyncIterator[Result]:  # <4>
    loop = asyncio.get_running_loop()
    coros = [probe(domain, loop) for domain in domains]  # <5>
    for coro in asyncio.as_completed(coros):  # <6>
        result = await coro  # <7>
        yield result  # <8>
