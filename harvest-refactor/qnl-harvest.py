import errno
import os
from sickle import Sickle
from sickle.iterator import OAIResponseIterator

sickle = Sickle('https://api.qdl.qa/oaipmh')
print("Sickle instance created.") # status update

# Set the resumption token to 0 to start or any number to continue from
records = sickle.ListRecords(resumptionToken='34155mods')
print("Records created.") # status update

directory = "output/qnl/data/"
os.makedirs(os.path.dirname(directory), exist_ok=True)

# Change start to the resumption token plus 1
for count, record in enumerate(records, start=34156):
    try:
        print("Record number " + str(count))
        out_file = 'output/qnl/data/qnl-{}.xml'.format(count)
        directory_name = os.path.dirname(out_file)
        with open(out_file, 'w') as f:
        	f.write(record.raw)
    except Exception as err:
        print(err)
