import glob, io, json, os, pathlib, re
from lxml import etree

mods_ns = "{http://www.loc.gov/mods/v3}"
oai_ns = "{http://www.openarchives.org/OAI/2.0/}"
metadata = oai_ns + "metadata/"

ar = {}
en = {}
matches = {}
non_matches = {}

# Helper functions
def to_str(bytes_or_str):
    '''Takes bytes or string and returns string'''
    if isinstance(bytes_or_str, bytes):
        value = bytes_or_str.decode('utf-8')
    else:
        value = bytes_or_str
    return value  # Instance of str

# Remove QDL files, add British Library files to either Arabic or English dictionary
for file in glob.glob('/Users/jtim/Dropbox/DLSS/DLME/dlme-metadata/qnl/data/*.xml'):
     tree = etree.parse(file)
     id = tree.find(oai_ns + "header/" + oai_ns + "identifier").text
     if 'qnlhc' in id:
         os.remove(file)
         print("File Removed: {}".format(file))
     elif '_en' in id:
         en[re.sub('_en', '', id)] = file
     else:
         ar[re.sub('_ar', '', id)] = file

# Check length of Arabic and English dictionaries
print("There are {} Arabic records and {} English records.".format(len(ar), len(en)))

# Convert Arabic and English dictionaries to sets to use intersection
set_ar = set(ar)
set_en = set(en)

# Add records without conterpart in the other language to non_matches dictionary
for en_key, en_value in en.items():
    if en_key not in ar.keys():
        non_matches[en_key] = en_value

# Print non matches found and write, if any, to outfile
print("There are {} records without matches".format(len(non_matches)))
if len(non_matches) > 0:
    out_non_matches = 'output/non_matches.json'
    os.makedirs(os.path.dirname(out_non_matches), exist_ok=True)
    with io.open(out_non_matches, 'w') as out_file:
        json.dump(non_matches, out_file, ensure_ascii=False)

# Add English records and Arabic Equivalent to matches dicationary
for file_id in set_ar.intersection(set_en):
    matches[ar[file_id]] = en[file_id]

# Print matches found and write, if any, to outfile
if len(matches) > 0:
    out_matches = 'output/matches.json'
    os.makedirs(os.path.dirname(out_matches), exist_ok=True)
    with io.open(out_matches, 'w') as out_file:
        json.dump(matches, out_file, ensure_ascii=False)

# data = 'output/data/'
# os.makedirs(os.path.dirname(data), exist_ok=True)

for count, (key, value) in enumerate(matches.items(), start=1):
    ar_tree = etree.parse(key)
    en_tree = etree.parse(value)
    dlme_id = re.sub('_ar', '_dlme', ar_tree.find(oai_ns + "header/" + oai_ns + "identifier").text)
    ar_metadata = ar_tree.find(metadata)
    en_metadata = en_tree.find(metadata)

    combined_record = 'output/data/qnl-combined-{}.xml'.format(count)
    os.makedirs(os.path.dirname(combined_record), exist_ok=True)
    with io.open(combined_record, 'w') as out_file:
        # Write record tag
        out_file.write('<record xmlns="http://www.openarchives.org/OAI/2.0/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">\n')
        # Write header
        out_file.write('\t<header>\n')
        out_file.write('\t\t<identifier>')
        out_file.write(dlme_id)
        out_file.write('</identifier>\n')
        out_file.write('\t</header>\n')
        # Write Arabic metadata
        out_file.write('\t<ar_metadata>\n')
        out_file.write(to_str(etree.tostring(ar_metadata)))
        out_file.write('\t</ar_metadata>\n')
        # Write Englih metadata
        out_file.write('\t<en_metadata>\n')
        out_file.write(to_str(etree.tostring(en_metadata)))
        out_file.write('\t</en_metadata>\n')
        # Write record closing tag
        out_file.write('</record>\n')









        # en_tree = etree.parse(en_key)
        # with open('combined/comb_{}.xml'.format(count), 'w') as out:
        #     out_file.write(etree.tostring(en_tree, encoding='unicode', pretty_print=True))
        #     count += 1

# for ar_key, ar_value in ar.items():
#     if ar_value not in en.values():
#         ar_tree = etree.parse(ar_key)
#         with open('combined/comb_{}.xml'.format(count), 'w') as out:
#             out_file.write(etree.tostring(ar_tree, encoding='unicode', pretty_print=True))
#             count += 1

# for en_key, en_value in en.items():
#     for ar_key, ar_value in ar.items():
#         if en_value == ar_value:
#             en_tree = etree.parse(en_key)
#             ar_tree = etree.parse(ar_key)
#             with open('combined/comb_{}.xml'.format(count), 'w') as out:
#                 en_id = en_tree.find(oai_ns + "header/" + oai_ns + "identifier").text
#                 ar_id = ar_tree.find(oai_ns + "header/" + oai_ns + "identifier").text
#                 en_datestamp = en_tree.find(oai_ns + "header/" + oai_ns + "datestamp").text
#                 ar_datestamp = ar_tree.find(oai_ns + "header/" + oai_ns + "datestamp").text
#                 shelfLocator = en_tree.find(metadata + "location/" + mods_ns + "shelfLocator").text
#                 url = en_tree.find(metadata + "location/" + mods_ns + "url").text
#                 en_physicalLocation = en_tree.find(metadata + "location/" + mods_ns + "physicalLocation").text
#                 ar_physicalLocation = ar_tree.find(metadata + "location/" + mods_ns + "physicalLocation").text
#                 record_identifer = en_tree.find(metadata + "recordInfo/" + mods_ns + "recordIdentifer").text
#                 en_title = en_tree.find(metadata + "titleInfo/" + mods_ns + "title").text
#                 ar_title = ar_tree.find(metadata + "titleInfo/" + mods_ns + "title").text
#                 date_issued = en_tree.find(metadata + "originInfo/" + mods_ns + "dateIssued").text
#                 date_captured = en_tree.find(metadata + "originInfo/" + mods_ns + "dateCaptured").text
#                 language_term = en_tree.find(metadata + "language/" + mods_ns + "languageTerm").text
#                 en_extent = en_tree.findall(metadata + "physicalDescription/" + mods_ns + "extent")
#                 ar_extent = ar_tree.findall(metadata + "physicalDescription/" + mods_ns + "extent")
#                 en_abstract = en_tree.find(metadata + "abstract")
#                 ar_abstract = ar_tree.find(metadata + "abstract")
#                 type_of_resource = en_tree.find(metadata + "typeOfResource")
#                 access_condition_url = en_tree.find(metadata + "accessCondition/" + mods_ns + "url").text
#
#                 # Write elements to combined file
#                 out_file.write('<record xmlns="http://www.openarchives.org/OAI/2.0/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">\n')
#
#                 # Write header content
#                 out_file.write('\t<header>\n')
#
#                 out_file.write('\t\t<identifier>')
#                 out_file.write(en_id)
#                 out_file.write('</identifier>\n')
#
#                 out_file.write('\t\t<identifier>')
#                 out_file.write(ar_id)
#                 out_file.write('</identifier>\n')
#
#                 out_file.write('\t\t<datestamp>')
#                 out_file.write(en_datestamp)
#                 out_file.write('</datestamp>\n')
#
#                 out_file.write('\t\t<datestamp>')
#                 out_file.write(ar_datestamp)
#                 out_file.write('</datestamp>\n')
#
#                 out_file.write('\t</header>\n')
#
#                 # Write metedata content
#                 out_file.write('\t<metadata>\n')
#                 out_file.write('\t\t<mods xmlns="http://www.loc.gov/mods/v3">\n')
#
#                 out_file.write('\t\t\t<identifier>')
#                 out_file.write(en_id)
#                 out_file.write('</identifier>\n')
#
#                 out_file.write('\t\t\t<identifier>')
#                 out_file.write(ar_id)
#                 out_file.write('</identifier>\n')
#
#                 out_file.write('\t\t\t<location>\n')
#
#                 out_file.write('\t\t\t\t<shelfLocator>')
#                 out_file.write(shelfLocator)
#                 out_file.write('</shelfLocator>\n')
#
#                 out_file.write('\t\t\t\t<url>')
#                 out_file.write(url)
#                 out_file.write('</url>\n')
#
#                 out_file.write('\t\t\t\t<physicalLocation>')
#                 out_file.write(en_physicalLocation)
#                 out_file.write('</physicalLocation>\n')
#
#                 out_file.write('\t\t\t\t<physicalLocation>')
#                 out_file.write(ar_physicalLocation)
#                 out_file.write('</physicalLocation>\n')
#
#                 out_file.write('\t\t\t</location>\n')
#
#                 out_file.write('\t\t\t<recordInfo>\n')
#                 out_file.write('\t\t\t\t<recordIdentifier>')
#                 out_file.write(record_identifer)
#                 out_file.write('</recordIdentifier>\n')
#                 out_file.write('\t\t\t</recordInfo>\n')
#
#                 out_file.write('\t\t\t<titleInfo>\n')
#                 out_file.write('\t\t\t\t<title>')
#                 out_file.write(en_title)
#                 out_file.write('</title>\n')
#                 out_file.write('\t\t\t\t<title>')
#                 out_file.write(ar_title)
#                 out_file.write('</title>\n')
#                 out_file.write('\t\t\t</titleInfo>\n')
#
#                 out_file.write('\t\t\t<originInfo>\n')
#                 out_file.write('\t\t\t\t<dateIssued>')
#                 out_file.write(date_issued)
#                 out_file.write('</dateIssued>\n')
#                 out_file.write('\t\t\t\t<dateCaptured>')
#                 out_file.write(date_captured)
#                 out_file.write('</dateCaptured>\n')
#                 out_file.write('\t\t\t</originInfo>\n')
#
#                 out_file.write('\t\t\t<language>\n')
#                 out_file.write('\t\t\t\t<languageTerm authority="iso639-2b">')
#                 out_file.write(language_term)
#                 out_file.write('</languageTerm>\n')
#                 out_file.write('\t\t\t</language>\n')
#
#                 out_file.write('\t\t\t<physicalDescription>\n')
#                 for i in en_extent:
#                     out_file.write('\t\t\t\t<extent>')
#                     out_file.write(i.text)
#                     out_file.write('</extent>\n')
#                 for i in ar_extent:
#                     out_file.write('\t\t\t\t<extent>')
#                     out_file.write(i.text)
#                     out_file.write('</extent>\n')
#                 out_file.write('\t\t\t</physicalDescription>\n')
#
#                 if en_abstract is not None:
#                     out_file.write('\t\t\t<abstract>')
#                     out_file.write(en_abstract.text)
#                     out_file.write('</abstract>\n')
#
#                 if ar_abstract is not None:
#                     out_file.write('\t\t\t<abstract>')
#                     out_file.write(ar_abstract.text)
#                     out_file.write('</abstract>\n')
#
#                 if type_of_resource is not None:
#                     out_file.write('\t\t\t<typeOfResource>')
#                     out_file.write(type_of_resource.text)
#                     out_file.write('</typeOfResource>\n')
#
#                 out_file.write('\t\t\t<accessCondition type="Use and reproduction">\n')
#                 out_file.write('\t\t\t\t<url>')
#                 out_file.write(access_condition_url)
#                 out_file.write('</url>\n')
#                 out_file.write('\t\t\t</accessCondition>\n')
#
#                 out_file.write('\t\t</mods>\n')
#                 out_file.write('\t</metadata>\n')
#                 out_file.write('</record>\n')
#                 count += 1
