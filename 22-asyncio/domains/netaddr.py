import asyncio
import socket
from collections.abc import Iterable, AsyncIterator
from typing import NamedTuple


class Result(NamedTuple):
    name: str
    found: bool


async def probe(loop: asyncio.AbstractEventLoop, name: str) -> Result:
    try:
        await loop.getaddrinfo(name, None)
    except socket.gaierror:
        return Result(name, False)
    return Result(name, True)


async def multi_probe(names: Iterable[str]) -> AsyncIterator[Result]:
    loop = asyncio.get_running_loop()
    coros = [probe(loop, name) for name in names]
    for coro in asyncio.as_completed(coros):
        result = await coro
        yield result
