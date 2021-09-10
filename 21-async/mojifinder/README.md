# Mojifinder: Unicode character search examples

Examples from _Fluent Python, Second Edition_—Chapter 22, _Asynchronous Programming_.

## How to run `web_mojifinder.py`

`web_mojifinder.py` is a Web application built with _[FastAPI](https://fastapi.tiangolo.com/)_.
To run it, first install _FastAPI_ and an ASGI server.
The application was tested with _[Uvicorn](https://www.uvicorn.org/)_.

```
$ pip install fastapi uvicorn
```

Now you can use `uvicorn` to run the app.

```
$ uvicorn web_mojifinder:app
```

Finally, visit http://127.0.0.1:8000/ with your browser to see the search form.


## Directory contents

These files can be run as scripts directly from the command line:

- `charindex.py`: libray used by the Mojifinder examples. Also works as CLI search script.
- `tcp_mojifinder.py`: TCP/IP Unicode search server. Depends only on the Python 3.9 standard library. Use a telnet application as client.
- `web_mojifinder_bottle.py`: Unicode Web service. Depends on `bottle.py` and `static/form.html`. Use an HTTP browser as client.

This program requires an ASGI server to run it:

- `web_mojifinder.py`: Unicode Web service. Depends on _[FastAPI](https://fastapi.tiangolo.com/)_ and `static/form.html`.

Support files:

- `bottle.py`: local copy of the single-file _[Bottle](https://bottlepy.org/)_ Web framework.
- `requirements.txt`: list of dependencies for `web_mojifinder.py`.
- `static/form.html`: HTML form used by the `web_*` examples.
- `README.md`: this file 🤓
