import helper, os
from sickle import Sickle
from sickle.iterator import OAIResponseIterator

def main():
    # Create sickle instance
    sickle = Sickle("https://api.lib.harvard.edu/oai/", iterator=OAIResponseIterator)

    records = sickle.ListRecords(metadataPrefix='oai_dc', ignore_deleted=True, set='ihp') # sickle.ListRecords(ignore_deleted=True)
    out_path = 'output/harvard/harvard-ihp/data/'
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    for count, record in enumerate(records, start=1):
        with open('harvard-ihp-{}.xml'.format(count), 'w') as f:
            f.write(records.next().raw.encode('utf8'))

if __name__ == "__main__":
    main()
