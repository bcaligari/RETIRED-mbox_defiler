# mbox_defiler

Tools to list, extract, and dedup all attachments from an mbox file.

* ```mbox_defiler.py``` - Extract attachments from an mbox mailbox file to a
directory.
* ```mbox_list_files.py``` - List filenames from an mbox mailbox file.
* ```dir_dedup.py``` - Dedup the files in a directory.

## mbox_defiler.py

**mbox_defiler.py** extracts all attachments found in emails within an mbox
format mailbox and stores them to a directory.  Duplicate files are identified
(based on a sha1 and file size hash) and stored just once.  The target directory
is scanned for duplicates, and any duplicates removed, before mailbox
attachments are added.  Attachment filenames are sanity checked for [some]
illegal characters and filename conflicts are resolved by renaming the
contenders.

By default no output is generated.  A json summary of all filenames found, along
with original filenames and duplicates, can be requested at the command line as
is logging verbosity.

### Usage

```{text}
usage: mbox_defiler.py [-h] [-d {0,1,2}] [-o {none,json}] mbox dir

Extract attachments from an mbox to a directory

positional arguments:
  mbox            mbox to defile
  dir             dedup directory to save to

optional arguments:
  -h, --help      show this help message and exit
  -d {0,1,2}      debug level
  -o {none,json}  output format
```

### Examples:

```{text}
./mbox_defiler.py -o json /tmp/OldInboxClearance tmp_data/
```

```{text}
./mbox_defiler.py -o json /tmp/OldInboxClearance tmp_data/
```

## mbox_list_files.py

**mbox_list_files.py** lists the filenames of attachemts identified within an
mbox format mailbox file along with the number of times the filename was
encountered.  Output defaults to plain text but can be overridden as json or
suppressed to a sum total.

Searching can be restricted using one or more regular expressions.

### Usage

```{text}
usage: mbox_list_files.py [-h] [-r REGEX] [-i] [-o {txt,count,json}] mbox

List attachments in an mbox

positional arguments:
  mbox                 mbox format mailbox

optional arguments:
  -h, --help           show this help message and exit
  -r REGEX             filename regular expression[s]
  -i                   case insensitive matching
  -o {txt,count,json}  output format
```

### Examples

```{text}
./mbox_list_files.py -r '^image02\.jpg$' OldInbox
```

```{text}
./mbox_list_files.py -o json OldInbox
```

```{text}
./mbox_list_files.py -i -r '\.jpg$' -r '\.*png$' OldInbox
```

## dir_dedup.py

**dir_dedup.py** scans files in specified directory and removes any duplicates
or symbolic links.

By default no output is generated.  A json summary of all filenames retained,
along with the filenames of removed duplicates, can be requested at the command
line as is logging verbosity.

### Usage

```{text}
usage: dir_dedup.py [-h] [-d {0,1,2}] [-o {none,json}] [--yes-sure] dir

Dedup files in a directory

positional arguments:
  dir             directory to dedup

optional arguments:
  -h, --help      show this help message and exit
  -d {0,1,2}      debug level
  -o {none,json}  output
  --yes-sure      required safety check
```

### Examples

```{text}
./dir_dedup.py --yes-sure tmp_data/
```

## Notes

* **mbox_defiler** grew out of an earlier, simple, and perfectly functional
  script into more of a toy project.
* Requires Python 3.5+ because of some standard library features.
* To evaluate ```part.is_attachment()``` in future.

