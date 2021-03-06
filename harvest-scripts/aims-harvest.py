#!/usr/bin/python
import os, requests
from io import BytesIO
from lxml import etree

def main():
    parser = etree.XMLParser(ns_clean=True, load_dtd=False)
    xml = requests.get('https://feed.podbean.com/themaghribpodcast/feed.xml').content
    tree = etree.parse(BytesIO(xml), parser)
    directory = "output/aims/data/"
    os.makedirs(os.path.dirname(directory), exist_ok=True)

    for counter, element in enumerate(tree.findall("//item"), start=1):
        with open("{}aims-{}.xml".format(directory, counter), "w") as out_file:
            out_file.write(etree.tostring(element, encoding='unicode', pretty_print=True))

if __name__ == "__main__":
    main()
