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
from io import TextIOWrapper

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


class PyFileWriter(object):
    def __init__(self, *args, **kwargs):
        self.fp = open(*args, **kwargs)

    def write_var(self, var_name, var_value, indent=""):
        if isinstance(var_value, str):
            var_value = '"{var_value}"'.format(**locals())
        self.fp.write("{indent}{var_name} = {var_value}\n".format(**locals()))

    def write(self, text, indent=""):
        if text[-1] != "\n":
            text += "\n"

        self.fp.write("{indent}{text}".format(**locals()))

    def writelines(self, *args, **kwargs):
        self.fp.writelines(*args, **kwargs)

    def __exit__(self, exc_type, exc_val, exc_tb):
        """To be used with context managers"""
        self.fp.close()

    def __enter__(self):
        """For use with context managers"""
        return self

    def __str__(self):
        return "Instance of PyFile"

    def __repr__(self):
        return "Instance of PyFile"


class CToPyFileConverter(object):
    def __init__(self, name, output_dir, base_indent=" " * 4):

        self.name = name
        self.out_dir = output_dir
        self.base_indent = base_indent

        self.code_block = dict()
        self.data = []

    def render(self):
        py_file_name = "{self.name}_gen.py".format(**locals())
        with PyFileWriter(py_file_name, 'w') as f:
            f.write("from c_file_writer import *\n\n")
            f.write_var("filename", "{self.name}_autogen.c".format(**locals()))
            f.write_var("outputpath", self.out_dir)
            f.write_var("indent", self.base_indent)
            f.write("with CFile(filename, outputpath, indent) as f:\n")

            # Write the data
            for item in self.data:
                if isinstance(item, str):
                    # Simple lines

                    if item.find(r"\n") not in [-1, len(item) - 1, 0]:
                        # new line char exists somewhere in the middle
                        # possibly as a printf statement
                        py_line = r'f.write(r"""{item}""")'.format(**locals())
                        f.write(py_line, self.base_indent)
                        f.write(r'f.write("\n")', self.base_indent)
                    else:
                        py_line = r'f.write("""{item}\n""")'.format(**locals())
                        f.write(py_line, self.base_indent)
                else:
                    logger.warning("NotImplemented for type - {}".format(type(item)))

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
    writer = CToPyFileConverter(file_name, os.path.dirname(file_path))

    for line in formatted_file:
        # logger.info(line)
        writer.add_line(line)

    writer.render()

    # For testing and comparison
    # TODO: delete this code after
    with open("test.c", 'w') as f:
        f.write("\n".join(formatted_file))


if __name__ == '__main__':
    # Set up logging
    logger = log.setup_console_logger(__name__)
    logger.setLevel(logging.INFO)

    parse_file(r'c_test.c')
