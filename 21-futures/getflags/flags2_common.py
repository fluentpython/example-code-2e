"""Utilities for second set of flag examples.
"""

import argparse
import string
import sys
import time
from collections import namedtuple, Counter
from enum import Enum
from pathlib import Path

Result = namedtuple('Result', 'status data')

HTTPStatus = Enum('HTTPStatus', 'ok not_found error')

POP20_CC = ('CN IN US ID BR PK NG BD RU JP '
            'MX PH VN ET EG DE IR TR CD FR').split()

DEFAULT_CONCUR_REQ = 1
MAX_CONCUR_REQ = 1

SERVERS = {
    'REMOTE': 'http://fluentpython.com/data/flags',
    'LOCAL':  'http://localhost:8000/flags',
    'DELAY':  'http://localhost:8001/flags',
    'ERROR':  'http://localhost:8002/flags',
}
DEFAULT_SERVER = 'LOCAL'

DEST_DIR = Path('downloaded')
COUNTRY_CODES_FILE = Path('country_codes.txt')


def save_flag(img: bytes, filename: str) -> None:
    (DEST_DIR / filename).write_bytes(img)


def initial_report(cc_list: list[str],
                   actual_req: int,
                   server_label: str) -> None:
    if len(cc_list) <= 10:
        cc_msg = ', '.join(cc_list)
    else:
        cc_msg = f'from {cc_list[0]} to {cc_list[-1]}'
    print(f'{server_label} site: {SERVERS[server_label]}')
    plural = 's' if len(cc_list) != 1 else ''
    print(f'Searching for {len(cc_list)} flag{plural}: {cc_msg}')
    if actual_req == 1:
        print('1 connection will be used.')
    else:
        print(f'{actual_req} concurrent connections will be used.')


def final_report(cc_list: list[str],
                 counter: Counter[HTTPStatus],
                 start_time: float) -> None:
    elapsed = time.perf_counter() - start_time
    print('-' * 20)
    plural = 's' if counter[HTTPStatus.ok] != 1 else ''
    print(f'{counter[HTTPStatus.ok]} flag{plural} downloaded.')
    if counter[HTTPStatus.not_found]:
        print(f'{counter[HTTPStatus.not_found]} not found.')
    if counter[HTTPStatus.error]:
        plural = 's' if counter[HTTPStatus.error] != 1 else ''
        print(f'{counter[HTTPStatus.error]} error{plural}.')
    print(f'Elapsed time: {elapsed:.2f}s')


def expand_cc_args(every_cc: bool,
                   all_cc: bool,
                   cc_args: list[str],
                   limit: int) -> list[str]:
    codes: set[str] = set()
    A_Z = string.ascii_uppercase
    if every_cc:
        codes.update(a+b for a in A_Z for b in A_Z)
    elif all_cc:
        text = COUNTRY_CODES_FILE.read_text()
        codes.update(text.split())
    else:
        for cc in (c.upper() for c in cc_args):
            if len(cc) == 1 and cc in A_Z:
                codes.update(cc + c for c in A_Z)
            elif len(cc) == 2 and all(c in A_Z for c in cc):
                codes.add(cc)
            else:
                raise ValueError('*** Usage error: each CC argument '
                                 'must be A to Z or AA to ZZ.')
    return sorted(codes)[:limit]


def process_args(default_concur_req):
    server_options = ', '.join(sorted(SERVERS))
    parser = argparse.ArgumentParser(
        description='Download flags for country codes. '
                    'Default: top 20 countries by population.')
    parser.add_argument(
        'cc', metavar='CC', nargs='*',
        help='country code or 1st letter (eg. B for BA...BZ)')
    parser.add_argument(
        '-a', '--all', action='store_true',
        help='get all available flags (AD to ZW)')
    parser.add_argument(
        '-e', '--every', action='store_true',
        help='get flags for every possible code (AA...ZZ)')
    parser.add_argument(
        '-l', '--limit', metavar='N', type=int, help='limit to N first codes',
        default=sys.maxsize)
    parser.add_argument(
        '-m', '--max_req', metavar='CONCURRENT', type=int,
        default=default_concur_req,
        help=f'maximum concurrent requests (default={default_concur_req})')
    parser.add_argument(
        '-s', '--server', metavar='LABEL', default=DEFAULT_SERVER,
        help=f'Server to hit; one of {server_options} '
             f'(default={DEFAULT_SERVER})')
    parser.add_argument(
        '-v', '--verbose', action='store_true',
        help='output detailed progress info')
    args = parser.parse_args()
    if args.max_req < 1:
        print('*** Usage error: --max_req CONCURRENT must be >= 1')
        parser.print_usage()
        sys.exit(1)
    if args.limit < 1:
        print('*** Usage error: --limit N must be >= 1')
        parser.print_usage()
        sys.exit(1)
    args.server = args.server.upper()
    if args.server not in SERVERS:
        print(f'*** Usage error: --server LABEL '
              f'must be one of {server_options}')
        parser.print_usage()
        sys.exit(1)
    try:
        cc_list = expand_cc_args(args.every, args.all, args.cc, args.limit)
    except ValueError as exc:
        print(exc.args[0])
        parser.print_usage()
        sys.exit(1)

    if not cc_list:
        cc_list = sorted(POP20_CC)
    return args, cc_list


def main(download_many, default_concur_req, max_concur_req):
    args, cc_list = process_args(default_concur_req)
    actual_req = min(args.max_req, max_concur_req, len(cc_list))
    initial_report(cc_list, actual_req, args.server)
    base_url = SERVERS[args.server]
    t0 = time.perf_counter()
    counter = download_many(cc_list, base_url, args.verbose, actual_req)
    assert sum(counter.values()) == len(cc_list), (
        'some downloads are unaccounted for'
    )
    final_report(cc_list, counter, t0)
