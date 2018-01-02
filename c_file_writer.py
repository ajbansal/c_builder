#!/usr/bin/env/python
"""
Title:
    Python script for writing C files

Assumption:
    1. All the python packages are installed
    2. You are using python==3.5
    3. Any more assumptions <>

Description:
    1. Describe the class

Author:
    Abhijit Bansal

"""

import os
import logging

# For logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class CCodeBlock(object):
    def __init__(self, header, start_indent="", base_indent=" " * 4, block_segmenter=('{', '}'),
                 comment_block=None, base=None, name="", block_type=""):
        """
        A C code block for code blocks such as loops, switch case comments, if-else etc

        Args:
            base (Union[CCodeBlock, CFile])): The base to which the block is nested to
            block_type (str): For type of code block, for stats for future
            name (str): Name of the block, for stats purposes, for future, Differs from header which also includes
                        things like typedef, if/else etc
            comment_block (CCommentBlockC): Comment block to go before the header
            block_segmenter (Tuple): A tuple of two elements for showing how the block starts and end after the header
            base_indent (str): The base indent of the block, used by all nested lines/blocks overwritten by base params
            start_indent (str): Starting indent of the header overwritten by base params
            header (str): The header, like function nae, if else condition
        """
        # For future stats purposes
        self.name = name
        self.type = block_type

        self.data = []
        self.start_indent = start_indent
        self.base_indent = base_indent
        self.block_segmenter = block_segmenter

        # For comment block that goes before the header
        self.comment_block = comment_block

        # For nested code blocks
        self.code_blocks = []
        self.base_code_block = base

        # Overwrite indents from the base block
        if isinstance(self.base_code_block, CCodeBlock):
            self.start_indent = self.base_code_block.start_indent + self.base_code_block.base_indent
            self.base_indent = self.base_code_block.base_indent
        if isinstance(self.base_code_block, CFile):
            self.start_indent = self.base_code_block.start_indent
            self.base_indent = self.base_code_block.indent

        if header:
            self.data.append("{}{}\n".format(self.start_indent, header))
        if block_segmenter[0]:
            self.data.append("{i}{p[0]}\n".format(i=self.start_indent, p=block_segmenter))
        if isinstance(self, CFile):
            self.total_indent = ""
        else:
            self.total_indent = self.start_indent + self.base_indent

    def add_code_block(self, code_block):
        """
        To add a code block

        Args:
            code_block (CCodeBlock): the nested codeblock
        """
        assert isinstance(code_block, CCodeBlock), "Incorrect data type given for code block"
        self.code_blocks.append(code_block)
        self.data = self.data + code_block.data

    def validate(self):
        # TODO: To add code to validate name and other standards
        pass

    def add_comment_block(self, comment_block):
        """
        To add a comment block to the code block

        Args:
            comment_block (CCommentBlockC): The comment block that precedes the header
        """
        assert isinstance(comment_block, CCommentBlockC), "Incorrect data type given for comment block"
        self.comment_block = comment_block

    def add_code_line(self, line, comment="", comment_char="//", termination=';', new_lines=1):
        """
        To add a code line to the code block

        Args:
            new_lines (int): Number of new lines to be added after the line
            termination (str): Termination character for the code line
            comment_char (str): Comment tag
            comment (str): Comment for the line if any
            line (str): The code line to be added
        """
        formatted_line = self._line(line, comment=comment, comment_char=comment_char,
                                    new_lines=new_lines, termination=termination)
        self.data.append("{}{}".format(self.total_indent, formatted_line))

    def add_comment_line(self, comment="", comment_char="//", new_lines=1):
        """
        To add a code line to the code block

        Args:
            new_lines (int): Number of new lines to be added after the line
            comment_char (str): Comment tag
            comment (str): Comment for the line if any
        """
        formatted_line = self._line("", comment=comment, comment_char=comment_char + " ",
                                    new_lines=new_lines, termination="")
        self.data.append("{}{}".format(self.total_indent, formatted_line))

    def add_spec_comment_line(self, comment="", new_lines=1):
        """
        To add a comment line to the code block with /*

        Args:
            new_lines (int): Number of new lines to be added after the line
            comment (str): Comment for the line if any
        """
        formatted_line = self._line("", comment=comment, comment_char="/* ", new_lines=new_lines, termination="")
        if formatted_line[-1] == "\n":
            formatted_line = formatted_line[:-1]
        self.data.append("{}{} */\n".format(self.total_indent, formatted_line))

    def add_block_comment_line(self, comment="", new_lines=1):
        """
        To add a code line to the code block

        Args:
            new_lines (int): Number of new lines to be added after the line
            comment (str): Comment for the line if any
        """
        formatted_line = "/* {c} */{n}".format(c=comment, n="\n" * new_lines)
        self.data.append("{}{}".format(self.total_indent, formatted_line))

    def add_blank_line(self, number_of_lines=1):
        """
        To add blank lines to the code block

        Args:
            number_of_lines (int): Number of blank lines to add
        """
        self.data.append("\n" * number_of_lines)

    def add_block(self, code_block):
        """
        To add a new block code data to this one

        Args:
            code_block (Union[CCodeBlock, CCommentBlock]): To add block code data to this code
        """
        assert isinstance(code_block, (CCodeBlock, CCommentBlockC)), "Incorrect data type given for block"
        self.data += code_block.data

    def write(self, line):
        """To keep legacy code"""
        self.data.append(line)

    def close(self):
        """To do the closing steps for the code block"""
        # add the block segmenter
        if isinstance(self, CCommentBlockC):
            if self.data[-2] != self.block_segmenter[1]:
                self.data.append("{}{}".format(self.start_indent, self.block_segmenter[1]))
        else:
            if self.data[-1] != self.block_segmenter[1]:
                self.data.append("{}{}".format(self.start_indent, self.block_segmenter[1]))

        # If the object has comment block, ensure we have closed it
        if getattr(self, "comment_block", None):
            self.comment_block.close()
            self.data = self.comment_block.data + self.data

        self.data.append("\n\n")

    @staticmethod
    def _line(line, comment="", termination=";", comment_char="//", new_lines=1):
        """
        To format a line

        Args:
            new_lines (int): Number of new lines to be added after the line
            termination (str): Termination character for the code line
            comment_char (str): Comment tag
            comment (str): Comment for the line if any
            line (str): The code line to be added
        """
        comment_line = ""
        main_line = line
        main_line = main_line + termination if main_line else main_line

        # Only add comment if given
        if comment:
            if main_line:
                comment_line = "    {}{}".format(comment_char, comment)
            else:
                comment_line = "{}{}".format(comment_char, comment)
        main_line += comment_line

        return main_line + ("\n" * new_lines)

    def __enter__(self):
        """For use with context managers"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """For use with context managers"""
        # Remember to close the block
        self.close()
        # If base code exists add this block that base code block
        if self.base_code_block:
            self.base_code_block.add_block(self)

    def __str__(self):
        class_type = type(self)
        if self.name:
            return "{self.name}({class_type})".format(**locals())
        else:
            prefix = self.data[0].replace("\n", "")
            return "{prefix}({class_type})".format(**locals())

    def __repr__(self):
        return self.__str__()


class CSwitchBlockC(CCodeBlock):
    def __init__(self, switch_var, base=None):
        """
        Class to implement switch block

        Args:
            base (CCodeBlock): The base block for the switch
            switch_var (str): Name of the switch variable
        """
        header = "switch ({switch_var})".format(**locals())
        super(CSwitchBlockC, self).__init__(header, base=base)


class CIf(CCodeBlock):
    def __init__(self, if_var, base=None):
        """
        Class to implement if block

        Args:
            base (CCodeBlock): The base block for the if block
            if_var (str): Name of the switch variable
        """
        header = "if ({if_var})".format(**locals())
        super(CIf, self).__init__(header, base=base)


class CElse(CCodeBlock):
    def __init__(self, base=None):
        """
        Class to implement else block

        Args:
            base (CCodeBlock): The base block for the else block
        """
        header = "else"
        super(CElse, self).__init__(header, base=base)


class CFor(CCodeBlock):
    def __init__(self, for_var, base=None):
        """
        Class to implement for block

        Args:
            base (CCodeBlock): The base block for the switch
            if_var (str): Name of the switch variable
        """
        header = "for ({for_var})".format(**locals())
        super(CFor, self).__init__(header, base=base)


class CTypedefEnum(CCodeBlock):
    def __init__(self, enum_name="", base=None):
        """
        Class to implement switch block

        Args:
            base (CCodeBlock): The base block for the switch
            enum_name (str): Name of the enum variable
        """
        header = "typedef enum"
        segmenter = ("{", "}} {enum_name};".format(**locals()))
        super(CTypedefEnum, self).__init__(header, base=base, block_segmenter=segmenter)

    def add_enums(self, enum_dict):
        """
        To add enums from a dict

        Args:
            enum_dict (dict): Enum dict with string name as value and numerical value as the key
        """
        for key in sorted(enum_dict.keys()):
            value = enum_dict[key]
            self.add_enum(key, value)

    def add_enum(self, key, value, comment=""):
        """
        To add single enum

        Args:
            comment (str): Comment for enum if any
            value (str): The string name of the value
            key (str): The numerical value as key
        """
        self.add_code_line("{value} = {key}".format(**locals()), termination=",", comment=comment)

    def add_instance_var(self, text):
        """can be any string including any directive for compiler"""
        if text:
            text = text.strip()
            block_start, block_end = self.block_segmenter
            block_end = block_end.replace(";", "")
            text = text if text[-1] == ';' else text + " ;"
            self.block_segmenter = block_start, "{block_end} {text}".format(**locals())


class CSwitchCase(CCodeBlock):
    def __init__(self, case_var, base=None, block_segmenter=("", "{}break;".format(" " * 4))):
        """
        Class to implement switch case inside a switch block

        Args:
            block_segmenter (tuple): The block segmenter, already populate by default
            base (CSwitchCase): The base block for the switch
            case_var (str): Name of the case variable
        """
        header = "case {case_var}:".format(**locals()) if case_var != 'default' else 'default:'
        super(CSwitchCase, self).__init__(header, block_segmenter=block_segmenter, base=base)


class CCommentBlockC(CCodeBlock):
    def __init__(self, start_indent="", block_segmenter=('/*', '*/'), base=None):
        """
        To add block comments

        Args:
            block_segmenter (tuple): The segmenter for the block
            base (CCodeBlock): The parent code block
            start_indent (str): The start indent of the block
        """
        self.base_code_block = base
        self.start_indent = start_indent

        super(CCommentBlockC, self).__init__("", self.start_indent, base_indent="", block_segmenter=block_segmenter, base=base)

    def add_line(self, line):
        """
        To add a new comment line to the block

        Args:
            line (str): To add the line to the comment block
        """
        self.data.append("{} * {}\n".format(self.start_indent, line))


class CFile(CCodeBlock):
    def __init__(self, name, directory, base_indent, header_guard=False, mode='w'):
        """
        To write a new C or any type file

        Args:
            header_guard (bool): Add header guard
            mode (str): The mode with which the file to be opened
            base_indent (str): The base indent for the file, can be used for nested blocks
            directory (str): The path where the file should go
            name (str): Name of the file with the extension
        """
        self.name = name
        self.dir = directory
        self.indent = base_indent
        self.mode = mode
        self.data = []
        self.header_guard = header_guard
        self.file_path = os.path.join(self.dir, self.name)
        super(CFile, self).__init__(header="", start_indent="", base_indent="", block_segmenter=("", ""),
                                    block_type="main_file", name=name, base=None)

    def render(self):
        """
        To produce the file
        """
        data = self.data
        if self.header_guard:
            name = self.name.replace(" ", "_")
            name = name.upper()
            data.insert(0, "# ifndef {name}\n".format(**locals()))
            data.insert(1, "# define {name}\n\n".format(**locals()))
            data.append('#endif // For header guard - {name}\n'.format(**locals()))
        with open(self.file_path, self.mode) as f:

            f.writelines(self.data)
        logger.info("Finished generating file - {self.file_path}".format(**locals()))

    def add_include_line(self, file_name, comment="", comment_char="//", new_lines=1):
        """
        To add include file lines to the code block

        Args:
            comment_char (str): Comment tag to be used
            new_lines (int): Number of new lines after this one
            comment (str): The comment for the include line
            file_name (str): The name of the include file with its tags like <stdio.h> "user_def.h"
        """
        formatted_line = self._line("#include {}".format(file_name), comment=comment, termination="",
                                    comment_char=comment_char, new_lines=new_lines)
        self.data.append("{}{}".format(self.total_indent, formatted_line))

    def add_define_line(self, define, comment="", comment_char="//", new_lines=1):
        """
        To add defines to the code block

        Args:
            comment_char (str): Comment tag to be used
            new_lines (int): Number of new lines after this one
            comment (str): The comment for the include line
            define (str): The value of the define
        """
        formatted_line = self._line("#define {}".format(define), comment=comment, termination="",
                                    comment_char=comment_char, new_lines=new_lines)
        self.data.append("{}{}".format(self.total_indent, formatted_line))

    def __exit__(self, exc_type, exc_val, exc_tb):
        """To be used with context managers"""
        self.render()


class CUnion(CCodeBlock):
    def __init__(self, union_var="", typedef=False, base=None):
        """
        Class to implement union

        Args:
            typedef (bool): To enable adding typedef in the name
            base (CSwitchCase): The base block for the switch
            union_var (str): Name of the case variable
        """
        if typedef:
            header = "typedef union"
        else:
            header = "union"

        block_segmenter = ("{", "}} {union_var};".format(**locals()))
        super(CUnion, self).__init__(header, block_segmenter=block_segmenter, base=base)

    def add_instance_var(self, text):
        """can be any string including any directive for compiler"""
        if text:
            text = text.strip()
            block_start, block_end = self.block_segmenter
            block_end = block_end.replace(";", "")
            text = text if text[-1] == ';' else text + " ;"
            self.block_segmenter = block_start, "{block_end} {text}".format(**locals())


class CStruct(CCodeBlock):
    def __init__(self, struct_var="", typedef=False, base=None):
        """
        Class to implement struct

        Args:
            base (CSwitchCase): The base block for the switch
            struct_var (str): Name of the case variable
        """
        if typedef:
            header = "typedef struct"
        else:
            header = "struct"

        block_segmenter = ("{", "}} {struct_var};".format(**locals()))
        super(CStruct, self).__init__(header, block_segmenter=block_segmenter, base=base)

    def add_element(self, var_type, name, length=None, comment=""):
        """
        Add element to the struct

        Args:
            comment (str): Optional
            length (UNION(str, int)): Can be integer or string indicating length of var
            name (str): Name of the variable
            var_type (str): The type of variable like UINT64_t
        """
        if length:
            self.add_code_line("{var_type} {name}: {length}".format(**locals()), comment=comment)
        else:
            self.add_code_line("{var_type} {name}".format(**locals()), comment=comment)

    def add_instance_var(self, text):
        """can be any string including any directive for compiler"""
        if text:
            text = text.strip()
            block_start, block_end = self.block_segmenter
            block_end = block_end.replace(";", "")
            self.block_segmenter = block_start, "{block_end} {text}".format(**locals())
