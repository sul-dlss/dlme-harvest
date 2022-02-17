#!/usr/bin/python
import os
from sickle import Sickle
from sickle.iterator import OAIResponseIterator

def main():
    # Sets that have not been preioritized or permission has not been granted
    do_not_harvest = ['p15795coll3', 'p15795coll17', 'p15795coll18', 'p15795coll20',
                      'p15795coll22', 'p15795coll25']

    sickle = Sickle("http://cdm15795.contentdm.oclc.org/oai/oai.php")

    # Harvest specific listed sets
    specific_sets = {'kraus-meyerhof': 'p15795coll1', 'auc-historical-videos': 'p15795coll23'}
    for n,s in specific_sets.items():
        directory = "output/auc/{}/data/".format(n)
        os.makedirs(os.path.dirname(directory), exist_ok=True)

        records = sickle.ListRecords(metadataPrefix='oai_dc', set=s, ignore_deleted=True)
        for counter, record in enumerate(records, start=1):
            with open('{}{}-{}.xml'.format(directory, n, counter), 'w') as f:
                f.write(record.raw)

    # Or, harvest everything not in do_not_harvest
    # sets = sickle.ListSets()
    # for s in sets:
    #     if s.setSpec not in do_not_harvest:
    #         directory = "output/auc/{}/data/".format(s.setSpec)
    #         os.makedirs(os.path.dirname(directory), exist_ok=True)
    #
    #         records = sickle.ListRecords(metadataPrefix='oai_dc', set=s.setSpec, ignore_deleted=True)
    #         for counter, record in enumerate(records, start=1):
    #             with open('{}{}-{}.xml'.format(directory, s.setSpec, counter), 'w') as f:
    #                 f.write(record.raw)

if __name__ == "__main__":
    main()
