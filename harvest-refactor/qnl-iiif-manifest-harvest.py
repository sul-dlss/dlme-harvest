from lxml import etree
import glob
import urllib.request

ns = {'oai': "http://www.openarchives.org/OAI/2.0/"}

files = glob.glob('/Users/jtim/Dropbox/DLSS/DLME/dlme-metadata/qnl/british-library/data/*.xml')

for file in files:
    file = open(file, 'r')
    tree = etree.ElementTree(file=file)
    print(tree)
    record_id = tree.find('/*/oai:identifier', ns).text.replace('_en', '')
    iiif_manifest_url = 'https://www.qdl.qa/en/iiif/{}/manifest'.format(record_id)
    urllib.request.urlretrieve(iiif_manifest_url, "qnl-iiif-manifests/{}".format(record_id))
