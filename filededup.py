#!/usr/bin/env python3

# Copyright (c) 2017 Brendon Caligari <caligari@cypraea.co.uk>
# This file is released under GPL v3.0

import logging
import pathlib
import unfile
import json

class FileDedup(object):
    """Dedup existing files in a directory and add more unique files.

    The directory is first scanned and duplicates removed.  More unique
    files can then be added.

    Multiple requests to FileDedup("some_directory") return a reference to
    the same FileDedup object.

    Logger levels:
        info     - dedup activity
        debug    - displays some internals
    """

    class FileName(object):
        """FileName on disk may have been sanitised or have duplicates"""

        def __init__(self, on_disk_name):
            self.on_disk_name = on_disk_name
            self.original_name = None
            self.duplicate_names = set()

    __caches = {}

    def __new__(cls, dirname):
        dirname_actual = str(pathlib.Path(dirname).resolve())
        if not dirname_actual in FileDedup.__caches:
            FileDedup.__caches[dirname_actual] = super().__new__(cls)
        return FileDedup.__caches[dirname_actual]

    def __init__(self, dirname):
        logging.debug("Initialised FileDedup for '{}'".format(dirname))
        if dirname[-1] == "/":
            self._dir = dirname
        else:
            self._dir = dirname + "/"
        self._file_cache = {}                   # key = md5sum.size, value = FileName
        self._read_dedup_dir()

    def _read_dedup_dir(self):
        """Scan, catalog, and dedup directory"""
        logging.debug("Scanning files already in directory")
        scan_dir = pathlib.Path(self._dir)
        all_files = [f for f in scan_dir.iterdir() if f.is_file()]
        for file_found in all_files:            # type(file_found) == pathlib.Path
            if file_found.is_symlink():         # we don't want symlinks
                file_found.unlink()
                logging.info("Unlinked symlink '{}'".format(file_found))
                continue
            uf = unfile.UnFile(file_found.read_bytes(), file_found.parts[-1])
            if uf.get_size() == 0:
                file_found.unlink()
                logging.info("Unlinked zero sized regular file '{}'".format(file_found))
                continue
            if self._is_cached(uf.get_key()):
                self._record_dup(uf.get_key(), uf.get_name())
                file_found.unlink()
                logging.info("Unlinked duplicate regular file '{}'".format(file_found))
            else:
                self._record_file(uf.get_key(), uf.get_name(), uf.get_origname())
                logging.info("Leaving unique regular file '{}'".format(file_found))
        logging.debug("Finished processing pre-existing files")

    def _commit_file(self, pathspec, blob):
        """Commit a binary blob to disk as a file"""
        pathlib.Path(pathspec).write_bytes(blob)

    def _record_file(self, key, filename, origname):
        """Record in _cache that a unique file is on disk"""
        self._file_cache[key] = self.FileName(filename)
        if filename != origname:
            self._file_cache[key].original_name = origname

    def _record_dup(self, key, filename):
        """Record in _cache that a duplicate has been detected"""
        self._file_cache[key].duplicate_names.add(filename)

    def _is_cached(self, key):
        """Check if a binary blob already exists as a file"""
        return key in self._file_cache

    def add_file(self, uf):
        """Add an Unfile to the dedup directory"""
        if self._is_cached(uf.get_key()):
            self._record_dup(uf.get_key(), uf.get_name())
            logging.info("Skipped duplicate of on disk '{}'".format(uf.get_name()))
        else:
            uf.sanitise_name()                  # We can't trust filenames coming from wherever
            if uf.get_name() != uf.get_origname():
                logging.info("Sanitising file name of '{}'".format(uf.get_origname()))
            if pathlib.Path("{}/{}".format(self._dir, uf.get_name())).exists():
                logging.info("Renaming unique file with name collision for '{}'".format(uf.get_name()))
                uf.infer_ext()
                uf.cook_name()
            self._commit_file("{}/{}".format(self._dir, uf.get_name()), uf.blob)
            self._record_file(uf.get_key(), uf.get_name(), uf.get_origname())
            logging.info("Adding unique file '{}'".format(uf.get_name()))

    def report(self):
        """Reports on ondisk files with original and duplicate filenames"""
        struct = dict()
        for f in self._file_cache.keys():
            struct[self._file_cache[f].on_disk_name] = {
                "original" : self._file_cache[f].original_name,
                "duplicates" : list(self._file_cache[f].duplicate_names)
            }
        return json.dumps(struct, sort_keys=True, indent=4)

if __name__ == "__main__":
    pass
