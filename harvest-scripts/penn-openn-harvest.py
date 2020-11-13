#!/usr/bin/python
import urllib.request, os, io
from lxml import etree, objectify

# Dictionary with keys for collection ids and lists of record ids
records = {'0001': ['ljs189', 'ljs196', 'ljs235', 'ljs286', 'ljs293', 'ljs294', 'ljs295',
                  'ljs296', 'ljs299', 'ljs311', 'ljs312', 'ljs322', 'ljs37', 'ljs38',
                  'ljs387', 'ljs388', 'ljs398', 'ljs399', 'ljs40', 'ljs400', 'ljs403',
                  'ljs404', 'ljs405', 'ljs407', 'ljs408', 'ljs409', 'ljs410', 'ljs412',
                  'ljs414', 'ljs417', 'ljs425', 'ljs426', 'ljs427', 'ljs434', 'ljs435',
                  'ljs436', 'ljs441', 'ljs444', 'ljs447', 'ljs45', 'ljs455', 'ljs456',
                  'ljs459', 'ljs460', 'ljs464', 'ljs467', 'ljs469', 'ljs486', 'ljs489',
                  'ljs49', 'ljs495', 'ljs_422'],
       '0002': ['misc_mss_box24_fldr3', 'misc_mss_box24_fldr4', 'mscodex1743', 'mscodex1892',
                'mscodex1893', 'mscodex1894', 'mscodex1895', 'mscodex1896', 'mscodex1897',
                'mscodex1898', 'mscodex1899', 'mscodex1900', 'mscodex1901', 'mscodex1902',
                'mscodex1903', 'mscodex1904', 'mscodex1907', 'mscodex1909', 'mscodex1910',
                'mscodex1911', 'mscodex1912', 'mscodex1913', 'mscodex1914', 'mscodex1915',
                'mscodex1916', 'mscodex1917', 'mscodex1918', 'mscodex1951', 'mscodex1952',
                'mscodex1958', 'mscodex1959', 'mscodex1961', 'mscodex1962', 'mscodex1963',
                'mscodex1964', 'mscodex23', 'mscodex24', 'mscodex40', 'mscodex41', 'mscodex42',
                'mscodex43', 'mscodex44', 'msroll1906', 'msroll1965'],
       '0023': ['lewis_o_002', 'lewis_o_003', 'lewis_o_005', 'lewis_o_007', 'lewis_o_008',
                'lewis_o_009', 'lewis_o_010', 'lewis_o_011', 'lewis_o_012', 'lewis_o_015',
                'lewis_o_016', 'lewis_o_017', 'lewis_o_018', 'lewis_o_019', 'lewis_o_020',
                'lewis_o_021', 'lewis_o_023', 'lewis_o_024', 'lewis_o_025', 'lewis_o_026',
                'lewis_o_027', 'lewis_o_028', 'lewis_o_029', 'lewis_o_030', 'lewis_o_031',
                'lewis_o_033', 'lewis_o_037', 'lewis_o_040', 'lewis_o_051', 'lewis_o_056',
                'lewis_o_058', 'lewis_o_061', 'lewis_o_072', 'lewis_o_085', 'lewis_o_088',
                'lewis_o_093', 'lewis_o_100'],
       '0031': ['2017_232_1'],
       '0032': ['ms_or_015', 'ms_or_019', 'ms_or_024', 'ms_or_025', 'ms_or_032', 'ms_or_044',
                'ms_or_046', 'ms_or_016', 'ms_or_021', 'ms_or_030', 'ms_or_033', 'ms_or_036',
                'ms_or_037', 'ms_or_038', 'ms_or_039', 'ms_or_041', 'ms_or_043', 'ms_or_047',
                'ms_or_048', 'ms_or_052', 'ms_or_054', 'ms_or_058', 'ms_or_060', 'ms_or_049',
                'ms_or_064', 'ms_or_066', 'ms_or_072', 'ms_or_069', 'ms_or_083', 'ms_or_091',
                'ms_or_094', 'ms_or_095', 'ms_or_096', 'ms_or_098', 'ms_or_083a', 'ms_or_099',
                'ms_or_100',  'ms_or_101', 'ms_or_103', 'ms_or_102', 'ms_or_104', 'ms_or_105',
                'ms_or_106', 'ms_or_107', 'ms_or_108', 'ms_or_109', 'ms_or_110', 'ms_or_111',
                'ms_or_112', 'ms_or_113', 'ms_or_114', 'ms_or_115', 'ms_or_118', 'ms_or_117',
                'ms_or_120', 'ms_or_122', 'ms_or_123', 'ms_or_131', 'ms_or_132', 'ms_or_137',
                'ms_or_138', 'ms_or_140', 'ms_or_141', 'ms_or_146a', 'ms_or_152a', 'ms_or_150',
                'ms_or_152b', 'ms_or_152c', 'ms_or_146', 'ms_or_173', 'ms_or_169', 'ms_or_178',
                'ms_or_179', 'ms_or_186', 'ms_or_203', 'ms_or_206', 'ms_or_209', 'ms_or_217',
                'ms_or_190', 'ms_or_222', 'ms_or_229', 'ms_or_230', 'ms_or_234', 'ms_or_237',
                'ms_or_238', 'ms_or_239', 'ms_or_240', 'ms_or_242', 'ms_or_256', 'ms_or_248',
                'ms_or_257', 'ms_or_258', 'ms_or_260', 'ms_or_261', 'ms_or_269', 'ms_or_278',
                'ms_or_287', 'ms_or_290', 'ms_or_292', 'ms_or_294', 'ms_or_305', 'ms_or_298',
                'ms_or_310', 'ms_or_311', 'ms_or_355', 'ms_or_276', 'ms_or_147', 'ms_or_148',
                'ms_or_272', 'ms_or_319', 'ms_or_327', 'ms_or_329', 'ms_or_325', 'ms_or_318',
                'ms_or_307', 'ms_or_285', 'ms_or_330', 'ms_or_306', 'ms_or_321', 'ms_or_344',
                'ms_or_254', 'ms_or_366', 'ms_or_365', 'ms_or_359', 'ms_or_357', 'ms_or_369',
                'ms_or_372']
        }

def main():

    for key, value in records.items():
        for count, i in enumerate(value, start=1):
            url = "http://openn.library.upenn.edu/Data/{}/{}/data/{}_TEI.xml".format(key, i, i)
            print("Fetching {}".format(url))
            document = urllib.request.urlopen(url).read()
            root = objectify.fromstring(document)
            ms_identifier = root.teiHeader.fileDesc.sourceDesc.msDesc.msIdentifier
            # root.insert("teiHeader/fileDesc/sourceDesc/msDesc/msIdentifier", etree.Element("child0"))
            alt_id = etree.SubElement(ms_identifier, "altIdentifier", type="openn-url")
            alt_id.idno = "http://openn.library.upenn.edu/Data/{}/html/{}.html".format(key, i)

            obj_xml = etree.tostring(root, pretty_print=True, xml_declaration=True)

            directory = "output/penn/openn/{}/data/".format(key)
            os.makedirs(os.path.dirname(directory), exist_ok=True)
            with open("{}{}-{}.xml".format(directory, key, count), 'wb') as out_file:
                out_file.write(obj_xml)

if __name__ == "__main__":
    main()
