>>> import json
>>> with open('data/osconfeed.json') as fp:
...     feed = json.load(fp)  # <1>
>>> sorted(feed['Schedule'].keys())  # <2>
['conferences', 'events', 'speakers', 'venues']
>>> for key, value in sorted(feed['Schedule'].items()):
...     print(f'{len(value):3} {key}')  # <3>
...
  1 conferences
484 events
357 speakers
 53 venues
>>> feed['Schedule']['speakers'][-1]['name']  # <4>
'Carina C. Zona'
>>> feed['Schedule']['speakers'][-1]['serial']  # <5>
141590
>>> feed['Schedule']['events'][40]['name']
'There *Will* Be Bugs'
>>> feed['Schedule']['events'][40]['speakers']  # <6>
[3471, 5199]
