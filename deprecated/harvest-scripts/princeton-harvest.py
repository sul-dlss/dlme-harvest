import io, json, os, re, urllib.request

# Urls to the collection level iiif manifests for the Movie Posters, the Yemeni Digital Manuscript Initiative and Prinecton Islamic Manuscript collections
collection_urls = {'princeton-mss': 'https://figgy.princeton.edu/collections/52abe8f7-e2a1-46e9-9d13-3dc4fbc0bf0a/manifest',
                   'princeton-ymdi': 'https://figgy.princeton.edu/collections/eff75507-11bf-486b-b422-8fe29638b060/manifest',
                   'princeton-movie-posters': 'https://figgy.princeton.edu/collections/2ce536fa-8c6e-4f1d-b411-29a28fe188d5/manifest'}

def get_record_data(record_manifest_url):
    data = {}
    manifest_response = urllib.request.urlopen(record_manifest_url).read()
    record_data = json.loads(manifest_response)
    data['thumbnail'] = record_data['thumbnail']['@id']
    if 'description' in record_data:
        joined_description = " "
        joined_description = joined_description.join(record_data['description'])
        data['description'] = joined_description
    for i in record_data['metadata']:
        if i['label'].lower() == "identifier":
            if re.findall("(?P<url>https?://[^\s]+)", i['value'][0]):
                data['identifier'] = re.findall("(?P<url>https?://[^\s]+)", i['value'][0])[0].strip("'")
                data['alternate_identifier'] = re.findall("(?P<url>https?://[^\s]+)", i['value'][0])[1].strip("</a>")
            else:
                data['identifier'] = i['value'][0].strip("ark:/88435/")
                if i['label'].lower() == "local identifier":
                    data['alternate_identifier'] = i['value'][0]
        elif i['label'].lower() == "title":
            for t in i['value']:
                data['title'] = t['@value']
        elif i['label'].lower() == "director":
            for j in i['value']:
                data['director'] = i['value'][0]['@value']
        else:
            for j in i['value']:
                data[i['label'].lower().replace(" ", "_")] = j
    return data

def get_bad_response_data(record_manifest_url):
    data = {}
    manifest_response = urllib.request.urlopen(record_manifest_url).read()
    record_data = json.loads(manifest_response)
    data['thumbnail'] = record_data['thumbnail']['@id']
    if 'description' in record_data:
        joined_description = " "
        joined_description = joined_description.join(record_data['description'])
        data['description'] = joined_description
    for i in record_data['metadata']:
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
                    filename = 'output/princeton/{}/data/{}-{}.json'.format(key, key, count)
                    os.makedirs(os.path.dirname(filename), exist_ok=True)
                    with io.open(filename, 'w') as out_file:
                        json.dump(data, out_file, ensure_ascii=False)
            except:
                print("Bad response: {}".format(manifest['@id']))
                forbidden += 1
                bad_responses.append(manifest['@id'])
        # Bad responses have a differnt pattern
        # for count, url in enumerate(bad_responses, start=1):
        #     try:
        #         data = get_bad_response_data(url)
        #         filename = 'output/princeton/bad-responses/data/{}.json'.format(count)
        #         os.makedirs(os.path.dirname(filename), exist_ok=True)
        #         with io.open(filename, 'w') as out_file:
        #             json.dump(data, out_file, ensure_ascii=False)
        #         bad_responses.remove(url)
        #     except:
        #         print("Second attempt to harvest {} failed".format(url))
    # print("{} of {} records were harvested from the '{}' collection.".format((count-forbidden), count, key))


if __name__ == "__main__":
    main()
