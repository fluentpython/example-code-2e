from checkeddeco import checked

@checked
class Movie:
    title: str
    year: int
    megabucks: float


if __name__ == '__main__':
    movie = Movie(title='The Godfather', year=1972, megabucks=137)
    print(movie.title)
    print(movie)
    try:
        # remove the "type: ignore" comment to see Mypy error
        movie.year = 'MCMLXXII'  # type: ignore
    except TypeError as e:
        print(e)
    try:
        blockbuster = Movie(title='Avatar', year=2009, megabucks='billions')
    except TypeError as e:
        print(e)
