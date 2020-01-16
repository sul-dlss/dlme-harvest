import errno
import os
from sickle import Sickle
from sickle.iterator import OAIResponseIterator

# where to write data to (relative to the dlme-harvest repo folder)
base_output_folder = 'output'

# def to_str(bytes_or_str):
#     '''Takes bytes or string and returns string'''
#     if isinstance(bytes_or_str, bytes):
#         value = bytes_or_str.decode('utf-8')
#     else:
#         value = bytes_or_str
#     return value  # Instance of str

sickle = Sickle('https://api.qdl.qa/oaipmh')
print("Sickle instance created.") # status update

records = sickle.ListRecords(metadataPrefix='mods', ignore_deleted=True)
print("Records created.") # status update
file_count = 1
record_number = 1

directory = "output/qnl/data/"
os.makedirs(os.path.dirname(directory), exist_ok=True)

for count, record in enumerate(records, start=1):
    print("Record number " + str(count))
    out_file = 'output/qnl/data/qnl-{}.xml'.format(count)
    directory_name = os.path.dirname(out_file)
    with open(out_file, 'w') as f:
    	f.write(record.raw)
