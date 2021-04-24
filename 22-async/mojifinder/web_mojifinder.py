from pathlib import Path
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
    static = Path(__file__).parent.absolute() / 'static'  # <4>
    app.state.form = (static / 'form.html').read_text()

init(app)  # <5>

@app.get('/search', response_model=list[CharName])  # <6>
async def search(q: str):  # <7>
    chars = app.state.index.search(q)
    return ({'char': c, 'name': name(c)} for c in chars)  # <8>

@app.get('/', response_class=HTMLResponse, include_in_schema=False)
def form():  # <9>
    return app.state.form

# no main funcion  # <10>