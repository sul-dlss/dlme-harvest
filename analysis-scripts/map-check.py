#!/usr/bin/python
import csv, glob, json, math, ndjson, numpy, os, requests, urllib.request, validators, yaml
from argparse import ArgumentParser
from collections import Counter
from pathlib import Path
from PIL import Image
from random import sample

########## Inspection Helper Functions ##########

# Cluster field values
def cluster_fields(records):
    in_field_values = []
    out_field_values = []
    for record in records:
        if args.field_one in record:
            try:
                in_field_values.append(record[args.field_one][0])
            except:
                for i in record[args.field_one].items():
                    print(i[1])
                    in_field_values.append(i)
        if args.field_two in record:
            out_field_values.append(record[args.field_two][0])
    # count each value in list
    print("-------------------------------")
    print("Clusters:")
    try:
        in_clusters = Counter(in_field_values).most_common() # Count and convert to sorted list of lists
        out_clusters = Counter(out_field_values).most_common() # Count and convert to sorted list of lists
    except:
        in_clusters = in_field_values
        out_clusters = out_field_values
    return in_clusters, out_clusters

# field report showing frequesncy of each field in records
def field_report(records):
    ignore_fields = ['id', 'transform_version', 'transform_timestamp', 'dlme_source_file', 'agg_is_shown_at', 'agg_preview']
    data_provider = records[0]['agg_data_provider']['en'][0]
    width = 0
    field_count = 0
    title = ' DLME Data Mapping Report for {} '.format(data_provider)
    header_padding = '*'*int((((width-len(title)+15)/2)))
    for record_count, record in enumerate(records, start=1):
        if args.field_one in record:
            field_count += 1

    print("{}{}{}".format(header_padding, title, header_padding))
    print("\n")

    # merge all records into single counter object and print field report
    print('\033[1mAll fields in DLME intermediate record\033[0m')
    print('-' * (width+15) + '\n')
    field_counter = Counter()
    value_per_field_counter = Counter()
    lang_counter = {}
    for record in records:
        # Get field information
        for field, metadata in record.items():
            field_counter.update({field : 1})
            if type(metadata) == dict:
                for lang, values in metadata.items():
                    if lang_counter.get(field):
                        if lang_counter.get(field).get(lang):
                            lang_counter[field][lang] += 1
                        else:
                            lang_counter[field][lang] = 1
                    else:
                        lang_counter.update({field: {lang: 1}})
                    value_per_field_counter.update({field : len(values)})
            else:
                value_per_field_counter.update({field : len(metadata)})
        if 'agg_dc_rights' in record['agg_is_shown_at']:
            field_counter.update({'agg_is_shown_at.agg_dc_rights' : 1})
        if 'agg_edm_rights' in record['agg_is_shown_at']:
            field_counter.update({'agg_is_shown_at.agg_edm_rights' : 1})
        if 'wr_dc_rights' in record['agg_is_shown_at']:
            field_counter.update({'agg_is_shown_at.wr_dc_rights' : 1})
        if 'wr_edm_rights' in record['agg_is_shown_at']:
            field_counter.update({'agg_is_shown_at.wr_edm_rights' : 1})
        if 'wr_id' in record['agg_is_shown_at']:
            field_counter.update({'agg_is_shown_at.wr_id' : 1})
        if 'wr_id' in record['agg_preview']:
            field_counter.update({'agg_preview.wr_id' : 1})
        if 'wr_is_referenced_by' in record['agg_is_shown_at']:
            field_counter.update({'agg_is_shown_at.wr_is_referenced_by' : 1})

    ignore_value_counts = ['agg_data_provider_collection', 'agg_preview', 'agg_is_shown_at', 'cho_date_range_hijri', 'cho_date_range_norm', 'transform_timestamp', 'transform_version', 'id']
    for item, count in field_counter.items():
        if item not in ignore_fields:
            print(item + ': ', end ="")
            padding = width - len(item) - len(str(count))
            for i in range(padding):
                print('-', end ="")
            if value_per_field_counter.get(item) == None or item in ignore_value_counts or lang_counter.get(item) == None:
                print("{} of {} ({}%)".format(count, len(records), round(count/len(records)*100)))
            else:
                print("{} of {} ({}%)".format(count, len(records), round(count/len(records)*100)))
                print("     - Average number of values: {}".format(round(value_per_field_counter.get(item)/len(records), 2)))
                print("     - Languages: {}".format(lang_counter.get(item)))

    return width, len(records), field_counter

########## Core Functions for each Stage ##########

# inspect incoming values
def inspect(records, blank_lines, invalid_json):
    print("\n")
    print("There were {} blank lines in the intermediate representation.".format(len(blank_lines)))
    print("The blank lines were: {}".format(blank_lines))
    print('---------------------------------------------------------------------------------------')
    print("\n")
    print("There were {} invalid json objects in the intermediate representation.".format(len(invalid_json)))
    print('---------------------------------------------------------------------------------------')

    if len(invalid_json) > 0:
        print("Lines with invalid json: {}".format(invalid_json))
    print("\n")

    field_report(records)

# compare incoming field value to post processing field value
def compare(records):
    in_clusters, out_clusters = cluster_fields(records)
    values = []
    record_has_field_one_count = 0
    record_has_field_two_count = 0
    records_changed = 0
    directory = "/Users/jtim/Dropbox/DLSS/DLME/dlme-harvest/harvest-refactor/analysis-scripts/output"
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open("{}/{}-{}-and-{}.txt".format(directory, args.function, args.field_one, args.field_two), "w") as f:
        for record_count, record in enumerate(records, start=1):
            if args.field_one in record:
                record_has_field_one_count += 1
                field_one = record[args.field_one]
                if args.field_two in record:
                    record_has_field_two_count += 1
                    field_two = record[args.field_two]
                    if field_one == field_two:
                        pass
                    else:
                        records_changed += 1
                        print("{} => {}".format(field_one, field_two))
                        values.append("{} ========> {}".format(field_one, field_two))
        for i in set(values):
            print(i)
            f.write("{}\n\n".format(i))
        if len(in_clusters) == len(out_clusters):
            for in_item, out_item in zip(in_clusters, in_clusters):
                print("{}: {} => {}".format(in_item[1], in_item[0], out_item[0]))
        else:
            print("Warning: the number of incoming values {} does not match the numnber of outgoing values {}.".format(len(in_clusters), len(out_clusters)))
        print("------------------------------------")
        print("Summary:")
        print("{} of {} records have the {} field.".format(record_has_field_one_count, record_count, args.field_one))
        print("{} of {} records have the {} field.".format(record_has_field_two_count, record_count, args.field_two))
        print("{} of {} records transformed.".format(records_changed, record_count))
        f.write("------------------------------------\n")
        f.write("Summary:\n")
        f.write("{} of {} records have the {} field.\n".format(record_has_field_one_count, record_count, args.field_one))
        f.write("{} of {} records have the {} field.\n".format(record_has_field_two_count, record_count, args.field_two))
        f.write("{} of {} records transformed.\n".format(records_changed, record_count))

def report(records):

    width, record_count, field_counts = field_report(records)

    record_count = len(records)

    print('\n\033[1mDLME resource report\033[0m')
    print('-' * (width+15) + '\n')
    print('- {} of {} records had urls to thumbnail images.'.format(field_counts['agg_preview.wr_id'], record_count))
    print('- {} of {} records had urls to resources.'.format(field_counts['agg_is_shown_at.wr_id'], record_count))
    print('- {} of {} records had iiif manifests.'.format(field_counts['agg_is_shown_at.wr_is_referenced_by'], record_count))

    # thumbnail_report(records)

    print('\033[1mDLME rights report\033[0m')
    print('-' * (width+15) + '\n')
    print('- {} of {} records had a clearly expressed copyright status for the cultural heritage object.'.format(field_counts['cho_dc_rights'], record_count))
    wr_edm = field_counts['agg_is_shown_at.wr_edm_rights']
    wr_dc = field_counts['agg_is_shown_at.wr_dc_rights']
    if wr_edm > 0:
        wr_count = wr_edm
    else:
        wr_count = wr_dc
    print('- {} of {} records had a clearly expressed copyright status for the web resource.'.format(wr_count, record_count))
    print('- {} of {} records had clearly expressed aggregation rights.'.format((field_counts['agg_edm_rights']), record_count))

    # print('DLME coverage report\n')
    # print('-' * (width+15) + '\n')
    # problem_field_count = 0
    # coverage_threshold = 100
    # for item, count in field_counts.items():
    #     if round(count/len(records)*100) < coverage_threshold:
    #         problem_field_count += 1
    #         print('- {} did not meet recommended coverage. {} of {} records included this field.'.format(item, count, record_count))
    # if problem_field_count == 0:
    #     print('At least {}% of all fields were covered in the records.'.format(coverage_threshold))

    # print('\n')
    # print('''If you believe a mistake may have been made while mapping the above fields, please consult the crosswalk provided with this mapping report to ensure that the correct input field was mapped and report any issues to the DLME Data Manager, Jacob Hill (jtim@stanford.edu).''')

########## Functions for Debugging Transformations ##########


# use FIELD_MAP and args.field to determine which validation function to call
def records_missing_field(records):
    for record in records:
        if args.field_one in record:
            pass
        else:
            print(record['dlme_source_file'])

# in progress function for validating script
def validate_script(records):
    fields = []
    switcher = {
        'ar-Arab': ['a', 'e', 'i', 'o', 'u'],
        'en': ['ا' 'و', 'أ', 'ى', 'ي', 'إ']
    }
    # switcher.get(record[key], "Invalid script")
    for record in records:
        for key, value in record.items():
            if type(value) == dict:
                for key_two, value_two in value.items():
                    if switcher[key_two]:
                        print(switcher[key_two])

                        vowels = record[key]
                        for vowel in vowels:
                            print(vowel)

# validate type of record value
def validate_type(records):
    type_counts = Counter()
    for record in records:
        if args.field_one in record:
            if isinstance(record[args.field_one], str):
                type_counts.update({'string' : 1})
            elif isinstance(record[args.field_one], list):
                type_counts.update({'list' : 1})
            elif isinstance(record[args.field_one], dict):
                type_counts.update({'dictionary' : 1})
            else:
                type_counts.update({'other type' : 1})
    print(type_counts)

# check a sample of thumbnails and report on quality
def thumbnail_report(records):
    thumbnail_urls = []
    image_sizes = []
    passed_rec = 0
    failed_rec = 0
    rec_size = 400
    for record in records:
        thumbnail_urls.append(record['agg_preview']['wr_id'])
    if len(thumbnail_urls) > 10000:
        s = sample(thumbnail_urls, 1000)
    elif len(thumbnail_urls) < 1000 and len(thumbnail_urls) >= 100:
        s = sample(thumbnail_urls, 100)
    elif len(thumbnail_urls) < 100:
        s = thumbnail_urls
    else:
        s = sample(thumbnail_urls,(math.floor(len(thumbnail_urls)/10)))
    for url in s:
        image = Image.open(requests.get(url, stream=True).raw)
        image_sizes.append(image.size)
        # This portion is part of my test code
        # byteImgIO = io.BytesIO()
        # byteImg = Image.open("output/images/image.png")
        # byteImg.save(byteImgIO, "PNG")
        # byteImgIO.seek(0)
        # byteImg = byteImgIO.read()
        #
        # # Non test code
        # dataBytesIO = io.BytesIO(byteImg)
        # Image.open(dataBytesIO)

        for i in image_sizes:
            if i[0] >= rec_size and i[1] >= rec_size:
                passed_rec+=1
            else:
                failed_rec+=1
    print('\n\033[1mDLME thumbnail image quality report (a sample of {} thumbnail images were tested)\033[0m'.format(len(s)))
    print('-' * 70 + '\n')
    print("{}% of thumbnail images met the recommended size of {}x{}.".format(round((passed_rec/len(image_sizes))*100), rec_size, rec_size))
    i_one = 0
    i_two = 0
    for i in image_sizes:
        i_one += i[0]
        i_two += i[1]
    print("The average image size of the sample was {}x{}.\n".format(math.floor((i_one/len(image_sizes))), math.floor((i_two/len(image_sizes)))))

# print record value
def get_values(records):
    # print to console
    with open('output/out_file.txt', 'w') as out_file:
        for record in records:
            if args.field_one in record:
                print(record[args.field_one])
                out_file.write('{}\n'.format(record[args.field_one]))
            else:
                pass

# print unique values from a field formatted for inclusion in a translation map
def unique_values(records):
    values = []
    # print to console
    with open('output/out_file.yaml', 'w') as out_file:
        for record in records:
            if args.field_one in record:
                try:
                    if type(record[args.field_one]) == dict:
                        for k,v in record[args.field_one].items():
                            values.extend(v)
                    else:
                        values.extend(record[args.field_one])
                except:
                    values.extend(record[args.field_one][0]['values'])
            else:
                pass
        for v in numpy.unique(values):
            print(v+':')
            out_file.write(v+':\n')

    return numpy.unique(values)

def not_found(records):
    # when cho_type arg passed, returns any value in cho_type not
    # found in the type translation maps.
    field_values = []
    map_values = []
    translation_maps = []

    for record in records:
        try:
            if args.field_one in record:
                for k,v in record[args.field_one].items():
                    field_values.extend(v)
        except:
            field_values.extend(record[args.field_one][0]['values'])
        else:
            pass

    if args.field_one == 'cho_medium':
        translation_maps.append('/Users/jtim/Dropbox/DLSS/DLME/dlme-transform/lib/translation_maps/getty_aat_materials.yaml')

    elif args.field_one == 'cho_type':
        for file in glob.glob('/Users/jtim/Dropbox/DLSS/DLME/dlme-transform/lib/translation_maps/*.yaml'):
            if '_from_' in file:
                translation_maps.append(file)

    elif args.field_one == 'cho_spatial':
        translation_maps.append('/Users/jtim/Dropbox/DLSS/DLME/dlme-transform/lib/translation_maps/spatial_from_contributor.yaml')

    elif args.field_one == 'cho_temporal':
        translation_maps.append('/Users/jtim/Dropbox/DLSS/DLME/dlme-transform/lib/translation_maps/temporal_from_contributor.yaml')

    for i in translation_maps:
        data = yaml.safe_load(open(i, 'r'))
        for k, v in data.items():
            map_values.append(k)

    unique_values = (set([x.lower() for x in field_values]) - set([x.lower() for x in map_values]))
    for i in sorted(unique_values):
        print(i+':')

    number_of_terms = len(unique_values)
    print("{} terms found.".format(number_of_terms))

    return unique_values, number_of_terms

def extend_map(records):
    if args.field_one == 'cho_has_type':
        # Adds values found in cho_type field to translation map.
        unique_values, number_of_terms = not_found(records)
        has_types = yaml.safe_load(open('/Users/jtim/Dropbox/DLSS/DLME/dlme-transform/lib/translation_maps/has_type_from_contributor.yaml', 'r'))
        merged = {**dict.fromkeys(unique_values, 0), **has_types}

        if number_of_terms + len(has_types) == len(merged):
            with open('/Users/jtim/Dropbox/DLSS/DLME/dlme-transform/lib/translation_maps/has_type_from_contributor_extended.yaml', 'w') as f:
                yaml.safe_dump(merged, f, default_flow_style=False, allow_unicode=False)

        else:
            print('Wrong number of items')

    elif args.field_one == 'cho_temporal':
        # Adds values found in cho_type field to translation map.
        unique_values, number_of_terms = not_found(records)
        temporal = yaml.safe_load(open('/Users/jtim/Dropbox/DLSS/DLME/dlme-transform/lib/translation_maps/temporal_from_contributor.yaml', 'r'))
        merged = {**dict.fromkeys(unique_values, 0), **temporal}

        if number_of_terms + len(temporal) == len(merged):
            with open('/Users/jtim/Dropbox/DLSS/DLME/dlme-transform/lib/translation_maps/temporal_from_contributor_extended.yaml', 'w') as f:
                yaml.safe_dump(merged, f, default_flow_style=False, allow_unicode=False)
        else:
            print('Wrong number of items')

def build_controlled_vocabulary():
    # Builds controlled vocabularies from translation maps.
    edm_rights_en_translation_maps = []
    edm_rights_en_values = []
    edm_type_en_translation_maps = []
    edm_type_en_values = []
    has_type_en_translation_maps = []
    has_type_en_values = []
    material_en_translation_maps = []
    material_en_values = []
    spatial_en_translation_maps = []
    spatial_en_values = []
    temporal_en_translation_maps = []
    temporal_en_values = []

    for file in glob.glob('/Users/jtim/Dropbox/DLSS/DLME/dlme-transform/lib/translation_maps/edm_rights*.yaml'):
        edm_rights_en_translation_maps.append(file)

    for file in glob.glob('/Users/jtim/Dropbox/DLSS/DLME/dlme-transform/lib/translation_maps/edm_type_from*.yaml'):
        edm_type_en_translation_maps.append(file)

    for file in glob.glob('/Users/jtim/Dropbox/DLSS/DLME/dlme-transform/lib/translation_maps/has_type_from*.yaml'):
        has_type_en_translation_maps.append(file)

    for file in glob.glob('/Users/jtim/Dropbox/DLSS/DLME/dlme-transform/lib/translation_maps/getty_aat_material_from*.yaml'):
        material_en_translation_maps.append(file)

    for file in glob.glob('/Users/jtim/Dropbox/DLSS/DLME/dlme-transform/lib/translation_maps/spatial_from*.yaml'):
        spatial_en_translation_maps.append(file)

    for file in glob.glob('/Users/jtim/Dropbox/DLSS/DLME/dlme-transform/lib/translation_maps/temporal_from*.yaml'):
        temporal_en_translation_maps.append(file)

    p = Path('/Users/jtim/Dropbox/DLSS/DLME/dlme-transform/lib/controlled_vocabularies')
    p.mkdir(exist_ok=True)

    if args.field_one == 'edm_type_en':
        for i in edm_type_en_translation_maps:
            data = yaml.safe_load(open(i, 'r'))
            for k, v in data.items():
                if type(v) == list:
                    edm_type_en_values.extend(v)
                elif type(v) == None:
                    pass
                else:
                    edm_type_en_values.append(v)

        with open('/Users/jtim/Dropbox/DLSS/DLME/dlme-transform/lib/controlled_vocabularies/edm_type_en.yaml', 'w') as out:
            yaml.safe_dump(sorted(set(edm_type_en_values)), out, default_flow_style=False, allow_unicode=False)

    if args.field_one == 'has_type_en':
        for i in has_type_en_translation_maps:
            data = yaml.safe_load(open(i, 'r'))
            for k, v in data.items():
                if type(v) == list:
                    has_type_en_values.extend(v)
                elif type(v) == str:
                    has_type_en_values.append(v)
                else:
                    pass

        with open('/Users/jtim/Dropbox/DLSS/DLME/dlme-transform/lib/controlled_vocabularies/has_type_en.yaml', 'w') as out:
            yaml.safe_dump(sorted(set(has_type_en_values)), out, default_flow_style=False, allow_unicode=False)

    if args.field_one == 'material_en':
        for i in material_en_translation_maps:
            data = yaml.safe_load(open(i, 'r'))
            for k, v in data.items():
                if type(v) == list:
                    material_en_values.extend(v)
                elif type(v) == str:
                    material_en_values.append(v)
                else:
                    pass

        with open('/Users/jtim/Dropbox/DLSS/DLME/dlme-transform/lib/controlled_vocabularies/getty_aat_material_en.yaml', 'w') as out:
            yaml.safe_dump(sorted(set(material_en_values)), out, default_flow_style=False, allow_unicode=False)

    if args.field_one == 'spatial_en':
        for i in spatial_en_translation_maps:
            data = yaml.safe_load(open(i, 'r'))
            for k, v in data.items():
                if type(v) == list:
                    spatial_en_values.extend(v)
                elif type(v) == str:
                    spatial_en_values.append(v)
                else:
                    pass

        with open('/Users/jtim/Dropbox/DLSS/DLME/dlme-transform/lib/controlled_vocabularies/spatial_en.yaml', 'w') as out:
            yaml.safe_dump(sorted(set(spatial_en_values)), out, default_flow_style=False, allow_unicode=False)

    if args.field_one == 'temporal_en':
        for i in temporal_en_translation_maps:
            data = yaml.safe_load(open(i, 'r'))
            for k, v in data.items():
                if type(v) == list:
                    temporal_en_values.extend(v)
                elif type(v) == str:
                    temporal_en_values.append(v)
                else:
                    pass

        with open('/Users/jtim/Dropbox/DLSS/DLME/dlme-transform/lib/controlled_vocabularies/temporal_en.yaml', 'w') as out:
            yaml.safe_dump(sorted(set(temporal_en_values)), out, default_flow_style=False, allow_unicode=False)

    if args.field_one == 'edm_rights_en':
        for i in edm_rights_en_translation_maps:
            data = yaml.safe_load(open(i, 'r'))
            for k, v in data.items():
                if type(v) == list:
                    edm_rights_en_values.extend(v)
                elif type(v) == str:
                    edm_rights_en_values.append(v)
                else:
                    pass

        with open('/Users/jtim/Dropbox/DLSS/DLME/dlme-transform/lib/controlled_vocabularies/edm_rights_en.yaml', 'w') as out:
            yaml.safe_dump(sorted(set(edm_rights_en_values)), out, default_flow_style=False, allow_unicode=False)




def check_translation_maps():
    # Ensures that all values in the has_type translation maps are fully mapped
    # to cho_edm_type and fully translated into Arabic.
    ar_edm_types = []
    ar_has_types = []
    edm_keys = []
    edm_values = []
    has_type_values = []
    material_values = []
    material_values_ar = []
    spatial_values = []
    spatial_values_ar = []
    temporal_values = []
    temporal_values_ar = []

    ar_edm = yaml.safe_load(open('/Users/jtim/Dropbox/DLSS/DLME/dlme-transform/lib/translation_maps/edm_type_ar_from_en.yaml', 'r'))
    for k, v in ar_edm.items():
        ar_edm_types.append(k)
    ar_has = yaml.safe_load(open('/Users/jtim/Dropbox/DLSS/DLME/dlme-transform/lib/translation_maps/has_type_ar_from_en.yaml', 'r'))
    for k, v in ar_has.items():
        ar_has_types.append(k)
    edm = yaml.safe_load(open('/Users/jtim/Dropbox/DLSS/DLME/dlme-transform/lib/translation_maps/edm_type_from_has_type.yaml', 'r'))
    for k, v in edm.items():
        edm_keys.append(k)
        if type(v) == str:
            edm_values.append(v)
        else:
            edm_values.extend(v)
    has_type = yaml.safe_load(open('/Users/jtim/Dropbox/DLSS/DLME/dlme-transform/lib/translation_maps/has_type_from_contributor.yaml', 'r'))
    for k, v in has_type.items():
        if type(v) == str:
            has_type_values.append(v)
        elif type(v) == list:
            has_type_values.extend(v)
        else:
            pass

    material = yaml.safe_load(open('/Users/jtim/Dropbox/DLSS/DLME/dlme-transform/lib/translation_maps/getty_aat_material_from_contributor.yaml', 'r'))
    for k, v in material.items():
        if type(v) == str:
            material_values.append(v)
        elif type(v) == list:
            material_values.extend(v)
        else:
            pass
    material_ar = yaml.safe_load(open('/Users/jtim/Dropbox/DLSS/DLME/dlme-transform/lib/translation_maps/getty_aat_material_ar_from_en.yaml', 'r'))
    for k, v in material_ar.items():
        material_values_ar.append(k)

    spatial = yaml.safe_load(open('/Users/jtim/Dropbox/DLSS/DLME/dlme-transform/lib/translation_maps/spatial_from_contributor.yaml', 'r'))
    for k, v in spatial.items():
        if type(v) == str:
            spatial_values.append(v)
        elif type(v) == list:
            spatial_values.extend(v)
        else:
            pass
    spatial_ar = yaml.safe_load(open('/Users/jtim/Dropbox/DLSS/DLME/dlme-transform/lib/translation_maps/spatial_ar_from_en.yaml', 'r'))
    for k, v in spatial_ar.items():
        spatial_values_ar.append(k)

    temporal = yaml.safe_load(open('/Users/jtim/Dropbox/DLSS/DLME/dlme-transform/lib/translation_maps/temporal_from_contributor.yaml', 'r'))
    for k, v in temporal.items():
        if type(v) == str:
            temporal_values.append(v)
        elif type(v) == list:
            temporal_values.extend(v)
        else:
            pass
    temporal_ar = yaml.safe_load(open('/Users/jtim/Dropbox/DLSS/DLME/dlme-transform/lib/translation_maps/temporal_ar_from_en.yaml', 'r'))
    for k, v in temporal_ar.items():
        temporal_values_ar.append(k)

    if len((set([x.lower() for x in edm_values]) - set([x.lower() for x in ar_edm_types]))) > 0:
        print('edm_type_ar_from_en.yaml is missing the following keys:')
        for i in (set([x.lower() for x in edm_values]) - set([x.lower() for x in ar_edm_types])):
            print(i+':')

    if len((set([x.lower() for x in has_type_values]) - set([x.lower() for x in ar_has_types]))) > 0:
        print('has_type_ar_from_en.yaml is missing the following keys:')
        for i in (set([x.lower() for x in has_type_values]) - set([x.lower() for x in ar_has_types])):
            print(i+':')

    if len((set([x.lower() for x in has_type_values]) - set([x.lower() for x in edm_keys]))) > 0:
        print('edm_type_from_has_type.yaml is missing the following keys:')
        for i in (set([x.lower() for x in has_type_values]) - set([x.lower() for x in edm_keys])):
            print(i+':')

    if len((set([x.lower() for x in spatial_values]) - set([x.lower() for x in spatial_values_ar]))) > 0:
        print('spatial_ar_from_en.yaml is missing the following keys:')
        for i in (set([x.lower() for x in spatial_values]) - set([x.lower() for x in spatial_values_ar])):
            print(i+':')

    if len((set([x for x in temporal_values]) - set([x for x in temporal_values_ar]))) > 0:
        print('temporal_ar_from_en.yaml is missing the following keys:')
        new_list = sorted(list((set([x for x in temporal_values]) - set([x for x in temporal_values_ar]))))
        for i in new_list:
            print(i+':')

    if len((set([x for x in material_values]) - set([x for x in material_values_ar]))) > 0:
        print('getty_aat_material_ar_from_en.yaml is missing the following keys:')
        new_list = sorted(list((set([x for x in material_values]) - set([x for x in material_values_ar]))))
        for i in new_list:
            print(i+':')

def find_untransformed(records):
    with open('out_file.txt', 'w') as out_file:
        untransformed = glob.glob("/Users/jtim/Dropbox/DLSS/DLME/dlme-metadata/michigan/data/*.xml")
        print(untransformed)
        transformed = []
        for record in records:
            transformed.append("/Users/jtim/Dropbox/DLSS/DLME/dlme-metadata/{}".format(record['dlme_source_file']))
        # list(set(transformed) - set(untransformed)))
        if args.field_one in record:
            print(list(set(transformed) - set(untransformed)))
            out_file.write('{}\n'.format(list(set(transformed) - set(untransformed))))

# validate urls
def validate_urls(records):
    invalid_url_counts = Counter()
    for record in records:
        if args.field_one in record:
            valid=validators.url(record[args.field_one]['wr_id'])
            if valid==True:
                pass
            else:
                invalid_url_counts.update({'Invalid urls' : 1})
                print("id: {} \n url: {} \n".format(record['id'], record[args.field_one]['wr_id']))

    print("There were {} invalid urls.".format(invalid_url_counts['Invalid urls']))

# validate urls
def resolve_urls(records):
    unresolvable_url_counts = Counter()
    unresolvabel_urls = {}
    for count, record in enumerate(records, start=1):
        if args.field_one in record:
            try:
                print("Checking {} of {}".format(count, len(records)))
                status_code = urllib.request.urlopen(record[args.field_one]['wr_id']).getcode()
                if status_code==200:
                    pass
                else:
                    unresolvable_url_counts.update({'Unresolvable urls' : 1})
                    print("id: {} \n url: {} \n".format(record['id'], record[args.field_one]['wr_id']))
                    unresolvabel_urls[record['id']] = record[args.field_one]['wr_id']
            except:
                print('Url timeout')

    print("There were {} bad urls.".format(bad_url_counts['Bad urls']))
    for k,v in unresolvabel_urls.items():
        print(k, v)

########## Function Maps ##########

# Function dispatcher to map stage arguments to function names
FUNCTION_MAP = {"build_controlled_vocabulary": build_controlled_vocabulary,
                "check_translation_maps": check_translation_maps,
                "compare": compare,
                "extend_map": extend_map,
                "find_untransformed": find_untransformed,
                "inspect": inspect,
                "get_values": get_values,
                "records_missing_field": records_missing_field,
                "report": report,
                "resolve_urls": resolve_urls,
                "thumbnail_report": thumbnail_report,
                "not_found": not_found,
                "unique_values": unique_values,
                "validate_script": validate_script,
                "validate_type": validate_type,
                "validate_urls": validate_urls}

########## Main Loop ##########

def main():
    failed_lines = 0
    # Get all ndjson files from output and sort from oldest to newest
    files = sorted(glob.glob("/Users/jtim/Dropbox/DLSS/DLME/dlme-transform/output/*.ndjson"), key=os.path.getmtime)
    file = files[-1]
    # Get any file you want
    # file = "/Users/jtim/Dropbox/DLSS/DLME/dlme-transform/output/output-3dfa0243-0570-45b8-ba70-ed40c759ed03.ndjson"
    func = FUNCTION_MAP[args.function] # Map argument to function dispatcher
    # Get the path to the newest file
    with open(file, "r") as f:
        blank_lines = []
        invalid_json = []
        json_objects = []
        ir = f.readlines()
        for count, line in enumerate(ir, start=1):
            if len(line) == 1:
                blank_lines.append(count)
            else:
                try:
                    json_objects.append(json.loads(line))
                except ValueError as e:
                    invalid_json.append("Line {} does not contain valid json.".format(count))
        # call the funtion passed through as an argument on json_objects
        if args.function == 'inspect':
            func(json_objects, blank_lines, invalid_json)
        else:
            try:
                func(json_objects)
            except:
                func()

if __name__ == "__main__":
    # CLI client options.
    parser = ArgumentParser()
    # Temporarily hard coded file path above
    # parser.add_argument(
    #     "file",
    #     help="What is the path to the ndjson file?")
    parser.add_argument(
        "function", choices=FUNCTION_MAP.keys(),
        help="Which function do you want [inspect, compare, or validate]? ")
    parser.add_argument(
        "field_one",
        nargs="?",
        help="Which field do you want to compare?")
    parser.add_argument(
        "field_two",
        nargs="?",
        help="This is currently a generic second field that will change depending on the function you call. It could be another data field or a dictionary key, for example.")

    args = parser.parse_args()
    main()
