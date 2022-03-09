#!/usr/bin/python
import json, io, os, requests, urllib

other_cultures = []
def main():
    directory = "output/walters-art-museum/data/"
    os.makedirs(os.path.dirname(directory), exist_ok=True)
    file_count = 1
    page = 1
    next = True
    cultures = ['Achaemenid', 'Akkadian', 'Aramean', 'Assyrian', 'Babylonian', 'Canaanite', 'Coptic', 'Egypt', 'Egyptian', 'Egyptian-Islamic', 'Eblaite or Akkadia', 'Hittite', 'Iranian', 'Iranian-Islamic', 'Islamic', 'Islamic; Persian', 'Kassite', 'Isin Larsa; Old Babylonian', 'Mesopotamian', 'Neo-Sumerian', 'Neo-Sumerian?', 'Nubian', 'Neo-Babylonian (?); Assyrian (?)', 'Old Babylonian', 'Old-Babylonian', 'Ottoman-Islamic', 'Persian', 'Phoenician', 'Phoenician?', 'Phoenician (?)', 'post-Akkadian; Ur III', 'Sasanian', 'Syrian', 'Syro-Palestine', 'Sumerian', 'Yemeni', 'Zaydi Muslim']
    while next == True:
        response = urllib.request.urlopen('http://api.thewalters.org/v1/objects.json?apikey=nlyO2MGAtLM1R8tP9AEYsM1lBgOcsPOs5v4oPimXWzEYzaebZuyYnUFRjDDMxdIT&Page={}&PageSize=200'.format(page)).read()
        data = json.loads(response)
        page+=1
        next = data['NextPage']
        for i in data['Items']:
            if i.get('Culture') in cultures:
                filename = 'output/walters-art-museum/data/walters-{}.json'.format(file_count)
                file_count+=1
                with io.open(filename, 'w') as out_file:
                    json.dump(i, out_file, ensure_ascii=False)
            elif i.get('Culture') != None:
                other_cultures.append(i.get('Culture'))

    print('These cultures were not harvested:')
    for i in set(other_cultures):
        print(i)

if __name__ == "__main__":
    main()

# http://api.thewalters.org/v1/objects?apikey=nlyO2MGAtLM1R8tP9AEYsM1lBgOcsPOs5v4oPimXWzEYzaebZuyYnUFRjDDMxdIT
#
# Collection=Islamic Art
#
# Collection=Manuscripts (filture by culture)
#
# Culture=Islamic
# Culture=Egyptian
# Culture=Egyptian-Islamic
# Old-Babylonian
# Assyrian
