from struct import iter_unpack

FORMAT = 'i12s2sf'                             # <1>

def text(field: bytes) -> str:                 # <2>
    octets = field.split(b'\0', 1)[0]          # <3>
    return octets.decode('cp437')              # <4>

with open('metro_areas.bin', 'rb') as fp:      # <5>
    data = fp.read()

for fields in iter_unpack(FORMAT, data):       # <6>
    year, name, country, pop = fields
    place = text(name) + ', ' + text(country)  # <7>
    print(f'{year}\t{place}\t{pop:,.0f}')
