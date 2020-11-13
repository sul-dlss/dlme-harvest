import os

# Dictionary mapping institutions to sets that should not be harvested
do_not_harvest = {
                 "auc": ['p15795coll31', 'p15795coll32', 'p15795coll25', 'p15795coll29', 'p15795coll22', 'p15795coll7',
                 		'p15795coll3', 'p15795coll20', 'p15795coll17', 'p15795coll18'],
}

# Common helper functions
def to_str(bytes_or_str):
    '''Takes bytes or string and returns string'''
    if isinstance(bytes_or_str, bytes):
        value = bytes_or_str.decode('utf-8')
    else:
        value = bytes_or_str
    return value  # Instance of str

def write_records(records, directory):
    for counter, record in enumerate(records):
        os.makedirs(os.path.dirname(directory), exist_ok=True)
        with open('{}/{}.xml'.format(directory, counter), 'w') as f:
            f.write(to_str(record)) #.raw.encode('utf8')
    print('{} records written to {}'.format(counter, directory))
