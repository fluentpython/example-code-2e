#!/usr/bin/env python3

from checkedlib import Checked

class Movie(Checked):
    title: str
    year: int
    box_office: float


if __name__ == '__main__':
    movie = Movie(title='The Godfather', year=1972, box_office=137)
    print(movie.title)
    print(movie)
    try:
        # remove the "type: ignore" comment to see Mypy error
        movie.year = 'MCMLXXII'  # type: ignore
    except TypeError as e:
        print(e)
    try:
        blockbuster = Movie(title='Avatar', year=2009, box_office='billions')
    except TypeError as e:
        print(e)
