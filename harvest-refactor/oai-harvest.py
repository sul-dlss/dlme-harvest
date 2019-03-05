import errno
import helper
import os
from argparse import ArgumentParser
from sickle import Sickle
from sickle.iterator import OAIResponseIterator

def main():
    # CLI client options.
    parser = ArgumentParser()
    parser.add_argument(
        "-i",
        "--institution",
        dest="institution",
        help="add the institution and the set names to ignore to the helper.do_not_harvest dictionary")
    parser.add_argument("-m", "--metadata_prefix", dest="metadata_prefix",
                        help="add the metadata prefix if other than oai_dc")
    parser.add_argument(
        "-s",
        "--sets",
        dest="sets",
        help="add the -s flag if sets are a feature used by the data provider")
    parser.add_argument(
        "base_url",
        help="put the base url you want harvested here.")

    args = parser.parse_args()

    # Create sickle instance
    sickle = Sickle(args.base_url)

    if args.sets:
        # Get a list of all sets available
        sets = sickle.ListSets()
        for s in sets:
            if s.setSpec not in helper.get_values_if_any(
                    helper.do_not_harvest, args.institution):
                records = sickle.ListRecords(
                    metadataPrefix=args.metadata_prefix,
                    set=s.setSpec,
                    ignore_deleted=True)
                file_path = 'output/{}/data/'.format(s.setSpec)
                for record in records:
                    helper.write_records(records, file_path)

    else:
        records = sickle.ListRecords(
            metadataPrefix=args.metadata_prefix,
            ignore_deleted=True)
        print("Records created.")  # status update
        file_path = 'output/data/'
        helper.write_records(records, file_path)

if __name__ == "__main__":
    main()
