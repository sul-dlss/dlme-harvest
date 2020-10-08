import urllib.request, math, os, re, io, time
from lxml import etree




# Url to the collection manifest
# url = 'https://api.lib.harvard.edu/v2/items?q=%E2%80%9CStuart%20Cary%20Welch%20Islamic%20and%20South%20Asian%20Photograph%20Collection.%E2%80%9D'
url = 'https://api.lib.harvard.edu/v2/items?q=SCW2016.*&drsObjectId=*'

# add all namespaces
ns = {'xmlns:oai_dc': "http://www.openarchives.org/OAI/2.0/oai_dc/",
      'xmlns:marc': "http://www.loc.gov/MARC21/slim",
      'xmlns:xlink': "http://www.w3.org/1999/xlink",
      'xmlns:xs': "http://www.w3.org/2001/XMLSchema",
      'xmlns:HarvardDRS': "http://hul.harvard.edu/ois/xml/ns/HarvardDRS",
      'xmlns': "http://api.lib.harvard.edu/v2/item",
      'xmlns:sets': "http://hul.harvard.edu/ois/xml/ns/sets",
      'mods': "http://www.loc.gov/mods/v3",
      'xmlns:dc': "http://purl.org/dc/elements/1.1/",
      'xmlns:librarycloud': "http://hul.harvard.edu/ois/xml/ns/librarycloud",
      'xmlns:xsi': "http://www.w3.org/2001/XMLSchema-instance"}

def to_str(bytes_or_str):
    '''Takes bytes or string and returns string'''
    if isinstance(bytes_or_str, bytes):
        value = bytes_or_str.decode('utf-8')
    else:
        value = bytes_or_str

    return value  # Instance of str

def main():
    response = urllib.request.urlopen(url).read()
    tree = etree.fromstring(response)
    number_of_records = int(tree[0][1].text)
    print(str(number_of_records) + " records found.")
    limit = 100
    start_record = 9400 # the starting record is zero or 1 less than the digital_record_count
    iterations = math.ceil((number_of_records - start_record) / limit)
    digital_record_count = 9401 # the number for the file name
    for i in range(iterations):
        print("Harvesting batch {} of {}".format(i+1, iterations))
        batch_url = "{}&limit={}&start={}".format(url, limit, start_record)
        batch_response = urllib.request.urlopen(batch_url).read()
        tree = etree.fromstring(batch_response)
        start_record += limit
        # Get record manifests and harvest data for each record
        for record in tree[1]:
            filename = 'output/harvard/scw/data/scw-{}.xml'.format(digital_record_count)
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with io.open(filename, 'wb') as out_file:
                out_file.write(etree.tostring(record, pretty_print=True))
            digital_record_count += 1

        time.sleep(5) # the network seems to be throttling large downloads
    print("Harvested {} records".format(digital_record_count - 1))
if __name__ == "__main__":
    main()
