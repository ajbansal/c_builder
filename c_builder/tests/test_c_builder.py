from unittest import TestCase

import os
import sys


import c_builder


class TestCBuilder(TestCase):
    def __init__(self, values):
        super(TestCBuilder, self).__init__(values)
        self.this_file_dir = os.path.dirname(__file__)
        self.test_input_file = os.path.join(self.this_file_dir, 'c_test.c')

    def test_parses_file(self):
        """To test if it parses c file and can execute the python file"""

        try:
            py_file_path = c_builder.c_file_parser.parse_file(self.test_input_file)

            try:
                sys.path.insert(0, self.this_file_dir)
                file_name, file_ext = os.path.splitext(os.path.basename(py_file_path))
                exec("import {}".format(file_name))

            except Exception as e:
                self.assertFalse(False, "Generated python file failed to execute")
                raise

        except Exception as e:
            self.assertFalse(False, "Python file could not be generated")
            raise

        else:
            self.assertTrue(True, "Test passed for parses_file_and_runs")
