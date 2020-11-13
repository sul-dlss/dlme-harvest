import requests
import sys
import json
import re

PER_PAGE = 100 # 100 seems to be the max this API supports
TOTAL_RESULTS = 6175 # found by looking at the totalResults value from the API

# (department=3 corresponds to the Ancient Near Eastern Art department)
COLLECTION_LISTING_URL = 'https://metmuseum.org/api/collection/collectionlisting?department=3&showOnly=openAccess&perPage={per_page}&offset={offset}'
COOKIES = 'visid_incap_1661922=zeuzF5AvQfWEarqGk4nTIo8sgFwAAAAAQUIPAAAAAAANrejACMF3rOn44O3eDzZY; incap_ses_116_1661922=C6sBaULX+kKsxIrKgTmcAY8sgFwAAAAA1Gru/faBBF6yATIK5Zr2OQ==;'
DATA_FILE = 'collection_identifiers.txt'
FETCH_ID = re.compile(r"/(\d+)\?")

def get_item_id(line):
    url = line['url']
    match = FETCH_ID.search(url)
    if match is None:
        print('No identifier found in {}'.format(url))
        exit(1)
    return match.group(1)


# Hits the COLLECTION_LISTING_URL and writes the response to collection_listing.json
def fetch_json(file, offset=0):
    headers = {'Cookie': COOKIES }
    url = COLLECTION_LISTING_URL.format(per_page=str(PER_PAGE), offset=str(offset))
    print('Call to {}'.format(url))
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    if response.text.startswith('<html'):
      # This API doesn't return useful status_codes
      sys.stderr.write('The request failed, check cookies\n')
      exit(1)

    json = response.json()['results']
    for line in json:
        file.write(get_item_id(line))
        file.write('\n')



with open(DATA_FILE, "w") as file:
    for offset in range(0, TOTAL_RESULTS, PER_PAGE):
        fetch_json(file, offset)
