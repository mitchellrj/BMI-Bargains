from persistent.mapping import PersistentMapping
from persistent.dict import PersistentDict
from persistent.list import PersistentList

from searchqueue import SearchQueue

class Searches(PersistentMapping):
    __name__ = None
    __parent__ = None

    def __init__(self, *args, **kwargs):
        super(Searches, self).__init__(*args, **kwargs)
        self.routes_cache = None
        self.availability_cache = {}

class Search(PersistentDict):
    def __init__(self, email, start_date, end_date, departdaysofweek, origins,
                 destinations, num_days, price, adults, children, infants):
        super(Search, self).__init__()
        self['email'] = email
        self['start_date'] = start_date
        self['end_date'] = end_date
        self['departdaysofweek'] = departdaysofweek
        self['origins'] = origins
        self['destinations'] = destinations
        self['num_days'] = num_days
        self['price'] = price
        self['adults'] = adults
        self['children'] = children
        self['infants'] = infants
        self['active'] = False
        self['told'] = PersistentList()

    def activate(self):
        self['active'] = True

def appmaker(zodb_root):
    if not 'app_root' in zodb_root:
        app_root = Searches()
        zodb_root['app_root'] = app_root
        import transaction
        transaction.commit()

    SearchQueue(zodb_root['app_root'], name="searchQueue").start()

    return zodb_root['app_root']
