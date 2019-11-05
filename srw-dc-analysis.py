import hashlib
import sys
import pprint
from argparse import ArgumentParser
from xml.etree import ElementTree as etree
import six
import os

DC_NS = "{http://purl.org/dc/elements/1.1/}"
OAI_NS = "{http://www.openarchives.org/OAI/2.0/}"
OAI_DC = "{http://www.openarchives.org/OAI/2.0/oai_dc/}"
SRW_NS = "{http://www.loc.gov/zing/srw/}"


class RepoInvestigatorException(Exception):
    """This is our base exception class for this script."""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "%s" % (self.value,)

class Record:
    """Base class for a Dublin Core (qdc or dc) metadata record in an OAI-PMH
       Repository file."""
    def __init__(self, elem, args):
        """Create the Record class instance."""
        self.elem = elem
        self.args = args

    def get_record_id(self):
        """Find an identifier for the record, checking the OAI header."""
        try:
            dc_node = self.elem.find("{}recordData/{}dc".format(SRW_NS, OAI_DC))
            record_id = dc_node.find("{}identifier".format(DC_NS)).text
            return record_id
        except:
            raise RepoInvestigatorException("Record does not have a valid Record Identifier. Check the structure of the Harvested XML (does it have a OAI header? Are the namespaces correct?) and the XML path used here to get to the identifier.")

    def get_record_status(self):
        """Get only 'active' status OAI-PMH records."""
        return self.elem.find("{}header".format(OAI_NS)).get("status", "active")

    def get_elements(self):
        """Get all the values for a given DC element/field."""
        out = []
        try:
            elements = self.elem[1][0].findall(DC_NS + self.args.element)
            for element in elements:
                if element.text:
                    out.append(element.text.encode("utf-8").strip())

            if len(out) == 0:
                out = None

            self.elements = out
            return self.elements
        except IndexError:
            self.elements = None
            return self.elements

    def get_all_data(self):
        """Gets all the values as a list for the TSV export option."""
        out = []
        for i in self.elem[1][0]:
            if i.text:
                out.append((i.tag, i.text.encode("utf-8").strip().replace("\n", " ")))
        return out

    def get_stats(self):
        """Get the field presence stats for the default report."""
        stats = {}
        try:
            for element in self.elem[1][0]:
                stats.setdefault(element.tag, 0)
                stats[element.tag] += 1
            return stats
        except IndexError:
            return stats

    def has_element(self):
        """Return True/False if a given field is present and non-empty."""
        elements = self.elem[1][0].findall(DC_NS + self.args.element)
        for element in elements:
            if element.text:
                return True
        return False

    def get_xpath(self):
        """Get all the values for a given nested element/field."""
        out = []
        metadata = self.elem
        if metadata is not None:
            if len(metadata):
                if metadata.xpath(self.args.xpath, namespaces=namespaces):
                    for value in metadata.xpath(self.args.xpath, namespaces=namespaces):
                        if value.text:
                            out.append(value.text.encode("utf-8").strip())
                if len(out) == 0:
                    out = None
                self.elements = out
                return self.elements

    def has_xpath(self):
        """Return True/False if a given nested field is present & non-empty."""
        out = []
        present = False
        metadata = self.elem.find("{}".format(DC_NS))
        if len(metadata):
            if metadata.xpath(self.args.xpath, namespaces=namespaces):
                for value in metadata.xpath(self.args.xpath, namespaces=namespaces):
                    if value.text:
                        present = True
                        return present



def collect_stats(stats_aggregate, stats):
    """Method for generating the default field usage report."""
    #increment the record counter
    stats_aggregate["record_count"] += 1

    for field in stats:

        # get the total number of times a field occurs
        stats_aggregate["field_info"].setdefault(field, {"field_count": 0})
        stats_aggregate["field_info"][field]["field_count"] += 1

        # get average of all fields
        stats_aggregate["field_info"][field].setdefault("field_count_total", 0)
        stats_aggregate["field_info"][field]["field_count_total"] += stats[field]


def create_stats_averages(stats_aggregate):
    """Method for generating the default field usage report."""
    for field in stats_aggregate["field_info"]:
        field_count = stats_aggregate["field_info"][field]["field_count"]
        field_count_total = stats_aggregate["field_info"][field]["field_count_total"]

        field_count_total_average = (float(field_count_total) / float(stats_aggregate["record_count"]))
        stats_aggregate["field_info"][field]["field_count_total_average"] = field_count_total_average

        field_count_element_average = (float(field_count_total) / float(field_count))
        stats_aggregate["field_info"][field]["field_count_element_average"] = field_count_element_average

    return stats_aggregate


def calc_completeness(stats_averages):
    """Method for generating the default field usage report."""
    completeness = {}
    record_count = stats_averages["record_count"]
    completeness_total = 0
    wwww_total = 0
    dpla_total = 0
    collection_total = 0
    collection_field_to_count = 0

    wwww = [
        "{http://purl.org/dc/elements/1.1/}creator",       # who
        "{http://purl.org/dc/elements/1.1/}title",         # what
        "{http://purl.org/dc/elements/1.1/}identifier",    # where
        "{http://purl.org/dc/elements/1.1/}date"           # when
    ]

    dpla = [
        "{http://purl.org/dc/elements/1.1/}title",
        "{http://purl.org/dc/elements/1.1/}identifier",
        "{http://purl.org/dc/elements/1.1/}rights"
    ]

    populated_elements = len(stats_averages["field_info"])
    for element in sorted(stats_averages["field_info"]):
            element_completeness_percent = 0
            element_completeness_percent = ((stats_averages["field_info"][element]["field_count"]
                                             / float(record_count)) * 100)
            completeness_total += element_completeness_percent

            # gather collection completeness
            if element_completeness_percent > 10:
                collection_total += element_completeness_percent
                collection_field_to_count += 1
            # gather wwww completeness
            if element in wwww:
                wwww_total += element_completeness_percent
            # gather dpla completeness
            if element in dpla:
                dpla_total += element_completeness_percent

    completeness["dc_completeness"] = completeness_total / float(15)
    completeness["collection_completeness"] = collection_total / float(collection_field_to_count)
    completeness["wwww_completeness"] = wwww_total / float(len(wwww))
    completeness["dpla_completeness"] = dpla_total / float(len(dpla))
    completeness["average_completeness"] = ((completeness["dc_completeness"] +
                                             completeness["collection_completeness"] +
                                             completeness["wwww_completeness"] +
                                             completeness["dpla_completeness"]) / float(4))
    return completeness


def pretty_print_stats(stats_averages):
    """Method for generating the default field usage report."""
    record_count = stats_averages["record_count"]
    # get header length
    element_length = 0
    for element in stats_averages["field_info"]:
        if element_length < len(element):
            element_length = len(element)

    print("\n\n")
    for element in sorted(stats_averages["field_info"]):
        percent = (stats_averages["field_info"][element]["field_count"] / float(record_count)) * 100
        percentPrint = "=" * (int((percent) / 4))
        columnOne = " " * (element_length - len(element)) + element
        print("%s: |%-25s| %6s/%s | %3d%% " % (
            columnOne,
            percentPrint,
            stats_averages["field_info"][element]["field_count"],
            record_count,
            percent
        ))

    print("\n")
    completeness = calc_completeness(stats_averages)
    for i in ["dc_completeness", "collection_completeness", "wwww_completeness", "dpla_completeness", "average_completeness"]:
        print("%23s %f" % (i, completeness[i]))

def process(datafile, args, stats_aggregate, s):
    for event, elem in etree.iterparse(datafile):
        if elem.tag == SRW_NS + "record":
            r = Record(elem, args)
            record_id = r.get_record_id()

            if args.stats is False and args.present is False and args.element is not None:
                if r.get_elements() is not None:
                    for i in r.get_elements():
                        if args.id:
                            print("\t".join([record_id, i]))
                        else:
                            print(i)

            if args.stats is False and args.present is False and args.xpath is not None:
                if r.get_xpath() is not None:
                    for i in r.get_xpath():
                        if args.id:
                            print("\t".join([record_id, i]))
                        else:
                            print(i)

            if args.stats is False and args.element is not None and args.present is True:
                print("%s %s" % (record_id, r.has_element()))

            if args.stats is False and args.xpath is not None and args.present is True:
                print("%s %s" % (record_id, r.has_xpath()))

            if args.stats is True and args.element is None:
                if (s % 1000) == 0 and s != 0:
                    print("%d records processed" % s)
                s += 1
                collect_stats(stats_aggregate, r.get_stats())
            elem.clear()
    return(stats_aggregate)


def main():
    # Sets up values needed for the default field report.
    stats_aggregate = {
        "record_count": 0,
        "field_info": {}
    }
    element_stats_aggregate = {}

    # CLI client options.
    parser = ArgumentParser(usage='%(prog)s [options] data_filename.xml')
    parser.add_argument("-e", "--element", dest="element",
                        help="element to print to screen")
    parser.add_argument("-i", "--id", action="store_true", dest="id",
                        default=False, help="prepend meta_id to line")
    parser.add_argument("-s", "--stats", action="store_true", dest="stats",
                        default=False, help="only print stats for repository")
    parser.add_argument("-p", "--present", action="store_true", dest="present",
                        default=False, help="print if the field is non-empty.")
    parser.add_argument("-d", "--dump", action="store_true", dest="dump",
                        default=False, help="Dump data to tab-delimited format")
    parser.add_argument("-b", "--batch", action="store_true", dest="batch",
                        default=False, help="if the file passed is dir")
    parser.add_argument("-x", "--xpath", dest="xpath",
                        help="get value of xpath on mods:mods record")
    parser.add_argument("file", help="put the datafile you want analyzed here")

    args = parser.parse_args()

    # Returns the help text if there are no flags or a datafile present.
    if not len(sys.argv) > 0:
        parser.print_help()
        exit()

    # Sets the flow control based on the flags given in the CLI client.
    if args.element is None:
        args.stats = True

    # For record counting purposes.
    s = 0
    if args.batch:
        for dirpath, dirnames, filenames in os.walk(args.file):
            for filename in [f for f in filenames if f.endswith(".xml")]:
                filepath = os.path.join(dirpath, filename)
                output = process(filepath, args, stats_aggregate, s)

    else:
        stats_aggregate = process(args.file, args, stats_aggregate, s)


    if args.stats is True and args.element is None:
        stats_averages = create_stats_averages(stats_aggregate)
        pretty_print_stats(stats_averages)



if __name__ == "__main__":
    main()
