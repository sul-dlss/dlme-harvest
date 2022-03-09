#!/usr/bin/python
import os
from sickle import Sickle
from sickle.iterator import OAIResponseIterator

def main():
    sickle = Sickle("https://api.archives-ouvertes.fr/oai/hal")
    sets = ['collection:IFPOIMAGES']
    for s in sets:
        directory = "output/ifpo/{}/data/".format(s.split(':'[-1]))
        os.makedirs(os.path.dirname(directory), exist_ok=True)

        records = sickle.ListRecords(metadataPrefix='oai_dc', set=s, ignore_deleted=True)
        for counter, record in enumerate(records, start=1):
            with open('{}{}-{}.xml'.format(directory, s, counter), 'w') as f:
                f.write(record.raw)

if __name__ == "__main__":
    main()
