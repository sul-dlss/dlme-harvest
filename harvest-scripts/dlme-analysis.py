#!/usr/bin/python
import json
from argparse import ArgumentParser
from subprocess import call

def main():
    with open('map.json') as map:
        data = json.load(map)
        try:
            for m in data:
                if m['institution'] == args.institution:
                    __import__(m['analysis'])
                    call(["python", "{}.py".format(m['analysis']), "{}".format(m['path']), "-b"])
        except:
            print("""Error possibly caused by:\n -the map.json file doesn't have the mapping info for this institution\n -a misspelling during call or in the map.json file\n -errors in the analysis script\n -no data in the output folder""")

if __name__ == "__main__":
    # CLI client options.
    parser = ArgumentParser()
    parser.add_argument(
        "institution",
        help="put the institution name (see map.json) you want analyzed here.")

    args = parser.parse_args()
    main()
