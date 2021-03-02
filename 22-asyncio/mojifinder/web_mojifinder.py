import pathlib
from unicodedata import name

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from charindex import InvertedIndex

app = FastAPI(  # <1>
    title='Mojifinder Web',
    description='Search for Unicode characters by name.',
)

class CharName(BaseModel):  # <2>
    char: str
    name: str

def init(app):  # <3>
    app.state.index = InvertedIndex()
    static = pathlib.Path(__file__).parent.absolute() / 'static'
    with open(static / 'form.html') as fp:
        app.state.form = fp.read()

init(app)  # <4>

@app.get('/search', response_model=list[CharName])  # <5>
async def search(q: str):  # <6>
    chars = app.state.index.search(q)
    return ({'char': c, 'name': name(c)} for c in chars)  # <7>

@app.get('/',  # <8>
         response_class=HTMLResponse,
         include_in_schema=False)
def form():
    return app.state.form
