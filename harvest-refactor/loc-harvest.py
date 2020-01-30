import io, json, os, re, urllib.request, math, time

# Url to the collection manifest
collections = {
               'persian': 'https://www.loc.gov/collections/persian-language-rare-materials/?c=100&fo=json',
               'abdul-hamid-ii-books': 'https://www.loc.gov/collections/abdul-hamid-ii-books/?c=100&fo=json',
               'el-taher': 'https://www.loc.gov/collections/eltaher-collection/?c=100&fo=json',
               'abdul-hamid-ii-photos': 'https://www.loc.gov/collections/abdul-hamid-ii/?c=100&fo=json',
               'st-catherines-monastery': 'https://www.loc.gov/collections/manuscripts-in-st-catherines-monastery-mount-sinai/?c=100&fo=json',
               'greek-and-armenian-patriarchates': 'https://www.loc.gov/collections/greek-and-armenian-patriarchates-of-jerusalem/?c=100&fo=json'
               }

def main():
    total = 0
    for key, value in collections.items():
        try:
            record_count = 1
            # http connection
            user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
            values = {'name': 'Jacob Hill',
                      'location': 'Chapel Hill',
                      'language': 'Python' }
            headers = {'User-Agent': user_agent}
            data = urllib.parse.urlencode(values)
            data = data.encode('ascii')
            request = urllib.request.Request(value, data, headers)
            response = urllib.request.urlopen(request)
            collection_data = json.load(response)

            collection_pages = []
            for i in range(math.ceil(collection_data['pagination']['of'] / 100)):
                collection_pages.append('{}&sp={}'.format(value, i+1))

            for page in collection_pages:
                print('Harvesting {}'.format(page))
                request = urllib.request.Request(page, data, headers)
                response = urllib.request.urlopen(request)
                collection_data = json.load(response)

                for item in collection_data['results']:
                    filename = 'output/loc/{}/data/{}-{}.json'.format(key, key, record_count)
                    os.makedirs(os.path.dirname(filename), exist_ok=True)
                    with io.open(filename, 'w') as out_file:
                        json.dump(item, out_file, ensure_ascii=False)
                    record_count += 1
                time.sleep(3)

        except:
            pass

if __name__ == "__main__":
    main()
