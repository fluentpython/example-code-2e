"""
schedule2.py: traversing OSCON schedule data

    >>> import shelve
    >>> db = shelve.open(DB_NAME)
    >>> if CONFERENCE not in db: load_db(db)

# BEGIN SCHEDULE2_DEMO

    >>> DbRecord.set_db(db)  
    >>> event = DbRecord.fetch('event.33950')  
    >>> event  
    <Event 'There *Will* Be Bugs'>
    >>> event.venue  
    <DbRecord serial='venue.1449'>
    >>> event.venue.name  
    'Portland 251'
    >>> for spkr in event.speakers:  
    ...     print('{0.serial}: {0.name}'.format(spkr))
    ...
    speaker.3471: Anna Martelli Ravenscroft
    speaker.5199: Alex Martelli

# END SCHEDULE2_DEMO

    >>> db.close()

"""

# BEGIN SCHEDULE2_RECORD
import warnings
import inspect  

import osconfeed

DB_NAME = 'data/schedule2_db'  
CONFERENCE = 'conference.115'


class Record:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __eq__(self, other):  
        if isinstance(other, Record):
            return self.__dict__ == other.__dict__
        else:
            return NotImplemented
# END SCHEDULE2_RECORD


# BEGIN SCHEDULE2_DBRECORD
class MissingDatabaseError(RuntimeError):
    """Raised when a database is required but was not set."""  


class DbRecord(Record): 

    __db = None  

    @staticmethod  
    def set_db(db):
        DbRecord.__db = db  

    @staticmethod 
    def get_db():
        return DbRecord.__db

    @classmethod  
    def fetch(cls, ident):
        db = cls.get_db()
        try:
            return db[ident]  
        except TypeError:
            if db is None:  
                msg = "database not set; call '{}.set_db(my_db)'"
                raise MissingDatabaseError(msg.format(cls.__name__))
            else:  
                raise

    def __repr__(self):
        if hasattr(self, 'serial'):  
            cls_name = self.__class__.__name__
            return '<{} serial={!r}>'.format(cls_name, self.serial)
        else:
            return super().__repr__()  
# END SCHEDULE2_DBRECORD


# BEGIN SCHEDULE2_EVENT
class Event(DbRecord):  

    @property
    def venue(self):
        key = 'venue.{}'.format(self.venue_serial)
        return self.__class__.fetch(key)  

    @property
    def speakers(self):
        if not hasattr(self, '_speaker_objs'):  
            spkr_serials = self.__dict__['speakers']  
            fetch = self.__class__.fetch 
            self._speaker_objs = [fetch('speaker.{}'.format(key))
                                  for key in spkr_serials]  
        return self._speaker_objs  

    def __repr__(self):
        if hasattr(self, 'name'):  
            cls_name = self.__class__.__name__
            return '<{} {!r}>'.format(cls_name, self.name)
        else:
            return super().__repr__()  
# END SCHEDULE2_EVENT


# BEGIN SCHEDULE2_LOAD
def load_db(db):
    raw_data = osconfeed.load()
    warnings.warn('loading ' + DB_NAME)
    for collection, rec_list in raw_data['Schedule'].items():
        record_type = collection[:-1]  
        cls_name = record_type.capitalize()  
        cls = globals().get(cls_name, DbRecord)  
        if inspect.isclass(cls) and issubclass(cls, DbRecord):  
            factory = cls  
        else:
            factory = DbRecord  
        for record in rec_list:  
            key = '{}.{}'.format(record_type, record['serial'])
            record['serial'] = key
            db[key] = factory(**record)  
# END SCHEDULE2_LOAD
