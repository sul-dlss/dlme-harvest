#!/usr/bin/python
import glob, ndjson, os
from argparse import ArgumentParser
from collections import Counter


########## Inspection Helper Functions ##########


# Cluster field values
def cluster_fields(records):
    in_field_values = []
    out_field_values = []
    for record in records:
        if args.field_one in record:
            in_field_values.append(record[args.field_one][0])
        if args.field_two in record:
            out_field_values.append(record[args.field_two][0])
    # Count each value in list
    print("-------------------------------")
    print("Clusters:")
    in_clusters = Counter(in_field_values).most_common() # Count and convert to sorted list of lists
    out_clusters = Counter(out_field_values).most_common() # Count and convert to sorted list of lists
    return in_clusters, out_clusters
    # for item in clusters:
    #     print("{}: {}".format(item[0], item[1]))


########## Comparision Helper Functions ##########


# Validate output of date normalization
def validate_cho_date_norm(records):
    for record in records:
        if args.field_two in record:
            output = record[args.field_two]
            for date in output:
                if len(date) == 4 and date.isdigit():
                    pass
                else:
                    print("Date validation error: the output value is '{}'\n".format(date))
                    print("The record id is {}\n".format(record['id']))
                    print("cho_date_norm: {}".format(record[args.field_two]))
                    break
                break
        break

########## Validation Helper Functions ##########


# Validate cho_date field
def validate_cho_date(records):
    for record in records:
        id = record['id']
        if args.field in record:
            field = record[args.field]
            try:
                print(field[1].isdigit())
            except:
                print("{} is not a digit; record id is: {}". format(field[1], id))
                print('\n')


########## Core Functions for each Stage ##########


# Inspect incoming values
def inspect(records):
    in_clusters = cluster_fields(records)[0]
    for item in in_clusters:
        print("{}: {}".format(item[0], item[1]))
    field_count = 0
    for record_count, record in enumerate(records, start=1):
        if args.field_one in record:
            field_count += 1
    print("{} of {} records have the {} value".format(field_count, record_count, args.field_one))


# Compare incoming field value to post processing field value
def compare(records):
    # in_clusters, out_clusters = cluster_fields(records)
    record_has_field_one_count = 0
    record_has_field_two_count = 0
    records_changed = 0
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
    # if len(in_clusters) == len(out_clusters):
    #     for in_item, out_item in zip(in_clusters, in_clusters):
    #         print("{}: {} => {}".format(in_item[1], in_item[0], out_item[0]))
    # else:
    #     print("Error: the number of incoming values does not match the numnber of outgoing values.")
    print("------------------------------------")
    print("Summary:")
    print("{} of {} records have the {} field.".format(record_has_field_one_count, record_count, args.field_one))
    print("{} of {} records have the {} field.".format(record_has_field_two_count, record_count, args.field_two))
    print("{} of {} records transformed.".format(records_changed, record_count))

# Use FIELD_MAP and args.field to determine which validation function to call
def validate(records):
    func = FIELD_MAP[args.field_two] # Use dispatcher to map argument to function
    func(records)


########## Function Maps ##########


# Function dispatcher to map field arguments to function names
FIELD_MAP = {'cho_date': validate_cho_date_norm,
             'cho_subject': validate_cho_date}

# Function dispatcher to map stage arguments to function names
FUNCTION_MAP = {'inspect': inspect,
                'compare': compare,
                'validate': validate}


########## Main Loop ##########


def main():
    # Get all ndjson files from output and sort from oldest to newest
    files = sorted(glob.glob('/Users/jtim/Dropbox/DLSS/DLME/dlme-transform/output/*.ndjson'), key=os.path.getmtime)
    # Get the path to the newest file
    with open(files[-1], 'r') as f:
        data = ndjson.load(f)
        func = FUNCTION_MAP[args.stage] # Map argument ot function dispatcher
        func(data)


if __name__ == "__main__":
    # CLI client options.
    parser = ArgumentParser()
    # Temporarily hard coded file path above
    # parser.add_argument(
    #     "file",
    #     help="What is the path to the ndjson file?")
    parser.add_argument(
        "stage", choices=FUNCTION_MAP.keys(),
        help="Which stage are you on [inspect, compare, or validate]? ")
    parser.add_argument(
        "field_one",
        help="Which field do you want to compare?")
    parser.add_argument(
        "field_two",
        nargs='?',
        help="Which field do you want to compare?")

    args = parser.parse_args()
    main()
