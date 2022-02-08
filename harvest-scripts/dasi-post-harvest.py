import glob
import urllib.request
from lxml import etree
from bs4 import BeautifulSoup

records = "/Users/jtim/Dropbox/DLSS/DLME/dlme-harvest/harvest-scripts/output/dasi/epi_set/data/*"
namespaces = {'dc': 'http://purl.org/dc/elements/1.1/'} # add more as needed

for count, r in enumerate(glob.glob(records), start=1):
    print(f'Working on {count} of {len(glob.glob(records))}: {r}')
    tree = etree.parse(r)
    root = tree.getroot()
    ids = tree.findall('//dc:identifier', namespaces)
    for i in ids:
        if i.text.startswith('http'):
            url = urllib.request.urlopen(f"http://dasi.cnr.it/index.php?id=79&prjId=1&corId=5&colId=0&navId=458870343&recId={i.text.split('recId=')[-1]}")
            if url.getcode() != 200:
                raise Exception(f"Failed because {url} unresolvable")
            soup = BeautifulSoup( url.read() , 'html.parser')
            thumb_div = soup.find( class_ = "thumbnail_med" )
            if thumb_div is None:
                pass
            else:
                thumb_url = thumb_div.find("img")['src']
                c = etree.Element("thumbnail")
                c.text = thumb_url
                root.insert(2, c)
                et = etree.ElementTree(root)
                et.write(f'{r}', pretty_print=True)
