#!/usr/bin/python
import glob, io, json, os, requests, urllib
from selenium import webdriver
import pandas as pd
from lxml import etree
from bs4 import BeautifulSoup

def get_iiif_id(call_number):
    try:
        request = urllib.request.urlopen("https://collections.peabody.yale.edu/search/Record/{}".format(call_number).replace(' ', '-'))

        iiif_url = list(filter(lambda x: x.startswith("https://view.collections.yale.edu/m3/?"),
            (a["href"] for a in BeautifulSoup(request.read(), features="lxml").find_all("a", href=True))))[0]
        return iiif_url.split('&canvas=')[0].replace('https://view.collections.yale.edu/m3/?manifest=https://manifests.collections.yale.edu', '')
    except:
        return 'time out'

def get_image_from_manifest(iiif_id, call_number):
    try:
        if iiif_id == 'time out':
            print('Timeout found, trying again.')
            iiif_id = get_iiif_id(call_number)

        request = urllib.request.urlopen("https://manifests.collections.yale.edu/{}".format(iiif_id)).read()
        record_data = json.loads(request)

        return "https://images.collections.yale.edu/iiif/2/ypm:{}/full/full/0/default.jpg".format(record_data['items'][0].get('id').split('/')[-1])
    except:
        return 'time out'

def main():
    # The number of records divided by 500, check records when refreshing, select 'has media'
    # https://collections.peabody.yale.edu/search/Search/Results?join=AND&bool0%5B%5D=AND&lookfor0%5B%5D=BC&type0%5B%5D=AllFields&filter%5B%5D=%7Ecollection%3A%22Anthropology%22&filter%5B%5D=resource%3AResource+available+online
    # for i in range(1, 20, 1):
    #     request = urllib.request.urlopen("https://collections.peabody.yale.edu/search/Search/Results?join=AND&bool0%5B%5D=AND&lookfor0%5B%5D=BC&type0%5B%5D=AllFields&limit=100&page={}&filter%5B%5D=~collection%3A%22Anthropology%22&filter%5B%5D=resource%3A%22Resource+available+online%22&view=csv".format(i)).read()
    #     filename = "output/yale/babylonian/data/yale-{}.csv".format(i)
    #     os.makedirs(os.path.dirname(filename), exist_ok=True)
    #     with open(filename, 'wb') as out_file:
    #         out_file.write(request)

    extension = 'csv'
    all_filenames = [i for i in glob.glob('output/yale/babylonian/data/*.{}'.format(extension))]

    # for file in all_filenames:
    #     print('Working on file: {}'.format(file))
    #     df = pd.read_csv(file)
    #     df = df.drop_duplicates(subset="occurrence_id", keep='first', inplace=False)
    #     df['iiif_id'] = df.apply(lambda row : get_iiif_id(row['callnumber']), axis = 1)
    #     df['image_id'] = df.apply(lambda row : get_image_from_manifest(row['iiif_id'], row['callnumber']), axis = 1)
    #     df.to_csv( file, index=False, encoding='utf-8-sig')

    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])

    # bad_countries = ['USA', 'Mexico', 'Canada', 'Ecuador', 'Honduras', 'China', 'Malaysia', 'Peru', 'Korea', 'Italy', 'Guatemala', 'Greece']

    # Check countries again to make sure no countries are missing from the above list
    countries = combined_csv['format'].sort_values().unique()
    for c in countries:
        print(c+': Museum Object')

    # combined_csv = combined_csv[~combined_csv['geographic_country'].isin(bad_countries)]

    # for index, row in combined_csv.iterrows():
    #     if row['iiif_id'] == 'time out':
    #         get_image_from_manifest(get_iiif_id(row['callnumber']), row['callnumber'])

    # combined_csv = combined_csv.drop_duplicates(subset="occurrence_id", keep='first', inplace=False)

    # combined_csv['iiif_id'] = combined_csv.apply(lambda row : get_iiif_id(row['callnumber']), axis = 1)

    # combined_csv.to_csv( "output/yale/babylonian/data/yale-babylonian.csv", index=False, encoding='utf-8-sig')

if __name__ == "__main__":
    main()
