#!/usr/bin/env python3

# Copyright (c) 2014-2017 Brendon Caligari <caligari@cypraea.co.uk>
# This file is released under GPL v3.0

import sys
import argparse
import re
import mailbox
import json


def parse_arguments():
    """parse command line options"""
    #  Namespace(caseless=True, mbox=['OldInbox'], output='json', regex=[['\\.jpg$'], ['\\.png']])
    arg_parser = argparse.ArgumentParser(description="List attachments in an mbox")
    arg_parser.add_argument("mbox", metavar="mbox",
                            nargs=1, type=str,
                            help="mbox format mailbox")
    arg_parser.add_argument("-r", dest="regex",
                            nargs=1, type=str, action="append",
                            help="filename regular expression[s]")
    arg_parser.add_argument("-i", dest="caseless",
                            action="store_true",
                            help="case insensitive matching")
    arg_parser.add_argument("-o", dest="output",
                            choices=["txt", "count", "json"], default="txt",
                            help="output format")
    return arg_parser.parse_args()


def validate_regex(regex_strings, caseless=False):
    """validate filename regular expressions"""
    re_flags = 0
    if caseless:
        re_flags |= re.IGNORECASE
    return [re.compile(r, flags=re_flags) for r in regex_strings]


def scan_mbox(mbox_file, regex_list):
    """scan mbox for named attachments"""
    mbox = mailbox.mbox(mbox_file, create=False)
    unique_filenames = {}
    for msg in mbox:
        for part in msg.walk():
            # TODO: only if content disposition is attachment
            att_name = part.get_filename()
            if not att_name is None:
                if any(re.search(regex, att_name) for regex in regex_list):
                    if att_name in unique_filenames:
                        unique_filenames[att_name] += 1
                    else:
                        unique_filenames[att_name] = 1
    mbox.close()
    return unique_filenames


def publish_results(filename_stats, output_format):
    """Publish attachment file match results"""
    if output_format == "count":
        print("{}".format(sum(c for c in filename_stats.values())))
    elif output_format == "json":
        print(json.dumps(filename_stats, sort_keys=True, indent=4))
    else:
        print("\n".join("{1}\t{0}".format(f, c) for f, c in sorted(filename_stats.items())))


def main():
    """mbox_list_attachment actual"""
    cmd_args = parse_arguments()

    if cmd_args.regex:
        regex_strings = [r[0] for r in cmd_args.regex]
    else:
        regex_strings = [".*"]
    try:
        regex_list = validate_regex(regex_strings, cmd_args.caseless)
    except re.error as err:
        sys.exit("Unable to parse regex: {}".format(repr(err)))

    try:
        unique_filenames = scan_mbox(cmd_args.mbox[0], regex_list)
    except mailbox.Error as err:
        sys.exit("Unable to open mbox file: {}".format(repr(err)))

    publish_results(unique_filenames, cmd_args.output)


if __name__ == "__main__":
    main()
