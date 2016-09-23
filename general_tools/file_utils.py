# -*- coding: utf8 -*-
#
#  Copyright (c) 2016 unfoldingWord
#  http://creativecommons.org/licenses/MIT/
#  See LICENSE file for details.
#
#  Contributors:
#  Phil Hopper <phillip_hopper@wycliffeassociates.org>

from __future__ import unicode_literals
import codecs
import json
import os
import zipfile
import sys

# we need this to check for string versus object
PY3 = sys.version_info[0] == 3

if PY3:
    string_types = str,
else:
    # noinspection PyCompatibility
    string_types = basestring,


def unzip(source_file, destination_dir):
    """
    Unzips <source_file> into <destination_dir>.
    :param str|unicode source_file: The name of the file to read
    :param str|unicode destination_dir: The name of the directory to write the unzipped files
    """
    with zipfile.ZipFile(source_file) as zf:
        zf.extractall(destination_dir)

def add_file_to_zip(zip_file, filename, arcname=None, compress_type=None):
    """
    Zip <filename> into <zip_file> as <arcname>.
    :param str|unicode zip_file: The file name of the zip file
    :param str|unicode filename: The name of the file to add, including the path
    :param str|unicode archname: The new name, with directories, of the file, the same as filename if not given
    """
    with zipfile.ZipFile(zip_file, 'a') as zf:
        zf.write(filename, arcname, compress_type)

def make_dir(dir_name, linux_mode=0o755, error_if_not_writable=False):
    """
    Creates a directory, if it doesn't exist already. If the directory does exist, and <error_if_not_writable> is True,
    the directory will be checked for writability.
    :param str|unicode dir_name: The name of the directory to create
    :param int linux_mode: The mode/permissions to set for the new directory expressed as an octal integer (ex. 0o755)
    :param bool error_if_not_writable: The name of the file to read
    """
    if not os.path.exists(dir_name):
        os.makedirs(dir_name, linux_mode)
    elif error_if_not_writable:
        if not os.access(dir_name, os.R_OK | os.W_OK | os.X_OK):
            raise IOError('Directory {0} is not writable.'.format(dir_name))


def load_json_object(file_name, default=None):
    """
    Deserialized <file_name> into a Python object
    :param str|unicode file_name: The name of the file to read
    :param default: The value to return if the file is not found
    """
    if not os.path.isfile(file_name):
        return default

    # use utf-8-sig in case the file has a Byte Order Mark
    with codecs.open(file_name, 'r', 'utf-8-sig') as in_file:
        # read the text from the file
        content = in_file.read()

    # convert Windows line endings to Linux line endings
    content = content.replace('\r\n', '\n')

    # return a deserialized object
    return json.loads(content)


def write_file(file_name, file_contents, indent=None):
    """
    Writes the <file_contents> to <file_name>. If <file_contents> is not a string, it is serialized as JSON.
    :param str|unicode file_name: The name of the file to write
    :param str|unicode|object file_contents: The string to write or the object to serialize
    :param int indent: Specify a value if you want the output formatted to be more easily readable
    """
    # make sure the directory exists
    make_dir(os.path.dirname(file_name))

    if isinstance(file_contents, string_types):
        text_to_write = file_contents
    else:
        text_to_write = json.dumps(file_contents, sort_keys=True, indent=indent)

    with codecs.open(file_name, 'w', encoding='utf-8') as out_file:
        out_file.write(text_to_write)


if __name__ == '__main__':
    pass
