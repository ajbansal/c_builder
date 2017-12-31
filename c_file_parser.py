#!/usr/bin/env/python
"""
Title:
    Python script for reading a C file

Assumption:
    1. All the python packages are installed
    2. You are using python==3.5
    3. Any more assumptions <>

Description:
    1. Describe the class

Author:
    Abhijit Bansal

"""

# **************************
# region GLOBAL IMPORTS

import logging

# endregion
# **************************

# **************************
# region LOCAL IMPORTS

from c_file_writer import *
import log

# endregion
# **************************

# For logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class CFileWriter(object):
    def __init__(self, name):
        self.name = name
        self.code_block = dict()
        self.data = []

    def render(self):
        pass

    def add_line(self, value):
        self.data.append(value)

    def add_code_block(self, code_block):
        assert isinstance(code_block, CCodeBlock), \
            "Incorrect type of value passed - {}".format(type(code_block))
        self.code_block[code_block.name] = code_block
        self.data.append(code_block)


def format_file(filename):
    """
    This function parses the file into a meaningful format

    It strips out all comments, makes sure the line ends in ';'
    This is useful so that we can write a common parser for the ldf files.

    Args:
        filename: path to the ldf file

    Returns:
        tempdata(list) : list of all lines with comments stripped out
    """
    global commentBlock
    counter = 0
    tempdata = []
    # Copy the entire file into a list
    with open(filename, 'rb') as filedata:
        for line in filedata:
            line = line.strip()
            if line == b"{":
                tempdata[-1] += line.decode("utf-8")
            elif line.endswith(b"}"):
                tempdata.append(line[:-1].decode("utf-8"))
                tempdata.append("}")
            elif line == '':
                pass
            else:
                tempdata.append(line.decode("utf-8"))
            counter += 1
    return tempdata


def parse_file(file_path):

    # Format the file
    formatted_file = format_file(file_path)
    file_name, file_ext = os.path.splitext(os.path.basename(file_path))

    # Initialize python writer
    writer = CFileWriter(file_name)

    for line in formatted_file:
        # logger.info(line)
        print(line)
    with open("test.c", 'w') as f:
        f.write("\n".join(formatted_file))


if __name__ == '__main__':
    # Set up logging
    logger = log.setup_console_logger(__name__)
    logger.setLevel(logging.INFO)

    parse_file(r'c_test.c')
