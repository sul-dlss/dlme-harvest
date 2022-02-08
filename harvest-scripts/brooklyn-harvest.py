import json
import requests

headers = {
    "api_key" : "0IzFpBiUksT8LMVGLUxovj9IR0ltlSH1"
}

# with open('/Users/jtim/Desktop/brooklyn-museum/record-ids/islamic-art.json', 'r') as f:
#     data = json.load(f)
#
#     for count, i in enumerate(data, start=1):
#         api_endpoint = f"https://www.brooklynmuseum.org/api/v2/object/{i['id']}"
#         try:
#             response = requests.get(
#                 api_endpoint,
#                 headers = headers
#             )
#             with open(f'brooklyn-museum/islamic-art/brooklin-islamic-art-{count}.json', 'w') as out:
#                 json.dump(response.json()['data'], out)
#                 print(f'{count} of {len(data)} complete.')
#         except:
#             pass

with open('/Users/jtim/Desktop/brooklyn-museum/record-ids/near-east-and-egyptian.json', 'r') as f:
    data = json.load(f)

    for count, i in enumerate(data, start=1):
        api_endpoint = f"https://www.brooklynmuseum.org/api/v2/object/{i['id']}"
        try:
            response = requests.get(
                api_endpoint,
                headers = headers
            )
            with open(f'brooklyn-museum/near-east-egyptian/brooklin-near-east-egyptian-{count}.json', 'w') as out:
                json.dump(response.json()['data'], out)
                print(f'{count} of {len(data)} complete.')
        except:
            pass
