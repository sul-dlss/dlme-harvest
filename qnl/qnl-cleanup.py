import glob, os, pathlib, re
from lxml import etree

mods_ns = "{http://www.loc.gov/mods/v3}"
oai_ns = "{http://www.openarchives.org/OAI/2.0/}"
metadata = oai_ns + "metadata/" + mods_ns + "mods/" + mods_ns

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
     id = tree.find(oai_ns + "header/" + oai_ns + "identifier").text
     if 'qnlhc' in id:
         os.remove(file)
         print("File Removed!")
     elif '_en' in id:
         en[file] = re.sub('_en', '', id)
     else:
         ar[file] = re.sub('_ar', '', id)

count = 1
pathlib.Path('combined').mkdir(parents=True, exist_ok=True)

for en_key, en_value in en.items():
    if en_value not in ar.values():
        en_tree = etree.parse(en_key)
        with open('combined/comb_{}.xml'.format(count), 'w') as out:
            out.write(etree.tostring(en_tree, encoding='unicode', pretty_print=True))
            count += 1

for ar_key, ar_value in ar.items():
    if ar_value not in en.values():
        ar_tree = etree.parse(ar_key)
        with open('combined/comb_{}.xml'.format(count), 'w') as out:
            out.write(etree.tostring(ar_tree, encoding='unicode', pretty_print=True))
            count += 1

for en_key, en_value in en.items():
    for ar_key, ar_value in ar.items():
        if en_value == ar_value:
            en_tree = etree.parse(en_key)
            ar_tree = etree.parse(ar_key)
            with open('combined/comb_{}.xml'.format(count), 'w') as out:
                en_id = en_tree.find(oai_ns + "header/" + oai_ns + "identifier").text
                ar_id = ar_tree.find(oai_ns + "header/" + oai_ns + "identifier").text
                en_datestamp = en_tree.find(oai_ns + "header/" + oai_ns + "datestamp").text
                ar_datestamp = ar_tree.find(oai_ns + "header/" + oai_ns + "datestamp").text
                shelfLocator = en_tree.find(metadata + "location/" + mods_ns + "shelfLocator").text
                url = en_tree.find(metadata + "location/" + mods_ns + "url").text
                en_physicalLocation = en_tree.find(metadata + "location/" + mods_ns + "physicalLocation").text
                ar_physicalLocation = ar_tree.find(metadata + "location/" + mods_ns + "physicalLocation").text
                record_identifer = en_tree.find(metadata + "recordInfo/" + mods_ns + "recordIdentifer").text
                en_title = en_tree.find(metadata + "titleInfo/" + mods_ns + "title").text
                ar_title = ar_tree.find(metadata + "titleInfo/" + mods_ns + "title").text
                date_issued = en_tree.find(metadata + "originInfo/" + mods_ns + "dateIssued").text
                date_captured = en_tree.find(metadata + "originInfo/" + mods_ns + "dateCaptured").text
                language_term = en_tree.find(metadata + "language/" + mods_ns + "languageTerm").text
                en_extent = en_tree.findall(metadata + "physicalDescription/" + mods_ns + "extent")
                ar_extent = ar_tree.findall(metadata + "physicalDescription/" + mods_ns + "extent")
                en_abstract = en_tree.find(metadata + "abstract")
                ar_abstract = ar_tree.find(metadata + "abstract")
                type_of_resource = en_tree.find(metadata + "typeOfResource")
                access_condition_url = en_tree.find(metadata + "accessCondition/" + mods_ns + "url").text

                # Write elements to combined file
                out.write('<record xmlns="http://www.openarchives.org/OAI/2.0/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">\n')

                # Write header content
                out.write('\t<header>\n')

                out.write('\t\t<identifier>')
                out.write(en_id)
                out.write('</identifier>\n')

                out.write('\t\t<identifier>')
                out.write(ar_id)
                out.write('</identifier>\n')

                out.write('\t\t<datestamp>')
                out.write(en_datestamp)
                out.write('</datestamp>\n')

                out.write('\t\t<datestamp>')
                out.write(ar_datestamp)
                out.write('</datestamp>\n')

                out.write('\t</header>\n')

                # Write metedata content
                out.write('\t<metadata>\n')
                out.write('\t\t<mods xmlns="http://www.loc.gov/mods/v3">\n')

                out.write('\t\t\t<identifier>')
                out.write(en_id)
                out.write('</identifier>\n')

                out.write('\t\t\t<identifier>')
                out.write(ar_id)
                out.write('</identifier>\n')

                out.write('\t\t\t<location>\n')

                out.write('\t\t\t\t<shelfLocator>')
                out.write(shelfLocator)
                out.write('</shelfLocator>\n')

                out.write('\t\t\t\t<url>')
                out.write(url)
                out.write('</url>\n')

                out.write('\t\t\t\t<physicalLocation>')
                out.write(en_physicalLocation)
                out.write('</physicalLocation>\n')

                out.write('\t\t\t\t<physicalLocation>')
                out.write(ar_physicalLocation)
                out.write('</physicalLocation>\n')

                out.write('\t\t\t</location>\n')

                out.write('\t\t\t<recordInfo>\n')
                out.write('\t\t\t\t<recordIdentifier>')
                out.write(record_identifer)
                out.write('</recordIdentifier>\n')
                out.write('\t\t\t</recordInfo>\n')

                out.write('\t\t\t<titleInfo>\n')
                out.write('\t\t\t\t<title>')
                out.write(en_title)
                out.write('</title>\n')
                out.write('\t\t\t\t<title>')
                out.write(ar_title)
                out.write('</title>\n')
                out.write('\t\t\t</titleInfo>\n')

                out.write('\t\t\t<originInfo>\n')
                out.write('\t\t\t\t<dateIssued>')
                out.write(date_issued)
                out.write('</dateIssued>\n')
                out.write('\t\t\t\t<dateCaptured>')
                out.write(date_captured)
                out.write('</dateCaptured>\n')
                out.write('\t\t\t</originInfo>\n')

                out.write('\t\t\t<language>\n')
                out.write('\t\t\t\t<languageTerm authority="iso639-2b">')
                out.write(language_term)
                out.write('</languageTerm>\n')
                out.write('\t\t\t</language>\n')

                out.write('\t\t\t<physicalDescription>\n')
                for i in en_extent:
                    out.write('\t\t\t\t<extent>')
                    out.write(i.text)
                    out.write('</extent>\n')
                for i in ar_extent:
                    out.write('\t\t\t\t<extent>')
                    out.write(i.text)
                    out.write('</extent>\n')
                out.write('\t\t\t</physicalDescription>\n')

                if en_abstract is not None:
                    out.write('\t\t\t<abstract>')
                    out.write(en_abstract.text)
                    out.write('</abstract>\n')

                if ar_abstract is not None:
                    out.write('\t\t\t<abstract>')
                    out.write(ar_abstract.text)
                    out.write('</abstract>\n')

                if type_of_resource is not None:
                    out.write('\t\t\t<typeOfResource>')
                    out.write(type_of_resource.text)
                    out.write('</typeOfResource>\n')

                out.write('\t\t\t<accessCondition type="Use and reproduction">\n')
                out.write('\t\t\t\t<url>')
                out.write(access_condition_url)
                out.write('</url>\n')
                out.write('\t\t\t</accessCondition>\n')

                out.write('\t\t</mods>\n')
                out.write('\t</metadata>\n')
                out.write('</record>\n')
                count += 1
