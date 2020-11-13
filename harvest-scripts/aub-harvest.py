#!/usr/bin/python
import os
from sickle import Sickle
from sickle.iterator import OAIResponseIterator

def main():
    sickle = Sickle("https://libraries.aub.edu.lb/xtf/oai")
    sets = ['al-adab', 'postcards']
    for s in sets:
        directory = "output/aub/{}/data/".format(s)
        os.makedirs(os.path.dirname(directory), exist_ok=True)

        records = sickle.ListRecords(metadataPrefix='oai_dc', set='postcards', ignore_deleted=True)
        for counter, record in enumerate(records, start=1):
            with open('{}{}-{}.xml'.format(directory, s, counter), 'w') as f:
                f.write(record.raw)

if __name__ == "__main__":
    main()
