#!/usr/bin/env python3.8

import sys
import io
from itertools import product
from unicodedata import name, unidata_version

from bottle import route, run, response, template


ZWJ = '\u200D'   # ZERO WIDTH JOINER

ADULTS = '\N{MAN}\N{WOMAN}'
CHILDREN = '\N{BOY}\N{GIRL}'

adults = list(ADULTS) + list(product(ADULTS, repeat=2))
children = list(CHILDREN) + list(product(CHILDREN, repeat=2))


def matrix():
    for kids in children:
        row = []
        suffix = ZWJ + ZWJ.join(kids)
        for p in adults:
            row.append(ZWJ.join(p)+suffix)
        yield row


def report():
    out = io.StringIO()
    print('Python', '.'.join(str(n) for n in sys.version_info[:3]), file=out)
    print('Unicode', unidata_version, file=out)

    print(end='\t', file=out)
    for parents in adults:
        print('+'.join(parents), end='\t', file=out)

    print(file=out)

    for kids, row in zip(children, matrix()):
        print('+'.join(kids), end='\t', file=out)
        for cell in row:
            print(cell, end='\t', file=out)

        print(file=out)

    return out.getvalue()

TABLE = """
<html>
<style>
table {text-align: center;
       border-collapse: collapse;}
td    {border: 1px solid gray;}
th    {padding: 0.5ex;}
</style>
<table ">
    <tr>
        <th></th>
        % for parents in adults:
            <th>{{'+'.join(parents)}}</th>
        % end
    </tr>
    % for kids, row in zip(children, matrix()):
        <tr>
            <th>{{'+'.join(kids)}}</th>
            % for cell in row:
                <td>{{cell}}</td>
            % end
        </tr>
    % end
</table>
</html>

"""


@route('/')
def index():
    response.content_type = 'text/html; charset=utf-8'
    return template(TABLE, **globals())


if __name__ == '__main__':
    run(host='localhost', port=8080)


