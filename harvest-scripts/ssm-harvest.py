import errno
import os
from sickle import Sickle
from sickle.iterator import OAIResponseIterator

def to_str(bytes_or_str):
    '''Takes bytes or string and returns string'''
    if isinstance(bytes_or_str, bytes):
        value = bytes_or_str.decode('utf-8')
    else:
        value = bytes_or_str
    return value  # Instance of str

sickle = Sickle('http://cdm21044.contentdm.oclc.org/oai/oai.php')
print("Sickle instance created.") # status update

sets = sickle.ListSets()
print("Sets created.") # status update

for s in sets:
    records = sickle.ListRecords(metadataPrefix="oai_dc", set=s.setSpec, ignore_deleted=True)
    print("Records created.") # status update
    directory = 'output/sakip-sabanci/{}/data/'.format(s.setSpec)
    os.makedirs(os.path.dirname(directory), exist_ok=True)
    for count, record in enumerate(records, start=1):
        with open('{}{}-{}.xml'.format(directory, s.setSpec, count), 'w') as f:
        	# f.write(to_str(record.raw.encode('utf8')))
            f.write(record.raw)
            print('Record {} written'.format(count))
