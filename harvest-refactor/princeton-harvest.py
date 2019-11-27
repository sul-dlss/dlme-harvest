import io, json, os, re, urllib.request
from bs4 import BeautifulSoup

# Urls to the collection level iiif manifests for the Movie Posters, the Yemeni Digital Manuscript Initiative and Prinecton Islamic Manuscript collections
collection_urls = { 'islamic_mss': 'https://figgy.princeton.edu/collections/52abe8f7-e2a1-46e9-9d13-3dc4fbc0bf0a/manifest',
                    'yemeni_mss': 'https://figgy.princeton.edu/collections/eff75507-11bf-486b-b422-8fe29638b060/manifest'}
# 'princeton-movie-posters': 'https://figgy.princeton.edu/collections/2ce536fa-8c6e-4f1d-b411-29a28fe188d5/manifest'

def main():
    manifest_urls = []
    record_ids = []
    bad_responses = []
    forbidden = 0
    # Grab all of the manifest urls and check for duplicates
    for key, value in collection_urls.items():
        collection_response = urllib.request.urlopen(value)
        collection_data = json.load(collection_response)
        # Get record manifests and harvest data for each record
        for manifest in collection_data['manifests']:
            # The collections have overlapping membership
            # ensure each record is havested only once
            if manifest['@id'] not in manifest_urls:
                manifest_urls.append(manifest['@id'])
            else:
                print("Already harvested this manifest url: " + manifest['@id'])
    # Harvest all records, splitting directories by title object type for easy mapping
    for count, manifest_url in enumerate(manifest_urls, start=1):
        try:
            data = {}
            data['iiif_manifest'] = manifest_url
            manifest_response = urllib.request.urlopen(manifest_url).read()
            record_data = json.loads(manifest_response)
            english_vowels = ['a', 'e', 'i', 'o', 'u']
            for i in record_data['metadata']:
                if i['label'] == 'Identifier':
                    if i['value'][0] not in record_ids:
                        if 'thumbnail' in record_data:
                            data['thumbnail'] = record_data['thumbnail']['@id']
                        if 'rendering' in record_data:
                            data['rendering'] = record_data['rendering']['@id']
                        if 'description' in record_data:
                            joined_description = " "
                            joined_description = joined_description.join(record_data['description'])
                            data['description'] = joined_description
                        # Get all metadata fields without alteration
                        for i in record_data['metadata']:
                            data[i['label'].lower().replace(" ", "_")] = i['value']
                            # Parse contributor by language
                            if i['label'] == 'Contributor':
                                for contributor in i['value']:
                                    for vowel in english_vowels:
                                        if vowel in contributor.replace('or', 'يا'):
                                            data['dlme_contributor_ara_latn'] = contributor
                                            break
                                        else:
                                            data['dlme_contributor_ara_arab'] = contributor
                            # Parse creator by language
                            if i['label'] == 'Creator':
                                for creator in i['value']:
                                    for vowel in english_vowels:
                                        if vowel in creator.replace('or', 'يا'):
                                            data['dlme_creator_ara_latn'] = creator
                                            break
                                        else:
                                            data['dlme_creator_ara_arab'] = creator
                            # Parse provenance by language
                            if i['label'] == 'Provenance':
                                for provenance in i['value']:
                                    for vowel in english_vowels:
                                        if vowel in provenance:
                                            data['dlme_provenance_en'] = provenance
                                            break
                                        else:
                                            data['dlme_provenance_ara_arab'] = provenance
                            # Map the different data structures of the title field to consistent structures
                            if i['label'] == 'Title':
                                for title in i['value']:
                                    if '@language' in title:
                                        if title['@language'] == 'ara':
                                            for vowel in english_vowels:
                                                if vowel in title['@value']:
                                                    data['dlme_title_ara_latn'] = title['@value']
                                                    break
                                                else:
                                                    data['dlme_title_ara_arab'] = title['@value']
                                        elif title['@language'] == 'ara-latn':
                                            data['dlme_title_ara_latn'] = title['@value']
                                        elif title['@language'] == 'ota-latn':
                                            data['dlme_title_ota_latn'] = title['@value']
                                        elif title['@language'] == 'ota':
                                            for vowel in english_vowels:
                                                if vowel in title['@value']:
                                                    data['dlme_title_ota_latn'] = title['@value']
                                                    break
                                                else:
                                                    data['dlme_title_ota_arab'] = title['@value']
                                        elif title['@language'] == 'fas':
                                            for vowel in english_vowels:
                                                if vowel in title['@value']:
                                                    data['dlme_title_per_latn'] = title['@value']
                                                    break
                                                else:
                                                    data['dlme_title_per_arab'] = title['@value']
                                        elif title['@language'] == 'fas-latn':
                                            data['dlme_title_per_latn'] = title['@value']
                                        elif title['@language'] == 'msa': # one title tagged msa but its English
                                            data['dlme_title_en'] = title['@value']
                                        elif title['@language'] == 'urd-latn':
                                            data['dlme_title_urdu_latn'] = title['@value']
                                        elif title['@language'] == 'urd':
                                            data['dlme_title_urdu_latn'] = title['@value']
                                        else:
                                            print(title['@language'])
                                    else:
                                        data['dlme_title_none'] = i['value']
                        filename = "output/princeton/princeton_mss/mss-{}.json".format(count)
                        os.makedirs(os.path.dirname(filename), exist_ok=True)
                        with io.open(filename, 'w') as out_file:
                            json.dump(data, out_file, ensure_ascii=False)
                        record_ids.append(i['value'][0])
                    else:
                        print('Duplicate: {}'.format(i['value'][0]))
        except:
            print('Bad url: {}'.format(manifest['@id']))
    print(bad_responses)
    print("{} of {} records were harvested from the Princeton Manuscript collections.".format((count-forbidden), count))

if __name__ == "__main__":
    main()
