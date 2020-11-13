import helper, os
from sickle import Sickle
from sickle.iterator import OAIResponseIterator

def main():
    # Create sickle instance
    sickle = Sickle("https://api.lib.harvard.edu/oai/")

    records = sickle.ListRecords(metadataPrefix='mods', ignore_deleted=True, set='ihp')
    print(records)
    out_path = 'output/harvard/harvard-ihp/data/'
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    for count, record in enumerate(records, start=1):
        with open('{}harvard-ihp-{}.xml'.format(out_path, count), 'w') as f:
            f.write(record.raw)

if __name__ == "__main__":
    main()
