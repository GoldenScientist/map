import logging
import re
import sys

logging.basicConfig(filename="mappy.log",level=logging.INFO,format='%(levelname)s - %(name)s - %(asctime)s: %(message)s')

class Agg_viewmode():
    def __init__(self, mode_name, zoom):
        logging.info("Create new aggregation for viewmode {}".format(mode_name))
        self.mode_name = mode_name
        self.count = 1
        self.zooms = {zoom}

    def __str__(self):
        return self.mode_name + "\t" + str(self.count) + "\t" + ','.join(map(str, self.zooms))

    def add_zoom(self, zoom):
        logging.info("Add zoom value {} for aggregation of {}".format(zoom, self.mode_name))
        self.count += 1
        self.zooms.add(zoom)


def parse_line(line):
    logging.info("Parsing line : {}".format(line))
    match = re.search('/map/1\.0/slab/([^/]*)/256/([^/]*)', line)
    mode_name, zoom = match.groups()
    return mode_name, zoom

def write_aggregations(aggregations):
    for aggregation in aggregations:
        print(aggregation)

def aggregate(logs):
    aggregations = []

    for line in logs:
        try:
            mode_name, zoom = parse_line(line)
            logging.info("mode_name : {}, zoom : {}".format(mode_name, zoom))

            if aggregations and mode_name == aggregations[-1].mode_name:
                aggregations[-1].add_zoom(zoom)
            else:
                agg_viewmode = Agg_viewmode(mode_name, zoom)
                aggregations.append(agg_viewmode)

        except Exception as e:
            logging.error("Error parsing line {}".format(line))

    return aggregations


if __name__ == "__main__":
    remove_endline = lambda x : x.rstrip('\n')

    if len(sys.argv) == 2:
        filename = sys.argv[1]
        logging.info("Reading data from file {}".format(filename))
        with open(filename, "r") as input_file:
            file_content = map(remove_endline, input_file.readlines())
    else:
        logging.info("Reading data from stdin")
        file_content = map(remove_endline, sys.stdin.readlines())

    aggregations = aggregate(file_content)

    write_aggregations(aggregations)