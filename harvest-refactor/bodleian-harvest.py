import io, json, os, re, urllib.request

# Urls to the collection level iiif manifests for the Armenian, Hebrew, and Arabic mss collections
collection_urls = {'Hebrew': 'https://iiif.bodleian.ox.ac.uk/iiif/collection/hebrew', 'Armenian': 'https://iiif.bodleian.ox.ac.uk/iiif/collection/armenian',
                   'Arabic': 'https://iiif.bodleian.ox.ac.uk/iiif/collection/arabic'}

def get_record_data(record_manifest_url):
    # Return the available fields in the record manifest
    data = {}
    manifest_response = urllib.request.urlopen(record_manifest_url).read()
    record_data = json.loads(manifest_response)
    data['thumbnail'] = record_data['thumbnail']['@id']
    if 'description' in record_data:
        data['description'] = record_data['description']
    for i in record_data['metadata']:
        if i['label'].lower() == 'homepage':
            data['homepage'] = i['value'].lower().replace('<span><a href=\"', '').replace('\">view on digital bodleian</a></span>', '')
        else:
            data[i['label'].lower().replace(" ", "_")] = i['value']
    return data

def main():
    record_ids = []
    bad_responses = []
    forbidden = 0
    for key, value in collection_urls.items():
        collection_response = urllib.request.urlopen(value)
        collection_data = json.load(collection_response)
        # Get record manifests and harvest data for each record
        for count, manifest in enumerate(collection_data['manifests'], start=1):
            try:
                if manifest['@id'] not in record_ids:
                    record_ids.append(manifest['@id'])
                    data = get_record_data(manifest['@id'])
                    filename = 'output/bodleian/{}/data/{}-{}.json'.format(key, key, count)
                    os.makedirs(os.path.dirname(filename), exist_ok=True)
                    with io.open(filename, 'w') as out_file:
                        json.dump(data, out_file, ensure_ascii=False)
                else:
                    print("Duplicate record: {}".format(manifest['@id']))
            except:
                print("Bad response: {}".format(manifest['@id']))
                forbidden += 1
                bad_responses.append(manifest['@id'])
        # Try bad responses a second time
        # for url in bad_responses:
        #     try:
        #         data = get_record_data(url)
        #         filename = 'output/bodleian/{}/data/{}-{}.json'.format(key, key, count)
        #         os.makedirs(os.path.dirname(filename), exist_ok=True)
        #         with io.open(filename, 'w') as out_file:
        #             json.dump(data, out_file, ensure_ascii=False)
        #         bad_responses.remove(url)
        #     except:
        #         print("Second attempt to harvest {} failed".format(url))
    print(bad_responses)
        print("{} of {} records were harvested from the '{}' collection.".format((count-forbidden), count, key))

if __name__ == "__main__":
    main()
