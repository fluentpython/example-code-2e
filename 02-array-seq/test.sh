#!/bin/bash
python3 -m doctest bisect_demo.py
python3 -m doctest metro_lat_lon.py
pytest -q --nbval
