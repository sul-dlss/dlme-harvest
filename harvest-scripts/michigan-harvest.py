#!/usr/bin/python
import json, os, requests, time

def main():
    directory = "output/michigan/data/"
    os.makedirs(os.path.dirname(directory), exist_ok=True)

    record_urls = []

    # Download json list at https://babel.hathitrust.org/cgi/mb?a=listis;c=1961411403
    data_path = '/Users/jtim/Dropbox/DLSS/DLME/dlme-harvest/harvest-scripts/output/1961411403-1622217526.json'
    with open(data_path, "r") as in_file:
        data = json.load(in_file)
        for record in data['gathers']:
            record_urls.append(record['catalog_url'] + '.xml')

    print("{} records found.".format(len(record_urls)))

    try:
        for count, record in enumerate(record_urls, start=1):
            metadata = requests.get(record)
            with open("{}michigan-{}.xml".format(directory, count), 'wb') as out_file:
                out_file.write(metadata.content)
                time.sleep(2)
    except:
        print('timeout')

if __name__ == "__main__":
    main()
