from lxml import etree

tree = etree.parse('/Users/jtim/Dropbox/DLSS/DLME/dlme-metadata/aims/data/aims.xml')

count = 1

for element in tree.findall("//item"):
    print("this is: {}".format(element))
    with open("output/aims/aims-{}.xml".format(count), 'w') as out_file:
        out_file.write(etree.tostring(element, encoding='unicode', pretty_print=True))
    count += 1
