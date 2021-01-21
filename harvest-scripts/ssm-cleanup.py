import glob, json, os
from lxml import etree

iiif_records = glob.glob('/Users/jtim/Dropbox/DLSS/DLME/dlme-harvest/harvest-scripts/output/abidindino-iiif/data/*.json')
xml_records = glob.glob('/Users/jtim/Dropbox/DLSS/DLME/dlme-harvest/harvest-scripts/output/abidindino-xml/data/*.xml')

iiif_ids = []
dupes = []

for record in iiif_records:
    with open(record) as f:
        data = json.load(f)
        iiif_ids.append(data['id'].replace('/manifest.json', '').split('/')[-1])

count = 0
for record in xml_records:
    with open(record) as f:
        tree = etree.parse(f)
        root = tree.getroot()
        id = root.find("{http://www.openarchives.org/OAI/2.0/}header/{http://www.openarchives.org/OAI/2.0/}identifier").text.split('/')[-1]
        if id in iiif_ids:
            dupes.append(record)
            print(record)
            count +=1
            os.remove(record)
print(count)
