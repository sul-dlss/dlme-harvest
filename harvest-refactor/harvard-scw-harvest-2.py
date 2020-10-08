import helper, os
from sickle import Sickle
from sickle.iterator import OAIResponseIterator



# Url to the collection manifest
url = 'https://api.lib.harvard.edu/v2/items?q=%E2%80%9CStuart%20Cary%20Welch%20Islamic%20and%20South%20Asian%20Photograph%20Collection.%E2%80%9D'
def main():
    # Create sickle instance
    sickle = Sickle(url)

    records = sickle.ListRecords(ignore_deleted=True)
    print(records)
    out_path = 'output/harvard/harvard-scw/data/'
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    for count, record in enumerate(records, start=1):
        with open('{}harvard-scw-{}.xml'.format(out_path, count), 'w') as f:
            f.write(record.raw)

if __name__ == "__main__":
    main()
