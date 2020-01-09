import io, json, os, re, urllib.request, math

# Url to the collection manifest
url = 'https://api.lib.harvard.edu/v2/items.json?q=%E2%80%9CStuart%20Cary%20Welch%20Islamic%20and%20South%20Asian%20Photograph%20Collection.%E2%80%9D'

def main():
    collection_response = urllib.request.urlopen(url)
    collection_data = json.load(collection_response)
    number_found = collection_data['pagination']['numFound']
    limit = 250 # the number of records returned in each batch
    iterations = math.ceil(number_found / limit)
    digital_record_count = 11755
    start = digital_record_count + 1 # the starting record for each batch
    for i in range(iterations):
        print("Harvesting batch {} of {}".format(i+1, iterations))
        batch_url = "{}&limit=250&start={}".format(url, start)
        batch_response = urllib.request.urlopen(batch_url)
        batch_data = json.load(batch_response)
        start += limit
        # Get record manifests and harvest data for each record
        for record in batch_data['items']['mods']:
            try:
                record_url = record['location']['url']['#text']
                record_in_context = urllib.request.urlopen(record_url).read().decode("utf8")
                pattern_matches = re.findall(r"onclick=\"copyManifestToClipBoard([^)]*)", record_in_context)
                iiif_manifest_url = pattern_matches[0].replace('onclick="copyManifestToClipBoard(', '').strip('(').strip("'")
                iiif_manifest = {'iiif_manifest': iiif_manifest_url}
                record.update(iiif_manifest)
                filename = 'output/harvard/scw/data/scw-{}.json'.format(digital_record_count)
                os.makedirs(os.path.dirname(filename), exist_ok=True)
                with io.open(filename, 'w') as out_file:
                    json.dump(record, out_file, ensure_ascii=False)
                digital_record_count += 1
            except:
                try:
                    for i in record['location']:
                        try:
                            record_url = i['url']['#text']
                            record_in_context = urllib.request.urlopen(record_url).read().decode("utf8")
                            pattern_matches = re.findall(r'onclick="copyManifestToClipBoard([^)]*)', record_in_context)
                            iiif_manifest_url = pattern_matches[0].replace('onclick="copyManifestToClipBoard(', '').strip('(').strip("'")
                            iiif_manifest = {'iiif_manifest': iiif_manifest_url}
                            record.update(iiif_manifest)
                            filename = 'output/harvard/scw/data/scw-{}.json'.format(digital_record_count)
                            os.makedirs(os.path.dirname(filename), exist_ok=True)
                            with io.open(filename, 'w') as out_file:
                                json.dump(record, out_file, ensure_ascii=False)
                            digital_record_count += 1
                        except:
                            filename = 'output/harvard/scw/data/scw-{}.json'.format(digital_record_count)
                            os.makedirs(os.path.dirname(filename), exist_ok=True)
                            with io.open(filename, 'w') as out_file:
                                json.dump(record, out_file, ensure_ascii=False)
                            digital_record_count += 1
                except:
                    print("here")
    print("Harvested {} records".format(digital_record_count))
if __name__ == "__main__":
    main()
