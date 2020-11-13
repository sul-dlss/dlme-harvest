#!/usr/bin/python
import json, os, requests

collections = ["https://cudl.lib.cam.ac.uk/iiif/collection/islamic", "https://cudl.lib.cam.ac.uk/iiif/collection/hebrew", "https://cudl.lib.cam.ac.uk/iiif/collection/genizah"]
def main():

    for collection in collections:
        collection_name = collection.split("/")[-1].lower()
        directory = "output/cambridge/{}/data".format(collection_name)
        os.makedirs(os.path.dirname(directory), exist_ok=True)

        collection_manifest = json.loads(requests.get(collection).text)

        items = collection_manifest["manifests"]
        for counter, item in enumerate(items, start=1):
            id = item["@id"].split("/")[-1]
            item_metadata_url = "https://services.cudl.lib.cam.ac.uk/v1/metadata/tei/{}".format(id)
            try:
                item_metadata = requests.get(item_metadata_url).text
                with open("{}{}-{}.xml".format(directory, collection_name, counter), "w") as out_file:
                    out_file.write(item_metadata)
            except:
                print("Error")

if __name__ == "__main__":
    main()
