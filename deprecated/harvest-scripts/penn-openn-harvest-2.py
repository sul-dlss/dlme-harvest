#!/usr/bin/python
import urllib.request, os, io, time
from io import StringIO, BytesIO
from lxml import etree

muslim_manuscripts_collection_url = "https://openn.library.upenn.edu/html/muslimworld_contents.html"
genizah_collection_url = "https://openn.library.upenn.edu/html/genizah_contents.html"

muslim_manuscripts_tei_urls = []
genizah_tei_urls = []

def main():
    # Get html
    genizah_collection_collection_html = urllib.request.urlopen(genizah_collection_url).read()
    muslim_manuscripts_collection_html = urllib.request.urlopen(muslim_manuscripts_collection_url).read()

    # Parse html
    parser = etree.HTMLParser()
    genizah_tree = etree.parse(BytesIO(genizah_collection_collection_html), parser)
    muslim_manuscripts_tree = etree.parse(BytesIO(muslim_manuscripts_collection_html), parser)

    # Get all record urls and append urls to TEI records to genizah_tei_urls
    # genizah_urls = genizah_tree.xpath('//ul[@class="ul_documents"]/li/span[@class="page-link"]/a')
    # for i in genizah_urls:
    #     if 'TEI' in i.attrib['href']:
    #         genizah_tei_urls.append(i.attrib['href'])
    #
    # for count, i in enumerate(genizah_tei_urls, start=1):
    #     document = urllib.request.urlopen("http://openn.library.upenn.edu/{}".format(i)).read()
    #     root = etree.parse(BytesIO(document), parser)
    #     html = root.find("./")
    #     url = etree.SubElement(html, "dlme_url").text = i
    #     obj_xml = etree.tostring(root, pretty_print=True, xml_declaration=True)
    #
    #     directory = "output/penn/openn/{}/data/".format(i.split('/')[2])
    #     os.makedirs(os.path.dirname(directory), exist_ok=True)
    #     with open("{}{}-{}.xml".format(directory, i.split('/')[2], count), 'wb') as out_file:
    #         out_file.write(obj_xml)
    #     time.sleep(5)

    # Get all record urls and append urls to TEI records to muslim_manuscripts_tei_urls
    muslim_manuscripts_urls = muslim_manuscripts_tree.xpath('//ul[@class="ul_documents"]/li/span[@class="page-link"]/a')
    for i in muslim_manuscripts_urls:
        if 'TEI' in i.attrib['href']:
            muslim_manuscripts_tei_urls.append(i.attrib['href'])

    for count, i in enumerate(muslim_manuscripts_tei_urls, start=1):
        document = urllib.request.urlopen("http://openn.library.upenn.edu/{}".format(i)).read()
        root = etree.parse(BytesIO(document), parser)
        html = root.find("./")
        url = etree.SubElement(html, "dlme_url").text = i
        obj_xml = etree.tostring(root, pretty_print=True, xml_declaration=True)

        directory = "output/penn/openn/mmw-{}/data/".format(i.split('/')[2])
        os.makedirs(os.path.dirname(directory), exist_ok=True)
        with open("{}mmw-{}-{}.xml".format(directory, i.split('/')[2], count), 'wb') as out_file:
            out_file.write(obj_xml)
        time.sleep(5) # the network seems to be throttling large downloads

if __name__ == "__main__":
    main()
