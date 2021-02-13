#!/usr/bin/env python3

"""Download flags of countries (with error handling).

asyncio async/await version

"""
# BEGIN FLAGS2_ASYNCIO_TOP
import asyncio
from collections import Counter

import aiohttp
from aiohttp import web
from aiohttp.http_exceptions import HttpProcessingError
import tqdm  # type: ignore

from flags2_common import main, HTTPStatus, Result, save_flag

# default set low to avoid errors from remote site, such as
# 503 - Service Temporarily Unavailable
DEFAULT_CONCUR_REQ = 5
MAX_CONCUR_REQ = 1000


class FetchError(Exception):  # <1>
    def __init__(self, country_code):
        self.country_code = country_code


async def get_flag(session, base_url, cc):  # <2>
    url = '{}/{cc}/{cc}.gif'.format(base_url, cc=cc.lower())
    async with session.get(url) as resp:
        if resp.status == 200:
            return await resp.read()
        elif resp.status == 404:
            raise web.HTTPNotFound()
        else:
            raise HttpProcessingError(
                code=resp.status, message=resp.reason,
                headers=resp.headers)


async def download_one(session, cc, base_url, semaphore, verbose):  # <3>
    try:
        async with semaphore:  # <4>
            image = await get_flag(session, base_url, cc)  # <5>
    except web.HTTPNotFound:  # <6>
        status = HTTPStatus.not_found
        msg = 'not found'
    except Exception as exc:
        raise FetchError(cc) from exc  # <7>
    else:
        save_flag(image, cc.lower() + '.gif')  # <8>
        status = HTTPStatus.ok
        msg = 'OK'

    if verbose and msg:
        print(cc, msg)

    return Result(status, cc)
# END FLAGS2_ASYNCIO_TOP

# BEGIN FLAGS2_ASYNCIO_DOWNLOAD_MANY
async def downloader_coro(cc_list: list[str],
                          base_url: str,
                          verbose: bool,
                          concur_req: int) -> Counter[HTTPStatus]:  # <1>
    counter: Counter[HTTPStatus] = Counter()
    semaphore = asyncio.Semaphore(concur_req)  # <2>
    async with aiohttp.ClientSession() as session:  # <8>
        to_do = [download_one(session, cc, base_url, semaphore, verbose)
                 for cc in sorted(cc_list)]  # <3>

        to_do_iter = asyncio.as_completed(to_do)  # <4>
        if not verbose:
            to_do_iter = tqdm.tqdm(to_do_iter, total=len(cc_list))  # <5>
        for future in to_do_iter:  # <6>
            try:
                res = await future  # <7>
            except FetchError as exc:  # <8>
                country_code = exc.country_code  # <9>
                try:
                    if exc.__cause__ is None:
                        error_msg = 'Unknown cause'
                    else:
                        error_msg = exc.__cause__.args[0]  # <10>
                except IndexError:
                    error_msg = exc.__cause__.__class__.__name__  # <11>
                if verbose and error_msg:
                    msg = '*** Error for {}: {}'
                    print(msg.format(country_code, error_msg))
                status = HTTPStatus.error
            else:
                status = res.status

            counter[status] += 1  # <12>

    return counter  # <13>


def download_many(cc_list: list[str],
                  base_url: str,
                  verbose: bool,
                  concur_req: int) -> Counter[HTTPStatus]:
    coro = downloader_coro(cc_list, base_url, verbose, concur_req)
    counts = asyncio.run(coro)  # <14>

    return counts


if __name__ == '__main__':
    main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)
# END FLAGS2_ASYNCIO_DOWNLOAD_MANY
