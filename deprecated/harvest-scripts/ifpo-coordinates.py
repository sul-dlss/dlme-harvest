import csv, json, requests, time
from bs4 import BeautifulSoup

urls = ['https://medihal.archives-ouvertes.fr/medihal-00463237']

with open('output/ifpo/ifpo-data.csv', 'a') as out:
    writer = csv.writer(out)
    writer.writerow(['url', 'lat', 'long', 'subject_ar', 'subject_en', 'subject_fr'])
    with open('output/ifpo/output-ifpo.ndjson', 'r') as input:
        for count, line in enumerate(input.readlines(), start=1):
            print(f'trying {count} of {len(input.readlines())}')
            try:
                data = json.loads(line)
                url = data.get('agg_is_shown_at').get('wr_id')
                subject_ar = data.get('cho_subject').get('ar-Arab')
                subject_en = data.get('cho_subject').get('en')
                subject_fr = data.get('cho_subject').get('fr')
                r = requests.get(url)
                soup = BeautifulSoup(r.text, 'html.parser')
                script = soup.find('div', {'id': 'map-canvas'}).find_parent('div').find('script')
                lat = script.contents[0].split('var lat = ')[-1].split(';')[0]
                long = script.contents[0].split('var lon = ')[-1].split(';')[0]
                writer.writerow([url, lat, long, subject_ar, subject_en, subject_fr])
            except:
                print("failed")
            time.sleep(10)
