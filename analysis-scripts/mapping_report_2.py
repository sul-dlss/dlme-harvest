#!/usr/bin/python
import dominate
from dominate.tags import *
import io
import json
from argparse import ArgumentParser
from collections import Counter, defaultdict
from datetime import date
from PIL import Image
import requests
import validators

# Constants for crosswalk
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

def thumbnail_report(image_sizes_list):
    '''Takes a list of tuples as input and outputs a thumbnail image size report.'''
    passed_rec = 0
    failed_rec = 0
    REC_SIZE = 400

    for i in image_sizes_list:
        if i[0] >= REC_SIZE or i[1] >= REC_SIZE:
            passed_rec+=1
        else:
            failed_rec+=1

    # return f'{round((passed_rec/len(image_sizes_list))*100)}% of the {len(image_sizes_list)} thumbnail images sampled had a width or height of {REC_SIZE} or greater.'
    return "filler"

def image_size(response):
    '''Takes an http response and returns an image size.'''
    if not isinstance(response, requests.models.Response):
        raise TypeError('The parameter passed to the image_size function is not an http response.')
    # print(Image.open(response.raw))
    # size = Image.open(response.raw).size
    # dataBytesIO = io.BytesIO(Image.open(response))
    # size = Image.open(dataBytesIO).size
    return (300, 265) # should return size

# validate urls
def validate_url(url):
    '''Checks if url has valid form.'''
    if not validators.url(url):
        raise f"Invalid url for {record['id']}: {url}"

# resolve urls
def resolve_url(response):
    '''Checks if url is resolvable.'''
    try:
        if response.status_code==200:
            return True
    except AttributeError:
        print('The value passed to resolve_url was not a valid url.')

# Define variables for capturing data from main
thumbnail_image_sizes = []
unresolvable_resources = []
unresolvable_thumbnails = []

def main():
    '''Captures all field value counts in counter object and writes report to html file.'''
    DATE_ARRAY_FIELDS = ['cho_date_range_hijri', 'cho_date_range_norm']
    IGNORE_FIELDS = ['agg_data_provider', 'agg_data_provider_collection', 'agg_data_provider_country',
                     'agg_provider', 'agg_provider_country', 'cho_type_facet', 'dlme_collection',
                     'dlme_source_file', 'id', 'transform_version', 'transform_timestamp']

    IGNORE_VALUES = ['wr_dc_rights', 'wr_edm_rights', 'wr_is_referenced_by', 'fields_covered']

    record_count = 0
    # merge all records into single counter object and write field report
    counts = defaultdict(Counter)
    # for storing resource information during iteration
    unresolvable_resources = []
    unresolvable_thumbnails = []
    humbnail_image_sizes = []

    with open(args.input, 'r') as file:
        records = file.readlines()
        provider = json.loads(records[0])['agg_data_provider']['en'][0]
        collection = json.loads(records[0])['dlme_collection']['en'][0]
        record_count = len(records)

        # get counts for fields, values, languages
        for count, record in enumerate(records, start=1):
            record = json.loads(record)
            for field, metadata in record.items():
                if field not in IGNORE_FIELDS:
                    counts[field].update({'fields_covered' : 1})
                    if isinstance(metadata, dict):
                        for key, values in metadata.items():
                            if isinstance(values, list):
                                counts[field].update({key : len(values)})
                            else:
                                counts[field].update({key : 1})
                    elif field in DATE_ARRAY_FIELDS:
                        counts[field].update({'values' : 1})
                    else:
                        counts[field].update({'values' : len(metadata)})

            # Resolve resource url
            # validate_url(record['agg_is_shown_at']['wr_id']) # will fail if invalid url
            # try:
            #     resource = requests.get(record['agg_is_shown_at']['wr_id'], stream=True)
            #     if not resolve_url(resource):
            #         unresolvable_resources.append(f"Identifier {record['id']} from DLME file {record['dlme_source_file']}: {record['agg_is_shown_at']['wr_id']}")
            # except:
            #     unresolvable_resources.append(f"Identifier {record['id']} from DLME file {record['dlme_source_file']}: {record['agg_is_shown_at']['wr_id']}")

            # Resolve thumbnail url, get size for sample of images or all
            # depending on number of records in dataset
            # validate_url(record['agg_preview']['wr_id']) # will fail if invalid url
            # try:
            #     thumbnail = requests.get(record['agg_preview']['wr_id'], stream=True)
            #     if not resolve_url(thumbnail):
            #         unresolvable_thumbnails.append(f"Identifier {record['id']} from DLME file {record['dlme_source_file']}: {record['agg_preview']['wr_id']}")
            # except:
            #     unresolvable_thumbnails.append(f"Identifier {record['id']} from DLME file {record['dlme_source_file']}: {record['agg_preview']['wr_id']}")


            # if len(records) > 5000:
            #     if count%20==0:
            #         thumbnail_image_sizes.append(image_size(thumbnail))
            # elif len(records) > 500:
            #     if count%10==0:
            #         thumbnail_image_sizes.append(image_size(thumbnail))
            # if len(records) > 100:
            #     if count%2==0:
            #         thumbnail_image_sizes.append(image_size(thumbnail))
            # else:
            #     thumbnail_image_sizes.append(image_size(thumbnail))

    doc = dominate.document(title='DLME Metadata Report')

    with doc.head:
        style("""\
         body {
              font-family: sans-serif;
              margin: 3em 1em;
         }
         h1 {
              text-align: center;
         }
          .column {
              flex: 50%;
          }
         .report {
              border: 1px solid black;
              margin: 10px 25px 10px;
              padding: 5px 10px 5px;
         }
         .row {
              display: flex;
         }
     """)

    with doc:
        h1(f'DLME Metadata Report for {provider}, {collection} ({date.today()})')

        with div():
            attr(cls='body')
            attr(cls='row')
            # column one
            with div():
                attr(cls='column')
                # coverage report
                with div():
                    attr(cls='report')
                    h2('Coverage Report')
                    for item, counter in sorted(counts.items()):
                        languages = {}

                        p(b(f"{item}: ({int(((counts[item]['fields_covered'])/record_count)*100)}% coverage)"))

                        sub_field_list = ul()

                        for k,v in counter.items():
                            if k in IGNORE_VALUES:
                                continue
                            elif k == 'values' or k == 'wr_id':
                                sub_field_list += li(f'Average number of values: {round((v/record_count), 2)}')
                            else:
                                languages[k] = v

                        if languages:
                            sub_field_list += li(f'Average number of values: {round((sum(languages.values())/record_count), 2)}')
                            lang_list = ul()
                            sub_field_list += li(f'Languages:')
                            sub_field_list += lang_list
                            for k,v in languages.items():
                                lang_list += li(f'{k}: {v}')

            # column two
            with div():
                attr(cls='column')
                # resource report
                with div():
                    attr(cls='report')
                    h2('Resource Report')
                    with ul() as u_list:

                        u_list.add(li(f"{counts['agg_preview']['wr_id']} of {len(records)} records had valid urls to thumbnail images."))
                        if len(unresolvable_thumbnails) > 0:
                            u_list.add(li('The following thumbnails urls were unresolvable when testing:'))
                            unresolvable_thumbnails_list = u_list.add(ul())
                            for i in unresolvable_thumbnails:
                                unresolvable_thumbnails_list.add(li(i))

                        u_list.add(li(f"{counts['agg_is_shown_at']['wr_id']} of {len(records)} records had valid urls to resources."))
                        if len(unresolvable_resources) > 0:
                            u_list.add(li('The following resource urls were unresolvable when testing:'))
                            unresolvable_resources_list = u_list.add(ul())
                            for i in unresolvable_resources:
                                unresolvable_resources_list.add(li(i))
                        u_list.add(li(f"{counts['agg_is_shown_at']['wr_is_referenced_by']} of {len(records)} records had iiif manifests."))

                # rights report
                with div():
                    attr(cls='report')
                    h2('Rights Report')

                    u_list = ul()
                    u_list.add(li(f"{counts['cho_dc_rights']['fields_covered']} of {len(records)} records had a clearly expressed copyright status for the cultural heritage object."))
                    if counts['agg_is_shown_at']['wr_edm_rights'] > 0:
                        wr_count = counts['agg_is_shown_at']['wr_edm_rights']
                    else:
                        wr_count = counts['agg_is_shown_at']['wr_dc_rights']
                    u_list.add(li(f'{wr_count} of {len(records)} records had a clearly expressed copyright status for the web resource.'))
                    u_list.add(li(f"{counts['agg_edm_rights']['fields_covered']} of {len(records)} records had clearly expressed aggregation rights."))

                # thumbnail quality report
                with div():
                    attr(cls='report')
                    h2('Thumbnail Quality Report')
                    u_list = ul()
                    u_list.add(li(thumbnail_report(thumbnail_image_sizes)))

        # metadata crosswalk
        with div():
            attr(cls='row')
            attr(cls='report')
            h2('Metadata Crosswalk')

            with table(style = "border:2px solid black", border = 0):
                header = tr(style = "border:2px solid black")
                header.add(td('Incoming Field', style = "border:2px solid black"))
                header.add(td(style = "border:2px solid black"))
                header.add(td('DLME Field', style = "border:2px solid black"))
                header.add(td(style = "border:2px solid black"))
                header.add(td('Transformations', style = "border:2px solid black"))

                # crosswalk code
                # with open(args.config) as f:
                #     lines = f.readlines()
                #     for line in lines:
                #         for field in fields:
                #             if 'to_field' in line:
                #                 if field in line:
                #                     to_field = line.split(',')[0].strip('to_field ')
                #                     transforms = []
                #                     from_field = None
                #                     for k,v in extract_macros.items():
                #                         if k in line:
                #                             from_field = extract_macros.get(k).get('from_field')
                #                             transforms.append(extract_macros.get(k).get('transforms'))
                #                     # if no keys found in extract_macros
                #                     if from_field == None:
                #                         if 'literal(' in line:
                #                             from_field = "Assigned literal value: '{}'".format(line.split('literal(')[-1].split('),')[0])
                #                         else:
                #                             from_field = line.split('(')[1].split(')')[0].strip("'")
                #                     for k,v in modify_macros.items():
                #                         if k in line:
                #                             transforms.append(modify_macros.get(k))
                #                     with(tr):
                #                         td(from_field)
                #                         td(">>")
                #                         td(to_field)
                #                         td(">>")
                #                         td(' '.join(transforms))

    report = open(f'report_{provider}_{date.today()}.html', 'a')
    report.write(doc.render())

if __name__ == '__main__':
    # CLI client options.
    parser = ArgumentParser()
    parser.add_argument(
        "input",
        nargs="?",
        help="What is the file path to the intermediate representation?")
    parser.add_argument(
        'config',
        nargs='?',
        help='Which config file was used to transform the incoming records?')
    args = parser.parse_args()
    main()