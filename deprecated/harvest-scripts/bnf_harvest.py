'''harvest script for BnF Gallica records'''
from datetime import datetime
from pathlib import Path
from xml.etree import ElementTree
import glob
import logging
import requests

Path("output/bnf").mkdir(parents=True, exist_ok=True)

# Set up logging.
logging.basicConfig()
logging.root.setLevel(logging.NOTSET)
FORMAT = '%(asctime)s:%(name)s:%(levelname)s - %(message)s'
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.basicConfig(filename='output/bnf/harvest.log', format=FORMAT, level=logging.INFO)

# Add data set url from web application UI and a name for the collection.
BNF_DATA = {
    'IDEO': '''https://gallica.bnf.fr/services/engine/search/sru?operation=searchRetrieve&version=
            1.2&startRecord={}&maximumRecords=50&page={}&collapsing=true&exactSearch=false&query=
            %28%28bibliotheque%20adj%20%22Institut%20dominicain%20d%27%C3%A9tudes%20orientales
            %22%29%29#resultat-id-3''',
    'IFAO': '''https://gallica.bnf.fr/services/engine/search/sru?operation=searchRetrieve&version=
            1.2&startRecord={}&maximumRecords=50&page={}&collapsing=true&exactSearch=false&query=
            dc.source%20all%20%22Institut%20fran%C3%A7ais%20d%E2%80%99arch%C3%A9ologie%20orientale
            %22%20%20and%20%28provenance%20adj%20%22bnf.fr%22%29'''
}

NS = {'srw': "http://www.loc.gov/zing/srw/"}

def base_url_to_xml(base_url):
    '''Takes a url to a search results webpage from gallica and returns a url to
    the xml data of the objects displayed in that page'''
    url_for_xml_file = base_url.replace('https://gallica.bnf.fr/services/engine/search/sru?', \
    'https://gallica.bnf.fr/SRU?')

    return url_for_xml_file

def main():
    '''Reads in a dictionary of form 'file_name: base_url', passes base_url to get_urls,
    then iterates over the list of urls-one for each page of records–and writes the xml
    from each page to a file'''
    for key, value in BNF_DATA.items():
        page=1
        start_record=1
        logging.info('''\t%s - Starting harvest of %s.''', datetime.now().strftime\
        ("%Y:%m:%d %H:%M:%S"), key)

        req = requests.get(base_url_to_xml(value.format(start_record, page)), allow_redirects=False)
        tree = ElementTree.fromstring(req.content)
        records_available = int(tree.find('srw:numberOfRecords', NS).text)

        # Get number of records.
        logging.info('\t\t%s - Number of records: %i', datetime.now().\
        strftime("%Y:%m:%d %H:%M:%S"), records_available)

        Path("output/bnf/{}".format(key.lower())).mkdir(parents=True, exist_ok=True)
        if records_available % 50 > 0:
            iterations = (records_available / 50) + 1
        else:
            iterations = records_available / 50

        for i in range(int(iterations)):
            req = requests.get(base_url_to_xml(value.format(start_record, page)), \
            allow_redirects=False)
            tree = ElementTree.fromstring(req.content)
            # Get a list of records from the collection
            records = tree.find('srw:records', NS)
            for count, record in enumerate(records, start=start_record+1):
                byt = ElementTree.tostring(record)
                with open('output/bnf/{}/bnf-{}-{}.xml'.format(key.lower(), key.lower(), \
                count), 'wb') as out:
                    out.write(byt)
            page+=1
            start_record+=50

        # Check that the number of records harvested matches what the server says are available.
        try:
            assert len(glob.glob('output/bnf/{}/*.xml'.format(key.lower()))) == records_available
        except AssertionError as err:
            logging.exception('\t\tThe value in the %s numberOfRecords element was %i but %i' \
                              'records were harvested.', key, records_available, len(glob.glob\
                              ('output/bnf/{}/*.xml'.format(key.lower()))))
            raise err

if __name__ == "__main__":
    main()
