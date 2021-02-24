"""
uvicorn main:app --reload
"""

import pathlib
from unicodedata import name

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from charindex import InvertedIndex

app = FastAPI(
    title='Mojifinder Web',
    description='Search for Unicode characters by name.',
)

class CharName(BaseModel):
    char: str
    name: str

def init(app):
    app.state.index = InvertedIndex()
    static = pathlib.Path(__file__).parent.absolute() / 'static'
    with open(static / 'form.html') as fp:
        app.state.form = fp.read()

init(app)

@app.get('/', response_class=HTMLResponse, include_in_schema=False)
def form():
    return app.state.form

@app.get('/search', response_model=list[CharName])
async def search(q: str):
    chars = app.state.index.search(q)
    return [{'char': c, 'name': name(c)} for c in chars]
