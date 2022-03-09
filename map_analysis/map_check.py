#!/usr/bin/python
from argparse import ArgumentParser
from collections import Counter
from datetime import datetime
import numpy as np
import json

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
        # if 'wr_id' in record['agg_preview']:
        #     field_counter.update({'agg_preview.wr_id' : 1})
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

# finds records missing a particular field
# @param a list of DLME intermediate representation json records
# @example "python map_check.py /Users/jtim/Dropbox/DLSS/DLME/dlme-transform/output/output-brooklyn-museum.ndjson records_missing_field cho_title"
def records_missing_field(records):
    for record in records:
        if args.field_one in record:
            pass
        else:
            print(record['dlme_source_file'])

# prints unique values from a field
# @param a list of DLME intermediate representation json records
# @example "python map_check.py /Users/jtim/Dropbox/DLSS/DLME/dlme-transform/output/output-brooklyn-museum.ndjson unique_values cho_edm_type"
# returns a list of unique vales
def unique_values(records):
    values = []
    with open(f"output/unique_values{args.file.split('/')[-1].split('-')[-1].split('.')[0]}_{datetime.today().strftime('%Y-%m-%d')}.txt", 'w') as out_file:
        for record in records:
            if args.field_one in record:
                if type(record[args.field_one]) == dict:
                    for k,v in record[args.field_one].items():
                        values.extend(v)
                elif type(record[args.field_one]) == list:
                    values.extend(record[args.field_one])
                else:
                    values.append(record[args.field_one])
        for v in np.unique(values):
            print(v+':')
            out_file.write(v+':\n')

    return np.unique(values)

# Function dispatcher to map stage arguments to function names
FUNCTION_MAP = {"field_report": field_report,
                "records_missing_field": records_missing_field,
                "unique_values": unique_values
               }

########## Main Loop ##########

def main():
    with open(args.file, "r") as f:
        func = FUNCTION_MAP[args.function] # Map argument to function dispatcher
    # Get the path to the newest file
        ir = f.readlines()
        json_objects = []
        invalid_json = []
        for count, line in enumerate(ir, start=1):
            try:
                json_objects.append(json.loads(line))
            except ValueError as e:
                invalid_json.append("Line {} does not contain valid json.".format(count))

        try:
            func(json_objects)
        except:
            func()

if __name__ == "__main__":
    # CLI client options.
    parser = ArgumentParser()

    parser.add_argument(
        "file",
        nargs="?",
        help="Which file do you want to validate?")
    parser.add_argument(
        "function", choices=FUNCTION_MAP.keys(),
        help="Which function do you want? ")
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
