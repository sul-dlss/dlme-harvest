#!/usr/bin/python
import csv, math
from argparse import ArgumentParser
from random import sample

fields = ['cho_alternative',
          'cho_contributor',
          'cho_creator',
          'cho_date ',
          'cho_dc_rights',
          'cho_description',
          'cho_edm_type',
          'cho_extent',
          'cho_format',
          'cho_has_part',
          'cho_has_type',
          'cho_identifier',
          'cho_is_part_of',
          'cho_language',
          'cho_medium',
          'cho_provenance',
          'cho_publisher',
          'cho_relation',
          'cho_same_as',
          'cho_source',
          'cho_spatial',
          'cho_subject',
          'cho_temporal',
          'cho_title',
          'cho_type']

extract_macros = {'cambridge_dimensions': {'from_field': '/tei:extent/tei:dimensions',
                                           'transforms': 'Extracts height and width into formated string.'},
                  'extract_aub_description': {'from_field': '/dc:description',
                                              'transforms': 'Ignores url values in the description field.'},
                  'generate_edm_type': {'from_field': '.Classification or .ObjectName',
                                        'transforms': "Seperate values on ';', then downcase"},
                  'json_title_plus':{'from_field': '.title and one other field',
                                        'transforms': 'The title field was merged with the truncated value from the second field.'},
                  'princeton_title_and_lang': {'from_field': '.title',
                                               'transforms': 'The script of the title was programatically determined.'},
                  'scw_has_type': {'from_field': '/*/mods:genre or /*/mods:typeOfResource or /*/mods:subject/mods:topic or /*/mods:extension/cdwalite:indexingMaterialsTechSet/'\
                                              'cdwalite:termMaterialsTech',
                                   'transforms': 'The output value was mapped to a value in a DLME controlled vocabulary.'},
                  'xpath_title_or_desc': {'from_field': '/dc:title or /dc:description[3]',
                                          'transforms': 'If no title found in /dc:title, map in truncated description.'},
                  'xpath_title_plus': {'from_field': 'the title field and a second field such as id or description',
                                       'transforms': 'The title field was merged with the truncated value from the second field.'}}

modify_macros = {'prepend': 'A literal value was prepended to provide context or to satisfy a consistent pattern requirement.',
                 'translation_map': 'The output value was mapped to a value in a DLME controlled vocabulary.'}

# use config file and yaml to write metadata crosswalk
def main():
    # print('DLME metadata crosswalk\n')
    # print('-' * 70 + '\n')
    # print("Incoming field ----------------------------------- DLME field --------------- Transforms")
    with open(args.file[0]) as f:
        lines = f.readlines()
        with open('/Users/jtim/Dropbox/DLSS/DLME/dlme-harvest/analysis-scripts/output/{}'.format(args.file[0].split('/')[-1].replace('_config.rb', '_crosswalk.csv')), mode='w') as out:
            out = csv.writer(out, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            out.writerow(["Incoming Field", "", "DLME Field", "", "Transformations"])

            for line in lines:
                for field in fields:
                    if 'to_field' in line:
                        if field in line:
                            to_field = line.split(',')[0].strip('to_field ')
                            transforms = []
                            from_field = None
                            for k,v in extract_macros.items():
                                if k in line:
                                    from_field = extract_macros.get(k).get('from_field')
                                    transforms.append(extract_macros.get(k).get('transforms'))
                            # if no keys found in extract_macros
                            if from_field == None:
                                if 'literal(' in line:
                                    from_field = "Assigned literal value: '{}'".format(line.split('literal(')[-1].split('),')[0])
                                else:
                                    from_field = line.split('(')[1].split(')')[0].strip("'")
                            for k,v in modify_macros.items():
                                if k in line:
                                    transforms.append(modify_macros.get(k))

                            out.writerow([from_field, ">>", to_field, "~", ' '.join(transforms)])

                            # print("{}{}>>    {}{}~ {}".format(from_field, ' '*(45-(len(from_field))), to_field, ' '*(25-(len(to_field))), ' '.join(transforms)))

########## Main Loop ##########

if __name__ == '__main__':
    # CLI client options.
    parser = ArgumentParser()
    parser.add_argument(
        'file',
        nargs='+',
        help='Which config file do you want to parse?')
    args = parser.parse_args()
    main()
