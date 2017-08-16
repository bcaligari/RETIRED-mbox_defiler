#!/usr/bin/env python3

# Copyright (c) 2014-2017 Brendon Caligari <caligari@cypraea.co.uk>
# This file is released under GPL v3.0

import common
import sys
import argparse
import logging
import mailbox
import filededup
import unfile


def parse_arguments():
    """parse command line options"""
    #  Namespace(debug=0, dir=['tmp_data'], mbox=['OldInbox'], output='json')
    arg_parser = argparse.ArgumentParser(description="Extract attachments from an mbox to a directory")
    arg_parser.add_argument("mbox", metavar="mbox",
                            nargs=1, type=str,
                            help="mbox to defile")
    arg_parser.add_argument("dir", metavar="dir",
                            nargs=1, type=str,
                            help="dedup directory to save to")
    arg_parser.add_argument("-d", dest="debug",
                            type=int, choices=[0, 1, 2], default=0,
                            help="debug level")
    arg_parser.add_argument("-o", dest="output",
                            choices=["none", "json"], default="none",
                            help="output format")
    return arg_parser.parse_args()


def extract_attachments(mbox_file, dedup_dir):
    """scan mbox for named attachments"""
    logging.debug("Scanning mbox for attachments '{}'".format(mbox_file))
    mbox = mailbox.mbox(mbox_file, create=False)
    unique_filenames = {}
    for msg in mbox:
        for part in msg.walk():
            # TODO: only if content disposition is attachment
            blob = part.get_payload(decode=True)
            att_name = part.get_filename()
            if blob and att_name:
                logging.debug("Found part of size {} with name '{}'".format(len(blob), att_name))
                uf = unfile.UnFile(blob, att_name)
                dedup_dir.add_file(uf)
    mbox.close()
    logging.debug("Finished processing mbox")


def main():
    """mbox_defiler actual"""
    cmd_args = parse_arguments()

    logging.basicConfig(level=common.int2loglevel(cmd_args.debug),
                        format=common.log_format())

    try:
        dd = filededup.FileDedup(cmd_args.dir[0])
    except OSError as err:
        logging.shutdown()
        sys.exit("Unable to process directory: {}".format(repr(err)))

    try:
        extract_attachments(cmd_args.mbox[0], dd)
    except mailbox.Error as err:
        logging.shutdown()
        sys.exit("Unable to process mailbox: {}".format(repr(err)))

    if cmd_args.output == "json":
        print(dd.report())

    logging.shutdown()


if __name__ == "__main__":
    main()
