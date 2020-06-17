import csv, io, json, os, re, urllib.request, math, time

def get_record_data(record_manifest_url):
    data = {}
    manifest_response = urllib.request.urlopen(record_manifest_url).read()
    record_data = json.loads(manifest_response)
    data['thumbnail'] = record_data['thumbnail']['@id']
    data['manifest'] = record_manifest_url
    if 'description' in record_data:
        joined_description = " "
        joined_description = joined_description.join(record_data['description'])
        data['description'] = joined_description
    for i in record_data['metadata']:
        data[i['label'].lower().replace(" ", "_")] = i['value']
    return data

def main():
    manifests = []
    with open('stanford-maps-druids.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            manifests.append("{}/iiif/manifest".format(row[5]))

    for count, manifest in enumerate(manifests, start=1):
        data = get_record_data(manifest)
        filename = 'output/stanford/rumsey-maps/data/rumsey-maps-{}.json'.format(count)
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with io.open(filename, 'w') as out_file:
            json.dump(data, out_file, ensure_ascii=False)

if __name__ == "__main__":
    main()
