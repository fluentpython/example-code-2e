"""
schedule_v3.py: property to get list of event speakers

    >>> event = Record.fetch('event.33950')
    >>> event
    <Event 'There *Will* Be Bugs'>
    >>> event.venue
    <Record serial=1449>
    >>> event.venue_serial
    1449
    >>> event.venue.name
    'Portland 251'

# tag::SCHEDULE3_DEMO[]
    >>> for spkr in event.speakers:
    ...     print(f'{spkr.serial}: {spkr.name}')
    3471: Anna Martelli Ravenscroft
    5199: Alex Martelli

# end::SCHEDULE3_DEMO[]
"""

import inspect
import json

JSON_PATH = 'data/osconfeed.json'

class Record:

    __index = None

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        return f'<{self.__class__.__name__} serial={self.serial!r}>'

    @staticmethod
    def fetch(key):
        if Record.__index is None:
            Record.__index = load()
        return Record.__index[key]


class Event(Record):

    def __repr__(self):
        try:
            return f'<{self.__class__.__name__} {self.name!r}>'
        except AttributeError:
            return super().__repr__()

    @property
    def venue(self):
        key = f'venue.{self.venue_serial}'
        return self.__class__.fetch(key)

# tag::SCHEDULE3_SPEAKERS[]
    @property
    def speakers(self):
        spkr_serials = self.__dict__['speakers']  # <1>
        fetch = self.__class__.fetch
        return [fetch(f'speaker.{key}')
                for key in spkr_serials]  # <2>

# end::SCHEDULE3_SPEAKERS[]


def load(path=JSON_PATH):
    records = {}
    with open(path) as fp:
        raw_data = json.load(fp)
    for collection, raw_records in raw_data['Schedule'].items():
        record_type = collection[:-1]
        cls_name = record_type.capitalize()
        cls = globals().get(cls_name, Record)
        if inspect.isclass(cls) and issubclass(cls, Record):
            factory = cls
        else:
            factory = Record
        for raw_record in raw_records:
            key = f'{record_type}.{raw_record["serial"]}'
            records[key] = factory(**raw_record)
    return records
