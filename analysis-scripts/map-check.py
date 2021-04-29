#!/usr/bin/python
import csv, glob, json, math, ndjson, os, requests, urllib.request, validators
from argparse import ArgumentParser
from collections import Counter
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
    data_provider = records[0]['agg_data_provider']['en'][0]
    width = 50
    field_count = 0
    title = ' DLME Data Mapping Report for {} '.format(data_provider)
    header_padding = '*'*int((((width-len(title)+15)/2)))
    for record_count, record in enumerate(records, start=1):
        if args.field_one in record:
            field_count += 1

    print("{}{}{}".format(header_padding, title, header_padding))
    print("\n")

    # merge all records into single counter object and print field report
    print('All fields in DLME intermediate record\n')
    print('-' * (width+15) + '\n')
    field_report = Counter()
    for record in records:
        for item in record:
            field_report.update({item : 1})
        if 'agg_dc_rights' in record['agg_is_shown_at']:
            field_report.update({'agg_is_shown_at.agg_dc_rights' : 1})
        if 'agg_edm_rights' in record['agg_is_shown_at']:
            field_report.update({'agg_is_shown_at.agg_edm_rights' : 1})
        if 'wr_dc_rights' in record['agg_is_shown_at']:
            field_report.update({'agg_is_shown_at.wr_dc_rights' : 1})
        if 'wr_edm_rights' in record['agg_is_shown_at']:
            field_report.update({'agg_is_shown_at.wr_edm_rights' : 1})
        if 'wr_id' in record['agg_is_shown_at']:
            field_report.update({'agg_is_shown_at.wr_id' : 1})
        if 'wr_id' in record['agg_preview']:
            field_report.update({'agg_preview.wr_id' : 1})
        if 'wr_is_referenced_by' in record['agg_is_shown_at']:
            field_report.update({'agg_is_shown_at.wr_is_referenced_by' : 1})

    for item, count in field_report.items():
        print(item + ': ', end ="")
        padding = width - len(item) - len(str(count))
        for i in range(padding):
            print('-', end ="")
        print("{} of {} ({}%)".format(count, len(records), round(count/len(records)*100)))
    print('\n')

    return width, len(records), field_report

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

    width, record_count, field_counts, = field_report(records)

    record_count = len(records)

    print('DLME resource report\n')
    print('-' * (width+15) + '\n')
    print('- {} of {} records had urls to thumbnail images.'.format(field_counts['agg_preview.wr_id'], record_count))
    print('- {} of {} records had urls to resources.'.format(field_counts['agg_is_shown_at.wr_id'], record_count))
    print('- {} of {} records had iiif manifests.'.format(field_counts['agg_is_shown_at.wr_is_referenced_by'], record_count))
    print('\n')

    print('DLME rights report\n')
    print('-' * (width+15) + '\n')
    print('- {} of {} records had a clearly expressed copyright status for the cultural heritage object.'.format(field_counts['cho_dc_rights'], record_count))
    print('- {} of {} records had a clearly expressed copyright status for the web resource.'.format((field_counts['agg_is_shown_at.wr_edm_rights'] + field_counts['agg_is_shown_at.wr_dc_rights']), record_count))
    print('- {} of {} records had clearly expressed aggregation rights.'.format((field_counts['agg_is_shown_at.agg_dc_rights'] + field_counts['agg_is_shown_at.agg_edm_rights']), record_count))
    print('\n')

    print('DLME coverage report\n')
    print('-' * (width+15) + '\n')
    problem_field_count = 0
    coverage_threshold = 100
    for item, count in field_counts.items():
        if round(count/len(records)*100) < coverage_threshold:
            problem_field_count += 1
            print('- {} did not meet recommended coverage. {} of {} records included this field.'.format(item, count, record_count))
    if problem_field_count == 0:
        print('At least {}% of all fields were covered in the records.'.format(coverage_threshold))

    print('\n')
    print('''If you believe a mistake may have been made while mapping the above fields, please consult the crosswalk provided with this mapping report to ensure that the correct input field was mapped and report any issues to the DLME Data Manager, Jacob Hill (jtim@stanford.edu).''')

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
    passed = 0
    failed = 0
    rec_size = 150
    for record in records:
        thumbnail_urls.append(record['agg_preview']['wr_id'])
    if len(thumbnail_urls) > 10000:
        s = sample(thumbnail_urls,(math.floor(len(thumbnail_urls)/100)))
    elif len(thumbnail_urls) > 5000:
        s = sample(thumbnail_urls,(math.floor(len(thumbnail_urls)/75)))
    else:
        s = sample(thumbnail_urls,(math.floor(len(thumbnail_urls)/500)))
    for url in s:
        image = Image.open(requests.get(url, stream=True).raw)
        image_sizes.append(image.size)
    for i in image_sizes:
        if i[0] >= rec_size and i[1] >= rec_size:
            passed+=1
        else:
            failed+=1
    print('DLME thumnail image quality report\n')
    print('-' * 70 + '\n')
    print("{}% of thumbnail images met the minimum recommended width of {}x{}.".format((passed/len(image_sizes))*100, rec_size, rec_size))


# print record value
def get_values(records):
    # print to console
    with open('out_file.txt', 'w') as out_file:
        for record in records:
            if args.field_one in record:
                print(record[args.field_one])
                out_file.write('{}\n'.format(record[args.field_one]))
            else:
                pass

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
FUNCTION_MAP = {"inspect": inspect,
                "compare": compare,
                "crosswalk": crosswalk,
                "find_untransformed": find_untransformed,
                "records_missing_field": records_missing_field,
                "validate_script": validate_script,
                "validate_type": validate_type,
                "get_values": get_values,
                "validate_urls": validate_urls,
                "report": report,
                "resolve_urls": resolve_urls,
                "thumbnail_report": thumbnail_report}


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
            func(json_objects)

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
