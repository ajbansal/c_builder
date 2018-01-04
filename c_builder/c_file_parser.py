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
import re

# endregion
# **************************

# **************************
# region LOCAL IMPORTS

from c_builder.c_file_writer import *
import log

# endregion
# **************************

# For logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class CodeBlockNotFound(Exception):
    pass


class PyFileWriter(object):
    def __init__(self, *args, **kwargs):
        self.fp = open(*args, **kwargs)

    def write_var(self, var_name, var_value, indent=""):
        if isinstance(var_value, str):
            var_value = '"{var_value}"'.format(**locals())
        self.fp.write("{indent}{var_name} = {var_value}\n".format(**locals()))

    def write_code_block(self, code_block, base, indent=" " * 4, level=1):
        self.write("\n")
        class_type = code_block['type']
        class_args = ", ".join(code_block['args'] + ["base={base}".format(**locals())])
        code_block_name = "Block_level_{level}".format(**locals())
        self.write("""{indent}with {class_type}({class_args}) as {code_block_name}:""".format(**locals()))
        indent += " " * 4
        for line in code_block['lines']:
            if isinstance(line, str):
                line = line.replace(";", "")
                self.write("""{indent}{code_block_name}.add_code_line(r'{line}')""".format(**locals()))
            else:
                self.write_code_block(line, base=code_block_name, indent=indent, level=level+1)
        # if instance var is defined
        instance_var = code_block['instance_var']
        if instance_var:
            self.write("""{indent}{code_block_name}.add_instance_var('{instance_var}')""".format(**locals()))

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
            f.write("from c_builder.c_file_writer import *\n\n")
            f.write_var("filename", "{self.name}_autogen.c".format(**locals()))
            f.write_var("outputpath", self.out_dir)
            f.write_var("indent", self.base_indent)
            f.write("\n")
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
                    # For code blocks
                    f.write(r'f.write("\n")', self.base_indent)
                    f.write_code_block(item, base='f')

    def add_line(self, value):
        self.data.append(value)

    def add_code_block(self, code_block):
        assert isinstance(code_block, dict), \
            "Incorrect type of value passed - {}".format(type(code_block))
        # self.code_block[code_block[type]] = code_block
        self.data.append(code_block)


def format_file(filename):
    """
    This function parses the file into a meaningful format

    This is useful so that we can write a common parser for the C files.

    Args:
        filename: path to the C file

    Returns:
        tempdata(list) : list of all lines with comments stripped out
    """

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
            elif line == b'':
                pass
            else:
                tempdata.append(line.decode("utf-8"))
            counter += 1
    return tempdata


def make_code_block(text):
    """
    To make appropriate code block

    Args:
        text (str): The actual text without the trailing'{'
    """
    text = text.strip()
    text_lower = text.lower()

    # TODO make it more robust so doesnt trigger for function names
    class_mapping = {'if': 'CIf',
                     'struct': 'CStruct',
                     'union': 'CUnion',
                     'switch': 'CSwitchBlockC',
                     'else': 'CElse',
                     'for': 'CFor'}

    func_ret_types = {'void', 'int', 'float', 'char', 'double'}

    # First check if its not a regular function then add other types
    if any(text.find(i) == 0 for i in func_ret_types):
        code_block_dict = {'type': 'CCodeBlock',
                           'args': ['"{}"'.format(text)],
                           'lines': [],
                           'instance_var': []}
        return code_block_dict
    else:
        for item, class_type in class_mapping.items():
            args = []
            if item in text:
                if 'typedef' in text:
                    args = ["typedef=True"]
                    pattern = re.compile(re.escape('typedef'), re.IGNORECASE)
                    text = pattern.sub('', text).strip()

                if class_type in ['CIf', 'CFor', 'CStruct', 'CUnion']:
                    if class_type == 'CIf':
                        pattern = re.compile(re.escape('if'), re.IGNORECASE)
                    elif class_type == 'CStruct':
                        pattern = re.compile(re.escape('struct'), re.IGNORECASE)
                    elif class_type == 'CUnion':
                        pattern = re.compile(re.escape('union'), re.IGNORECASE)
                    else:
                        pattern = re.compile(re.escape('for'), re.IGNORECASE)
                    text = pattern.sub('', text).strip()
                    code_block_dict = {'type': class_type,
                                       'args': ['"{text}"'.format(**locals())] + args,
                                       'lines': [],
                                       'instance_var': []}
                else:
                    code_block_dict = {'type': class_type,
                                       'args': [],
                                       'lines': [],
                                       'instance_var': []}
                return code_block_dict
        else:
            raise CodeBlockNotFound("No suitable code block found for {text}".format(**locals()))


def parse_file(file_path):
    """
    To parse C file and make a rough template for writing C Code

    Args:
        file_path (str): Path to the C file
    """
    # Format the file
    formatted_file = format_file(file_path)
    file_name, file_ext = os.path.splitext(os.path.basename(file_path))

    # Initialize python writer
    converter = CToPyFileConverter(file_name, os.path.dirname(file_path))

    code_block_lineage = []

    for line in formatted_file:
        # logger.info(line)
        # To start a new or nested code block
        if line.endswith("{"):
            code_block_lineage.append(make_code_block(line[:-1]))
        # To end a code block
        elif "}" in line and "=" not in line and code_block_lineage:
            instance_var = line.replace("}", "")

            # Add instance var
            if instance_var:
                code_block_lineage[-1]['instance_var'] = instance_var

            # Add base code block
            if len(code_block_lineage) == 1:
                converter.add_code_block(code_block_lineage.pop())
            else:
                # Nested code block
                code_block_lineage[-2]['lines'].append(code_block_lineage.pop())
        else:
            # If code block exist add it to last code block
            if code_block_lineage:
                code_block_lineage[-1]['lines'].append(line)
            else:
                # Else add it to the base
                converter.add_line(line)

    converter.render()


if __name__ == '__main__':
    # Set up logging
    logger = log.setup_console_logger(__name__)
    logger.setLevel(logging.INFO)

    parse_file(r'..\c_test.c')
