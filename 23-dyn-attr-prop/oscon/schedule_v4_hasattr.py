"""
schedule_v4.py: homegrown cached property for speakers

    >>> event = Record.fetch('event.33950')

# tag::SCHEDULE4_DEMO[]
    >>> event  # <1>
    <Event 'There *Will* Be Bugs'>
    >>> event.venue  # <2>
    <Record serial=1449>
    >>> event.venue.name  # <3>
    'Portland 251'
    >>> for spkr in event.speakers:  # <4>
    ...     print(f'{spkr.serial}: {spkr.name}')
    3471: Anna Martelli Ravenscroft
    5199: Alex Martelli

# end::SCHEDULE4_DEMO[]
"""

import json
import inspect

JSON_PATH = 'data/osconfeed.json'

class Record:

    __index = None

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        cls_name = self.__class__.__name__
        return f'<{cls_name} serial={self.serial!r}>'

    @staticmethod
    def fetch(key):
        if Record.__index is None:
            Record.__index = load()
        return Record.__index[key]


class Event(Record):

    def __repr__(self):
        if hasattr(self, 'name'):
            cls_name = self.__class__.__name__
            return f'<{cls_name} {self.name!r}>'
        else:
            return super().__repr__()  # <4>

    @property
    def venue(self):
        key = f'venue.{self.venue_serial}'
        return self.__class__.fetch(key)

# tag::SCHEDULE4_HASATTR_CACHE[]
    @property
    def speakers(self):
        if not hasattr(self, '__speaker_objs'):  # <1>
            spkr_serials = self.__dict__['speakers']
            fetch = self.__class__.fetch
            self.__speaker_objs = [fetch(f'speaker.{key}')
                    for key in spkr_serials]
        return self.__speaker_objs  # <2>

# end::SCHEDULE4_HASATTR_CACHE[]


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
