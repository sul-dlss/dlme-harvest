import helper, os
from sickle import Sickle
from sickle.iterator import OAIResponseIterator

def main():
    # Create sickle instance
    sickle = Sickle("https://luna.manchester.ac.uk/luna/servlet/oai")

    # Middle East related sets
    specific_sets = {'Nashriyah': 'Manchester~18~18',
                     'Genizah': 'ManchesterDev~95~2',
                     'Hebraica': 'Manchester~10~10',
                     'Papyri': 'ManchesterDev~93~3'}

    for k,v in specific_sets.items():
        try:
            records = sickle.ListRecords(metadataPrefix='oai_dc', ignore_deleted=True, set=v)
            out_path = 'output/manchester/{}/data/'.format(k)
            if not os.path.exists(out_path):
                os.makedirs(out_path)
            for count, record in enumerate(records, start=1):
                with open('{}{}-{}.xml'.format(out_path, k, count), 'w') as f:
                    f.write(record.raw)
        except Exception as err:
            print(err)

if __name__ == "__main__":
    main()
