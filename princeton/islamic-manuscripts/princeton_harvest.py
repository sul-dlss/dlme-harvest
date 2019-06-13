import io, json, os, re, urllib.request

# Urls to the collection level iiif manifests for the Yemeni Digital Manuscript Initiative and Prinecton Islamic Manuscript collections
collection_urls = {'princeton_ymdi': 'https://figgy.princeton.edu/collections/eff75507-11bf-486b-b422-8fe29638b060/manifest',
                  'princeton_mss': 'https://figgy.princeton.edu/collections/52abe8f7-e2a1-46e9-9d13-3dc4fbc0bf0a/manifest'}

# collection_urls = {'princeton_mss': 'https://figgy.princeton.edu/collections/52abe8f7-e2a1-46e9-9d13-3dc4fbc0bf0a/manifest'}
def main():
    forbidden = 0
    count = 1
    for key, value in collection_urls.items():
        collection_response = urllib.request.urlopen(value)
        collection_data = json.load(collection_response)
        for manifest in collection_data['manifests']:
            try:
                data = {}
                # Get data from collection iiif manifest_response
                data['thumbnail'] = manifest['thumbnail']['@id']
                manifest_response = urllib.request.urlopen(manifest['@id']).read()
                record_data = json.loads(manifest_response)
                # Get data from record iiif manifest
                if 'description' in record_data:
                    joined_description = " "
                    joined_description = joined_description.join(record_data['description'])
                    data['description'] = joined_description
                else:
                    continue
                for i in record_data['metadata']:
                    if i['label'].lower() == "identifier":
                        data['identifier'] = re.findall("(?P<url>https?://[^\s]+)", i['value'][0])[0].strip("'")
                        data['alternate_identifier'] = re.findall("(?P<url>https?://[^\s]+)", i['value'][0])[1].strip("</a>")
                    elif i['label'].lower() == "title":
                        for t in i['value']:
                            data['title'] = t['@value']
                    else:
                        for j in i['value']:
                            data[i['label'].lower().replace(" ", "_")] = j

                filename = 'output/{}/data/{}-{}.json'.format(key, key, count)
                os.makedirs(os.path.dirname(filename), exist_ok=True)
                with io.open(filename, 'w') as out_file:
                # with io.open('output/{}/data/{}-{}.json'.format(key, key, count), 'w') as out_file:
                    json.dump(data, out_file, ensure_ascii=False)
                    count += 1
            except:
                print("Bad url")
                forbidden += 1
        count = 1
    print(forbidden)
if __name__ == "__main__":
    main()
