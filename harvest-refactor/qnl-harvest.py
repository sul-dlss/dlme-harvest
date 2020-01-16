import errno
import os
from sickle import Sickle
from sickle.iterator import OAIResponseIterator

# where to write data to (relative to the dlme-harvest repo folder)
base_output_folder = 'output'

def to_str(bytes_or_str):
    '''Takes bytes or string and returns string'''
    if isinstance(bytes_or_str, bytes):
        value = bytes_or_str.decode('utf-8')
    else:
        value = bytes_or_str
    return value  # Instance of str

sickle = Sickle('https://api.qdl.qa/oaipmh')
print("Sickle instance created.") # status update

records = sickle.ListRecords(metadataPrefix='mods', ignore_deleted=True)
print("Records created.") # status update
file_count = 1
record_number = 1
for record in records:
    print("Record number " + str(record_number))
    record_number += 1
    out_file = '{}/data/qnl-{}.xml'.format(base_output_folder, file_count)
    directory_name = os.path.dirname(out_file)
    if not os.path.exists(directory_name):
        try:
            os.makedirs(os.path.dirname(directory_name))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
    with open(out_file, 'w') as f:
    	file_count += 1
    	f.write(to_str(record.raw.encode('utf8')))
