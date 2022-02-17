import io, os, pathlib, re, sys
from lxml import etree

ino = "{http://namespaces.softwareag.com/tamino/response2}"

tree = etree.parse('generaliPaola.xml')
records = tree.findall(ino + 'object/')

os.makedirs(os.path.dirname('output/vatican/data/'), exist_ok=True)
for count, record in enumerate(records, start=1):
    et = etree.ElementTree(record)
    with io.open('output/vatican/data/vatican-{}.xml'.format(count), 'wb') as out_file:
        et.write(out_file, xml_declaration=True, encoding="utf-8")
