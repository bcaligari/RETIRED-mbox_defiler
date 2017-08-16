# !/usr/bin/env python3

# Copyright (c) 2017 Brendon Caligari <caligari@cypraea.co.uk>
# This file is released under GPL v3.0

import logging


def log_format():
    return "%(module)-16s %(levelname)-8s %(message)s"


def int2loglevel(arg):
    """Convert a command line debug integer to logging level"""
    if arg == 1:
        return logging.INFO
    if arg == 2:
        return logging.DEBUG
    return logging.WARNING


if __name__ == "__main__":
    pass
