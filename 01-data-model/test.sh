#!/bin/bash
python3 -m doctest frenchdeck.doctest
python3 -m doctest vector2d.py
pytest -q --nbval
