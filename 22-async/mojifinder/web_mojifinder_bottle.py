#!/usr/bin/env python3

import json
import unicodedata

from bottle import route, request, run, static_file

from charindex import InvertedIndex

index = {}

@route('/')
def form():
    return static_file('form.html', root='static/')


@route('/search')
def search():
    query = request.query['q']
    chars = index.search(query)
    results = []
    for char in chars:
        name = unicodedata.name(char)
        results.append({'char': char, 'name': name})
    return json.dumps(results).encode('UTF-8')


def main(port):
    global index
    index = InvertedIndex()
    run(host='localhost', port=port, debug=True)


if __name__ == '__main__':
    main(8000)
