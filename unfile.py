#!/usr/bin/env python3

# Copyright (c) 2017 Brendon Caligari <caligari@cypraea.co.uk>
# This file is released under GPL v3.0

import hashlib
import re

class UnFile(object):
    """A binary blob of file contents and filename with no path"""

    def __init__(self, blob, name=None):
        self.blob = blob
        self._sha1sum = None
        self._size = None
        self._name = name
        self._origname = name
        self._ext = ""

    def get_name(self):
        """Returns set or makes up a filename for the blob"""
        if not self._name:
            self.cook_name()
        return self._name

    def get_origname(self):
        """Returns original name set for the blob"""
        return self._origname

    def get_size(self):
        """Return the size of the blob"""
        if not self._size:
            self._size = len(self.blob)
        return self._size

    def get_hash(self):
        """Compute a hash (sha1) for the blob"""
        if not self._sha1sum:
            self._sha1sum = hashlib.sha1(self.blob).hexdigest()
        return self._sha1sum

    def get_key(self):
        """Returns a reasonably unique hash to represent file"""
        return "{}{:08x}".format(self.get_hash(), self.get_size())

    def set_name(self, name):
        """Set a filename for blob"""
        self._name = name

    def set_ext(self, ext):
        """Set a file extension for blob"""
        self._ext = ext

    def cook_name(self):
        """Compose a unique(ish) filename for the blob"""
        self._name = "{}{}".format(self.get_key(), self._ext)
        return self._name

    def infer_ext(self, inferer=None):
        """Infer a file extension from last .* or specified function"""
        if self._name is None:
            self._ext = ""
            return
        if not inferer is None:
            self._ext = inferer(self._name)
        else:
            got_ext = re.search(r'\.[a-zA-Z0-9_]*(\.(zip|gz|bz2|xz)){0,1}$', self._name)
            if got_ext:
                self._ext = got_ext.group()

    def sanitise_name(self, sanitiser=None):
        """Sanitise a name based on presets or specified function"""
        if not sanitiser is None:
            self._name = sanitiser(self._name)
        else:
            self._name = re.sub(r'^[/.\s]*', '', self._name)    # garbage in front
            self._name = re.sub(r'[/.\s]*$', '', self._name)    # garbage at back
            self._name = re.sub(r'[\s]+', ' ', self._name)      # conmpress white space
            self._name = re.sub(r'[?*\\]', '_', self._name)     # bad stuff

if __name__ == "__main__":
    pass
