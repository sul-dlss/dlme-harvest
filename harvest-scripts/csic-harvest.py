import errno, os
from sickle import Sickle

sickle = Sickle('https://eu.alma.exlibrisgroup.com/view/oai/34CSIC_INST/request?')
print("Sickle instance created.") # status update

directory = "output/csic/data/"
os.makedirs(os.path.dirname(directory), exist_ok=True)

records = sickle.ListRecords(
             **{'metadataPrefix': 'marc21',
             'from': '2020-01-01',
             'set': 'manuscripta',
             'ignore_deleted': True
            })
print("Records created.") # status update
print(records)
for count, record in enumerate(records, start=1):
    with open('{}csic-{}.xml'.format(directory, count), 'w') as f:
    	# f.write(to_str(record.raw.encode('utf8')))
        f.write(record.raw)
        print('Record {} written'.format(count))
