#!/usr/bin/env python3

"""Download flags of countries (with error handling).

asyncio async/await version

"""
# tag::FLAGS2_ASYNCIO_TOP[]
import asyncio
from collections import Counter

import aiohttp
import tqdm  # type: ignore

from flags2_common import main, HTTPStatus, Result, save_flag

# default set low to avoid errors from remote site, such as
# 503 - Service Temporarily Unavailable
DEFAULT_CONCUR_REQ = 5
MAX_CONCUR_REQ = 1000


class FetchError(Exception):  # <1>
    def __init__(self, country_code: str):
        self.country_code = country_code


async def get_flag(session: aiohttp.ClientSession,  # <2>
                   base_url: str,
                   cc: str) -> bytes:
    url = f'{base_url}/{cc}/{cc}.gif'.lower()
    async with session.get(url) as resp:
        if resp.status == 200:
            return await resp.read()
        else:
            resp.raise_for_status()  # <3>
            return bytes()

async def download_one(session: aiohttp.ClientSession,  # <4>
                       cc: str,
                       base_url: str,
                       semaphore: asyncio.Semaphore,
                       verbose: bool) -> Result:
    try:
        async with semaphore:  # <5>
            image = await get_flag(session, base_url, cc)
    except aiohttp.ClientResponseError as exc:
        if exc.status == 404:               # <6>
            status = HTTPStatus.not_found
            msg = 'not found'
        else:
            raise FetchError(cc) from exc  # <7>
    else:
        save_flag(image, f'{cc}.gif')
        status = HTTPStatus.ok
        msg = 'OK'
    if verbose and msg:
        print(cc, msg)
    return Result(status, cc)
# end::FLAGS2_ASYNCIO_TOP[]

# tag::FLAGS2_ASYNCIO_START[]
async def supervisor(cc_list: list[str],
                     base_url: str,
                     verbose: bool,
                     concur_req: int) -> Counter[HTTPStatus]:  # <1>
    counter: Counter[HTTPStatus] = Counter()
    semaphore = asyncio.Semaphore(concur_req)  # <2>
    async with aiohttp.ClientSession() as session:
        to_do = [download_one(session, cc, base_url, semaphore, verbose)
                 for cc in sorted(cc_list)]  # <3>
        to_do_iter = asyncio.as_completed(to_do)  # <4>
        if not verbose:
            to_do_iter = tqdm.tqdm(to_do_iter, total=len(cc_list))  # <5>
        for coro in to_do_iter:  # <6>
            try:
                res = await coro  # <7>
            except FetchError as exc:  # <8>
                country_code = exc.country_code  # <9>
                try:
                    error_msg = exc.__cause__.message  # type: ignore  # <10>
                except AttributeError:
                    error_msg = 'Unknown cause'  # <11>
                if verbose and error_msg:
                    print(f'*** Error for {country_code}: {error_msg}')
                status = HTTPStatus.error
            else:
                status = res.status
            counter[status] += 1  # <12>
    return counter  # <13>

def download_many(cc_list: list[str],
                  base_url: str,
                  verbose: bool,
                  concur_req: int) -> Counter[HTTPStatus]:
    coro = supervisor(cc_list, base_url, verbose, concur_req)
    counts = asyncio.run(coro)  # <14>

    return counts

if __name__ == '__main__':
    main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)
# end::FLAGS2_ASYNCIO_START[]
