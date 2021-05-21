from collections.abc import Iterable, AsyncIterator
from typing import NamedTuple

from curio import TaskGroup
import curio.socket as socket


class Result(NamedTuple):
    domain: str
    found: bool


async def probe(domain: str) -> Result:
    try:
        await socket.getaddrinfo(domain, None)
    except socket.gaierror:
        return Result(domain, False)
    return Result(domain, True)


async def multi_probe(domains: Iterable[str]) -> AsyncIterator[Result]:
    async with TaskGroup() as group:
        for domain in domains:
            await group.spawn(probe, domain)
        async for task in group:
            yield task.result
