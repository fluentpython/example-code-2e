#!/usr/bin/env python3

from checkeddeco import checked

@checked
class Movie:
    title: str
    year: int
    box_office: float


if __name__ == '__main__':
    # No static type checker can understand this...
    movie = Movie(title='The Godfather', year=1972, box_office=137)  # type: ignore
    print(movie.title)
    print(movie)
    try:
        # remove the "type: ignore" comment to see Mypy correctly spot the error
        movie.year = 'MCMLXXII'  # type: ignore
    except TypeError as e:
        print(e)
    try:
        # Again, no static type checker can understand this...
        blockbuster = Movie(title='Avatar', year=2009, box_office='billions')  # type: ignore
    except TypeError as e:
        print(e)
