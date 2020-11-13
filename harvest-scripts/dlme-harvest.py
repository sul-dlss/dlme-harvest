#!/usr/bin/python
import json
from argparse import ArgumentParser
from subprocess import call

def main():
    with open('map.json') as map:
        data = json.load(map)
        if args.institution == 'all': # harvest all collections
            try:
                for m in data:
                    for script in m['harvest']:
                        __import__(script)
                        call(["python", "{}.py".format(script)])
            except:
                print('Error: Check the map.json file and your spelling; make sure there are no errors in the harvesting script.')
        else: # harvest collection specified
            try:
                for m in data:
                    if m['institution'] == args.institution:
                        for script in m['harvest']:
                            __import__(script)
                            call(["python", "{}.py".format(script)])
            except:
                print('Error: Check the map.json file and your spelling; make sure there are no errors in the harvesting script.')

if __name__ == "__main__":
    # CLI client options.
    parser = ArgumentParser()
    parser.add_argument(
        "institution",
        help="put the institution name (see harvest-mapping.json) you want harvested here.")

    args = parser.parse_args()
    main()
