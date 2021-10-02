#!/usr/bin/env python3

"""Download flags of countries (with error handling).

asyncio async/await version using run_in_executor for save_flag.

"""

import asyncio
from collections import Counter
from http import HTTPStatus

import aiohttp
import tqdm  # type: ignore

from flags2_common import main, DownloadStatus, save_flag

# default set low to avoid errors from remote site, such as
# 503 - Service Temporarily Unavailable
DEFAULT_CONCUR_REQ = 5
MAX_CONCUR_REQ = 1000


class FetchError(Exception):
    def __init__(self, country_code: str):
        self.country_code = country_code

async def get_flag(session: aiohttp.ClientSession,
                   base_url: str,
                   cc: str) -> bytes:
    url = f'{base_url}/{cc}/{cc}.gif'
    async with session.get(url) as resp:
        if resp.status == 200:
            return await resp.read()
        else:
            resp.raise_for_status()
            return bytes()

# tag::FLAGS3_ASYNCIO_GET_COUNTRY[]
async def get_country(session: aiohttp.ClientSession,
                      base_url: str,
                      cc: str) -> str:  # <1>
    url = f'{base_url}/{cc}/metadata.json'
    async with session.get(url) as resp:
        if resp.status == 200:
            metadata = await resp.json()  # <2>
            return metadata.get('country', 'no name')  # <3>
        else:
            resp.raise_for_status()
            return ''
# end::FLAGS3_ASYNCIO_GET_COUNTRY[]

# tag::FLAGS3_ASYNCIO_DOWNLOAD_ONE[]
async def download_one(session: aiohttp.ClientSession,
                       cc: str,
                       base_url: str,
                       semaphore: asyncio.Semaphore,
                       verbose: bool) -> DownloadStatus:
    try:
        async with semaphore:
            image = await get_flag(session, base_url, cc)  # <1>
        async with semaphore:
            country = await get_country(session, base_url, cc)  # <2>
    except aiohttp.ClientResponseError as exc:
        if exc.status == HTTPStatus.NOT_FOUND:
            status = DownloadStatus.NOT_FOUND
            msg = 'not found'
        else:
            raise FetchError(cc) from exc
    else:
        filename = country.replace(' ', '_')  # <3>
        filename = f'{filename}.gif'
        loop = asyncio.get_running_loop()
        loop.run_in_executor(None,
                             save_flag, image, filename)
        status = DownloadStatus.OK
        msg = 'OK'
    if verbose and msg:
        print(cc, msg)
    return status
# end::FLAGS3_ASYNCIO_DOWNLOAD_ONE[]

async def supervisor(cc_list: list[str],
                     base_url: str,
                     verbose: bool,
                     concur_req: int) -> Counter[DownloadStatus]:
    counter: Counter[DownloadStatus] = Counter()
    semaphore = asyncio.Semaphore(concur_req)
    async with aiohttp.ClientSession() as session:
        to_do = [download_one(session, cc, base_url,
                              semaphore, verbose)
                 for cc in sorted(cc_list)]

        to_do_iter = asyncio.as_completed(to_do)
        if not verbose:
            to_do_iter = tqdm.tqdm(to_do_iter, total=len(cc_list))
        for coro in to_do_iter:
            try:
                status = await coro
            except FetchError as exc:
                country_code = exc.country_code
                try:
                    error_msg = exc.__cause__.message  # type: ignore
                except AttributeError:
                    error_msg = 'Unknown cause'
                if verbose and error_msg:
                    print(f'*** Error for {country_code}: {error_msg}')
                status = DownloadStatus.ERROR

            counter[status] += 1

    return counter


def download_many(cc_list: list[str],
                  base_url: str,
                  verbose: bool,
                  concur_req: int) -> Counter[DownloadStatus]:
    coro = supervisor(cc_list, base_url, verbose, concur_req)
    counts = asyncio.run(coro)  # <14>

    return counts


if __name__ == '__main__':
    main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)
