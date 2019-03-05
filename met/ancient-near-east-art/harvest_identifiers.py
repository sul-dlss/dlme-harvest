import requests
import sys
import json
import re

PER_PAGE = 100 # 100 seems to be the max this API supports
TOTAL_RESULTS = 6175 # found by looking at the totalResults value from the API

# (department=3 corresponds to the Ancient Near Eastern Art department)
COLLECTION_LISTING_URL = 'https://metmuseum.org/api/collection/collectionlisting?department=3&showOnly=openAccess&perPage=:per_page&offset=:page'
COOKIES = 'visid_incap_1661922=gIv8fJeISGGcJv0NPFp8CrqodlwAAAAAQkIPAAAAAACA0IKKAUgy2kw+zt//Ldn6njTuEdrNgU5h; incap_ses_116_1661922=bbTncN2klDMCuwKCfzmcAUTCflwAAAAAz69U/RVQ60rLyC5m76xvqQ==; visid_incap_1661977=3hA+zJCRRzuUunC4kljKEWa/dlwAAAAAQUIPAAAAAABop7jZ/Qyw7ASd4P6CBM1D; incap_ses_116_1661977=fBTTDMMiijrHhSh2fzmcAWa/dlwAAAAAwC9Zj2Eg4Bv0E68vqj7+Ow=='
DATA_FILE = 'collection_identifiers.txt'
FETCH_ID = re.compile(r"/(\d+)\?")

def get_item_id(line):
    url = line['url']
    match = FETCH_ID.search(url)
    if match is None:
        print(f'No identifier found in {url}')
        exit(1)
    return match.group(1)


# Hits the COLLECTION_LISTING_URL and writes the response to collection_listing.json
def fetch_json(file, page=0):
    headers = {'Cookie': COOKIES }
    url = COLLECTION_LISTING_URL.replace(':page', str(page)).replace(':per_page', str(PER_PAGE))
    print(f'Call to {url}')
    response = requests.get(url, headers=headers)

    if response.text.startswith('<html'):
      # This API doesn't return useful status_codes
      sys.stderr.write('The request failed, check cookies\n')
      exit(1)

    doc = json.loads(response.text)
    for line in doc['results']:
        file.write(get_item_id(line=line))
        file.write('\n')



f = open(DATA_FILE, "w")
for i in range(0, TOTAL_RESULTS, PER_PAGE):
    fetch_json(file=f, page=i)
