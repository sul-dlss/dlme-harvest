#!/usr/bin/python
import json, os, requests

def main():
    directory = "output/michigan/data/"
    os.makedirs(os.path.dirname(directory), exist_ok=True)

    record_urls = ['https://catalog.hathitrust.org/Record/006806667.xml']

    # Download json list at https://babel.hathitrust.org/cgi/mb?a=listis;c=1961411403
    # data_path = '/Users/jtim/Dropbox/DLSS/DLME/dlme-harvest/harvest-refactor/output/michigan/1961411403-1564405820.json'
    # with open(data_path, "r") as in_file:
    #     data = json.load(in_file)
    #     for record in data['gathers']:
    #         record_urls.append(record['catalog_url'] + '.xml')

    try:
        for count, record in enumerate(record_urls, start=1):
            metadata = requests.get(record)
            with open("{}{}.xml".format(directory, count), 'wb') as out_file:
                out_file.write(metadata.content)
    except:
        print('timeout')

if __name__ == "__main__":
    main()
