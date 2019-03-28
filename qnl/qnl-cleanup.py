import glob, os, pathlib, re
from copy import deepcopy
from lxml import etree

mods_ns = "http://www.loc.gov/mods/v3"
oai_ns = "http://www.openarchives.org/OAI/2.0/"

ar = {}
en = {}

# Helper functions
def to_str(bytes_or_str):
    '''Takes bytes or string and returns string'''
    if isinstance(bytes_or_str, bytes):
        value = bytes_or_str.decode('utf-8')
    else:
        value = bytes_or_str
    return value  # Instance of str

for file in glob.glob('/Users/jtim/Dropbox/DLSS/DLME/dlme-metadata/qnl/british-library/data/*.xml'):
     tree = etree.parse(file)
     id = tree.find("/*/".format(oai_ns, oai_ns)).text
     if '_en' in id:
         en[file] = id
     else:
         ar[file] = id


count = 1
for en_key, en_value in en.items():
    for ar_key, ar_value in ar.items():
        if re.sub('_en', '', en_value) == re.sub('_ar', '', ar_value):
    # if re.sub('_en', '', en_value) in re.sub('_ar', '', ar_value):
            en_root = etree.parse(en_key)
            ar_root = etree.parse(ar_key)
            pathlib.Path('combined').mkdir(parents=True, exist_ok=True)
            with open('combined/comb_{}.xml'.format(count), 'w') as out:
                for child in en_root.iter():
                    out.write(etree.tostring(child, encoding='unicode', pretty_print=True))
                    out.write("<ar>insert arabic</ar>")
                    # out.write(etree.tostring(ar_root.element, encoding='unicode', pretty_print=True))
                count += 1
