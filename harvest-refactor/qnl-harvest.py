import errno
import os
from sickle import Sickle
from sickle.iterator import OAIResponseIterator

# where to write data to (relative to the dlme-harvest repo folder)
base_output_folder = 'output'

sickle = Sickle('https://api.qdl.qa/oaipmh')
print("Sickle instance created.") # status update

records = sickle.ListRecords(metadataPrefix='mods', ignore_deleted=True)
print("{} records created.".format(records.len())) # status update

directory = "output/qnl/data/"
os.makedirs(os.path.dirname(directory), exist_ok=True)

for count, record in enumerate(records, start=1):
    if count == 18108:
        pass
    # if record is None:
    #     print("None type found {}".format(count))
    else:
        try:
            print("Record number " + str(count))
            out_file = 'output/qnl/data/qnl-{}.xml'.format(count)
            directory_name = os.path.dirname(out_file)
            with open(out_file, 'w') as f:
            	f.write(record.raw)
        except Exception as err:
            print(err)
