#!/usr/bin/python
import os
from sickle import Sickle
from sickle.iterator import OAIResponseIterator

def main():
    sickle = Sickle("http://dasi.cnr.it/de/cgi-bin/dasi-oai-x.pl")

    # Harvest specific listed sets
    # sets = ['epi_set', 'obj_set', 'obj_img_set']
    sets = ['obj_set']
    for s in sets:
        directory = "output/dasi/{}/data/".format(s)
        os.makedirs(os.path.dirname(directory), exist_ok=True)

        records = sickle.ListRecords(metadataPrefix='oai_dc', set=s, ignore_deleted=True)
        for counter, record in enumerate(records, start=1):
            with open('{}{}-{}.xml'.format(directory, s, counter), 'w') as f:
                f.write(record.raw)

if __name__ == "__main__":
    main()
