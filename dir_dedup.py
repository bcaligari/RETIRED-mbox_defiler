#!/usr/bin/env python3

# Copyright (c) 2014-2017 Brendon Caligari <caligari@cypraea.co.uk>
# This file is released under GPL v3.0

import common
import sys
import argparse
import logging
import filededup


def parse_arguments():
    """parse command line options"""
    #  Namespace(confirm=True, debug=0, dir=['tmp_data'], output='json')
    arg_parser = argparse.ArgumentParser(description="Dedup files in a directory")
    arg_parser.add_argument("dir", metavar="dir",
                            nargs=1, type=str,
                            help="directory to dedup")
    arg_parser.add_argument("-d", dest="debug",
                            type=int, choices=[0, 1, 2], default=0,
                            help="debug level")
    arg_parser.add_argument("-o", dest="output",
                            choices=["none", "json"], default="none",
                            help="output")
    arg_parser.add_argument("--yes-sure", dest="confirm",
                            action="store_true",
                            help="required safety check")
    return arg_parser.parse_args()


def main():
    """dir_dedup actual"""
    cmd_args = parse_arguments()

    if not cmd_args.confirm:
        sys.exit("Require --yes-sure parameter to know you really mean it")

    logging.basicConfig(level=common.int2loglevel(cmd_args.debug),
                        format=common.log_foremat())

    try:
        dd = filededup.FileDedup(cmd_args.dir[0])
    except OSError as err:
        logging.shutdown()
        sys.exit("Unable to process directory: {}".format(repr(err)))

    if cmd_args.output == "json":
        print(dd.report())

    logging.shutdown()


if __name__ == "__main__":
    main()
