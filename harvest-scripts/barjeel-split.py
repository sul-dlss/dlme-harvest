import io, os, pathlib, re, sys
from lxml import etree

tree = etree.parse('barjeel-raw-data.xml')
records = tree.findall('//item')

os.makedirs(os.path.dirname('output/barjeel/data/'), exist_ok=True)
for count, record in enumerate(records, start=1):
    et = etree.ElementTree(record)
    with io.open('output/barjeel/data/barjeel-{}.xml'.format(count), 'wb') as out_file:
        et.write(out_file, xml_declaration=True, encoding="utf-8")
