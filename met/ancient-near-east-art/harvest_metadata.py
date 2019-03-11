import requests
import sys
import json
import re
import os

IDENTIFIER_FILE = 'collection_identifiers.txt'
# (department=3 corresponds to the Ancient Near Eastern Art department)
ITEM_URL = 'https://collectionapi.metmuseum.org/public/collection/v1/objects/{id}'

OUTPUT_DIR = 'out/'

# Hits the ITEM_URL and writes the response to out/:id.json
def harvest_item(id):
    output_filepath = os.path.join(OUTPUT_DIR, '{}.json'.format(id))
    if os.path.exists(output_filepath):
        print('Skipping {}'.format(id))
        return

    print('Harvesting {}'.format(id))
    url = ITEM_URL.format(id=id)

    response = requests.get(url)

    if response.text.startswith('<html'):
      # This API doesn't return useful status_codes
      sys.stderr.write('The request to {} failed, check cookies\n'.format(url))
      print(response.text)
      exit(1)
    with open(output_filepath, 'w') as f:
        f.write(response.text)


with open(IDENTIFIER_FILE) as f:
    identifiers = f.readlines()

for id in identifiers:
    harvest_item(id.rstrip())
