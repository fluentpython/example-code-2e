"""
schedule_v1.py: traversing OSCON schedule data

# tag::SCHEDULE1_DEMO[]
    >>> records = load(JSON_PATH)  # <1>
    >>> speaker = records['speaker.3471']  # <2>
    >>> speaker  # <3>
    <Record serial=3471>
    >>> speaker.name, speaker.twitter  # <4>
    ('Anna Martelli Ravenscroft', 'annaraven')

# end::SCHEDULE1_DEMO[]

"""

# tag::SCHEDULE1[]
import json

JSON_PATH = 'data/osconfeed.json'

class Record:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)  # <1>

    def __repr__(self):
        return f'<{self.__class__.__name__} serial={self.serial!r}>'  # <2>

def load(path=JSON_PATH):
    records = {}  # <3>
    with open(path) as fp:
        raw_data = json.load(fp)  # <4>
    for collection, raw_records in raw_data['Schedule'].items():  # <5>
        record_type = collection[:-1]  # <6>
        for raw_record in raw_records:
            key = f'{record_type}.{raw_record["serial"]}' # <7>
            records[key] = Record(**raw_record)  # <8>
    return records
# end::SCHEDULE1[]
