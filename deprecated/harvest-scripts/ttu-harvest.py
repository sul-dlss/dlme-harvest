#!/usr/bin/python
import os
from sickle import Sickle
from sickle.iterator import OAIResponseIterator

def main():
    
    sickle = Sickle("https://swco-ir.tdl.org/oai/request?")

    # Harvest specific listed sets
    specific_sets = ['com_10605_355119']
    for s in specific_sets:
        directory = "output/texas-tech/tukish-oral-narrative/data/"
        os.makedirs(os.path.dirname(directory), exist_ok=True)

        records = sickle.ListRecords(metadataPrefix='oai_dc', set='com_10605_355119')
        for counter, record in enumerate(records, start=1):
            with open('{}tukish-oral-narrative-{}.xml'.format(directory, counter), 'w') as f:
                f.write(record.raw)

if __name__ == "__main__":
    main()
