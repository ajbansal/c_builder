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

def formatfile(filename):
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
            # Ignore comment blocks
            if line.startswith("/*"):
                if line.endswith('*/'):
                    continue
                else:
                    commentBlock = True
            if line.endswith('*/') and line.find('/*') == -1:
                commentBlock = False
                continue
            try:
                if commentBlock:
                    continue
            except NameError:
                pass
            if line.find('/*') > 1:
                line = line[:line.find('/*')].strip()
            if line.endswith(','):
                try:
                    tempdata[counter] = tempdata[counter] + " " + line
                except IndexError:
                    tempdata.append(line)
            elif line.endswith(';') or line.endswith('{') or line.endswith('}') or line == '':
                try:
                    if tempdata[counter].endswith(','):
                        tempdata[counter] = tempdata[counter] + " " + line
                        counter += 1
                        continue
                except IndexError:
                    pass

                tempdata.append(line)
                counter += 1
            else:
                logger.debug(line)
    return tempdata