#!/usr/bin/python
import json, os
import pandas as pd
from argparse import ArgumentParser
from lxml import etree

def main():
    # Main variables
    json_keys_with_values = []
    csv_col_names_with_values = []
    xml_elements_with_values = []
    # Main loop
    for file in os.listdir(args.file[0]):
        # csv files
        if file.endswith('.csv'):
            df = pd.read_csv("{}{}".format(args.file[0], file))
            for col_name in df.columns:
                csv_col_names_with_values.append(col_name)

        # json files
        elif file.endswith('.json'):

            with open("{}{}".format(args.file[0], file)) as f:
                data = json.load(f)
                # Will catch nested key, value pairs to the third level
                for (k, v) in data.items():
                    if v:
                        json_keys_with_values.append(k)
                        if isinstance(v, dict):
                            for (k_1, v_1) in v.items():
                                if v_1:
                                    json_keys_with_values.append("{}.{}".format(k, k_1))
                                    if isinstance(v_1, dict):
                                        for (k_2, v_2) in v_1.items():
                                            if v_2:
                                                json_keys_with_values.append("{}.{}.{}".format(k, k_1, k_2))

        # xml files
        elif file.endswith('.xml'):
                tree = etree.parse("{}{}".format(args.file[0], file))
                root = tree.getroot()
                events = ('start', 'end')
                for event, element in etree.iterparse("{}{}".format(args.file[0], file)):
                # context = etree.iterparse("{}{}".format(args.file[0], file), events=events)
                # for action, elem in context:
                    if element.text:
                        xml_elements_with_values.append(element.tag)

        # Print results
        # if args.file[0].endswith('.csv'):
    print(set(csv_col_names_with_values))
        # elif args.file[0].endswith('.json'):
    print(set(json_keys_with_values))
        # else:
    for elem in set(xml_elements_with_values):
        print(elem)

if __name__ == '__main__':
    # CLI client options.
    parser = ArgumentParser()
    parser.add_argument(
        'file',
        nargs='+',
        help='Which file do you want to parse?')
    args = parser.parse_args()
    main()
