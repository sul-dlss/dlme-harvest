import io, json, logging, os, re, urllib.request
from argparse import ArgumentParser

logger = logging.getLogger("logger")

collections = {
    # "al-musawwar": "https://cdm15795.contentdm.oclc.org/iiif/info/p15795coll29/manifest.json",
    # "alexandria-bombardment": "https://cdm15795.contentdm.oclc.org/iiif/info/p15795coll9/manifest.json",
    "bint-al-nil": "https://cdm15795.contentdm.oclc.org/iiif/info/p15795coll19/manifest.json",
    # "campus-photos": "https://cdm15795.contentdm.oclc.org/iiif/info/p15795coll32/manifest.json",
    # "coptic": "https://cdm15795.contentdm.oclc.org/iiif/info/p15795coll4/manifest.json",
    # "creswell": "https://cdm15795.contentdm.oclc.org/iiif/info/p15795coll14/p1.json", # deviates from pattern
    # "fathy": "https://cdm15795.contentdm.oclc.org/iiif/info/p15795coll13/manifest.json",
    # "hopkins": "https://cdm15795.contentdm.oclc.org/iiif/info/p15795coll12/manifest.json",
    # "islamic-aa": "https://cdm15795.contentdm.oclc.org/iiif/info/p15795coll30/manifest.json",
    # "maps": "https://cdm15795.contentdm.oclc.org/iiif/info/p15795coll6/manifest.json",
    # "maritz": "https://cdm15795.contentdm.oclc.org/iiif/info/p15795coll16/manifest.json",
    # "napoleonic-egypt": "https://cdm15795.contentdm.oclc.org/iiif/info/p15795coll2/manifest.json",
    # "parker": "https://cdm15795.contentdm.oclc.org/iiif/info/p15795coll31/manifest.json",
    # "postcards": "https://cdm15795.contentdm.oclc.org/iiif/info/p15795coll21/manifest.json",
    # "qurna": "https://cdm15795.contentdm.oclc.org/iiif/info/p15795coll24/manifest.json",
    # "rare-books": "https://cdm15795.contentdm.oclc.org/iiif/info/p15795coll11/manifest.json",
    # "sphinx": "https://cdm15795.contentdm.oclc.org/iiif/info/sphinx/manifest.json",
    # "student-news": "https://cdm15795.contentdm.oclc.org/iiif/info/p15795coll26/p1.json", # deviates from normal pattern
    # "taxiphote-slides": "https://cdm15795.contentdm.oclc.org/iiif/info/p15795coll15/manifest.json",
    # "underwood": "https://cdm15795.contentdm.oclc.org/iiif/info/p15795coll8/manifest.json",
    # "university-on-the-square": "https://cdm15795.contentdm.oclc.org/iiif/info/p15795coll7/manifest.json",
    # "wassef": "https://cdm15795.contentdm.oclc.org/iiif/info/p15795coll5/manifest.json"
    }

def get_record_data(record_manifest_url):
    # Return the available fields in the record manifest
    data = {}
    manifest_response = urllib.request.urlopen(record_manifest_url).read()
    record_data = json.loads(manifest_response)
    data['manifest'] = record_manifest_url
    if '@id' in record_data:
        data['id'] = record_data['@id']
    if 'thumbnail' in record_data:
        data['thumbnail'] = record_data['thumbnail']['@id']
    if 'description' in record_data:
        data['description_top'] = record_data['description']
    try:
        data['resource'] = record_data['sequences'][0]['canvases'][0]['images'][0]['resource']['@id']
    except:
        try:
            data['resource'] = record_data['sequences'][0]['canvases'][1]['images'][0]['resource']['@id']
        except:
            logger.exception("Bad resource {}".format(record_manifest_url))
    try:
        data['profile'] = record_data['sequences'][0]['canvases'][0]['images'][0]['resource']['service']['profile']
    except:
        try:
            data['profile'] = record_data['sequences'][0]['canvases'][1]['images'][0]['resource']['service']['profile']
        except:
            logger.exception("Bad profile {}".format(record_manifest_url))
    try:
        data['iiif_format'] = record_data['sequences'][0]['canvases'][0]['images'][0]['resource']['format']
    except:
        try:
            data['iiif_format'] = record_data['sequences'][0]['canvases'][1]['images'][0]['resource']['format']
        except:
            logger.exception("Bad format {}".format(record_manifest_url))
    for i in record_data['metadata']:
        data[i['label'].replace(" ", "-").lower().replace('(', '').replace(')', '')] = i['value']
    if '@context' in record_data:
        data['context'] = record_data['@context']

    return data

def main():
    for k,v in collections.items():
        record_ids = []
        bad_responses = []
        forbidden = 0
        collection_response = urllib.request.urlopen(v)
        collection_data = json.load(collection_response)

        # Get record manifests and harvest data for each record
        for count, manifest in enumerate(collection_data['manifests'], start=1):
            if manifest['@id'] not in record_ids:
                record_ids.append(manifest['@id'])
                data = get_record_data(manifest['@id'])
                filename = 'output/auc/{}/data/{}-{}.json'.format(k, k, count)
                os.makedirs(os.path.dirname(filename), exist_ok=True)
                with io.open(filename, 'w') as out_file:
                    json.dump(data, out_file, ensure_ascii=False)
            else:
                print("Duplicate record: {}".format(manifest['@id']))

        print("{} of {} records were harvested from the '{}' collection.".format((count-forbidden), count, k))

if __name__ == "__main__":
    main()
