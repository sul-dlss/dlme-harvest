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

sickle = Sickle('http://cdm21044.contentdm.oclc.org/oai/oai.php')
print("Sickle instance created.") # status update

sets = sickle.ListSets()
print("Sets created.") # status update

set_number = 0
for s in sets:
    records = sickle.ListRecords(metadataPrefix="oai_dc", set=s.setSpec, ignore_deleted=True)
    print("Records created.") # status update
    file_count = 1
    set_number += 1
    record_number = 1
    for record in records:
        print("Set number: " + str(set_number) + " | " + "Record number " + str(record_number))
        record_number += 1
        out_file = '{}/{}/data/{}-{}.xml'.format(base_output_folder, s.setSpec, s.setSpec, file_count)
        directory_name = os.path.dirname(out_file)
        if not os.path.exists(directory_name):
            try:
                os.makedirs(directory_name)
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise
        with open(out_file, 'w') as f:
        	file_count += 1
        	f.write(to_str(record.raw.encode('utf8')))
        	f.close()
