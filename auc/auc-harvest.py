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

sickle = Sickle(' http://cdm15795.contentdm.oclc.org/oai/oai.php')
print("Sickle instance created.") # status update

sets = sickle.ListSets()
print("Sets created.") # status update

# Do not harvest these sets; permission not yet granted
do_not_harvest = ['p15795coll31', 'p15795coll32', 'p15795coll25', 'p15795coll29', 'p15795coll22', 'p15795coll7', 
				 'p15795coll3', 'p15795coll20', 'p15795coll17', 'p15795coll18']

set_number = 0
for s in sets:
	if s.setSpec not in do_not_harvest:
	    records = sickle.ListRecords(metadataPrefix="oai_dc", set=s.setSpec, ignore_deleted=True)
	    print("Records created.") # status update
	    file_count = 1
	    set_number += 1
	    record_number = 1
	    for record in records:
	        print("Set number: " + str(set_number) + " | " + "Record number " + str(record_number))
	        record_number += 1
	        if not os.path.exists(os.path.dirname('{}/data/{}-{}.xml'.format(s.setSpec, s.setSpec, file_count))):
	            try:
	                os.makedirs(os.path.dirname('{}/data/{}-{}.xml'.format(s.setSpec, s.setSpec, file_count)))
	            except OSError as exc: 
	                if exc.errno != errno.EEXIST:
	                    raise
	        with open('{}/data/{}-{}.xml'.format(s.setSpec, s.setSpec, file_count), 'w') as f:
	        	file_count += 1
	        	f.write(to_str(record.raw.encode('utf8')))
	        	f.close()
    		