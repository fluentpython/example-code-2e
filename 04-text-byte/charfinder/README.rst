========================
Character Finder Utility
========================

Usage tips
==========

`cf.py` works as an executable on Unix-like systems,
if you have `python3` on your `$PATH`::

    $ chmod +x cf.py
    $ ./cf.py cat eyes
    U+1F638	😸	GRINNING CAT FACE WITH SMILING EYES
    U+1F63B	😻	SMILING CAT FACE WITH HEART-SHAPED EYES
    U+1F63D	😽	KISSING CAT FACE WITH CLOSED EYES

Use `wc -l` to count the number of hits::

    $ ./cf.py hieroglyph | wc -l
    1663

With `tee` you can get the output and the count::

    $ ./cf.py trigram | tee >(wc -l)
    U+2630	☰	TRIGRAM FOR HEAVEN
    U+2631	☱	TRIGRAM FOR LAKE
    U+2632	☲	TRIGRAM FOR FIRE
    U+2633	☳	TRIGRAM FOR THUNDER
    U+2634	☴	TRIGRAM FOR WIND
    U+2635	☵	TRIGRAM FOR WATER
    U+2636	☶	TRIGRAM FOR MOUNTAIN
    U+2637	☷	TRIGRAM FOR EARTH
    8


Running the tests
=================

Run the ``doctest`` module from the command line on 
this README.rst file (using ``-v`` to make tests visible)::

    $ python3 -m doctest README.rst -v

That's what the ``test.sh`` script does.


Tests
-----

Import functions for testing::

    >>> from cf import find, main

Test ``find`` with single result::

    >>> find('sign', 'registered')  # doctest:+NORMALIZE_WHITESPACE
    U+00AE	®	REGISTERED SIGN

Test ``find`` with two results::

    >>> find('chess', 'queen', end=0xFFFF)  # doctest:+NORMALIZE_WHITESPACE
    U+2655	♕	WHITE CHESS QUEEN
    U+265B	♛	BLACK CHESS QUEEN

Test ``find`` with no results::

    >>> find('no_such_character')

Test ``main`` with no words::

    >>> main([])
    Please provide words to find.
