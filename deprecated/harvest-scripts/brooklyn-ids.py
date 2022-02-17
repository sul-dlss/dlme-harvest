import json
import os
import requests

# api_endpoint = "https://www.brooklynmuseum.org/api/v2/collection/20/object?start={}"

headers = {
    "api_key" : "0IzFpBiUksT8LMVGLUxovj9IR0ltlSH1"
}
offset=1
limit=25 # max 34
harvested=0

# Islamic Art
# records=1506
# with open('brooklyn-museum/record-ids/islamic-art.json', 'a') as out:
#     ids = []
#     while harvested < records:
#         api_endpoint = f"https://www.brooklynmuseum.org/api/v2/collection/20/object?limit={limit}&offset={offset}"
#         print(f"Harvested: {api_endpoint}.")
#         response = requests.get(
#             api_endpoint,
#             headers = headers
#         )
#         offset+=limit
#         harvested+=limit
#         print(response)
#         for i in response.json()['data']:
#             ids.append(i)
#
#     json.dump(ids, out)

# Near East and Egyptian collection
records = 8786
with open('brooklyn-museum/record-ids/near-east-and-egyptian.json', 'a') as out:
    ids = []
    while harvested < records:
        api_endpoint = f"https://www.brooklynmuseum.org/api/v2/collection/5/object?limit={limit}&offset={offset}"
        print(f"Harvested: {api_endpoint}.")
        response = requests.get(
            api_endpoint,
            headers = headers
        )
        offset+=limit
        harvested+=limit
        print(response)
        for i in response.json()['data']:
            ids.append(i)

    json.dump(ids, out)
