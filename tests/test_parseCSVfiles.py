import unittest
import os
import re

import parseCSVFiles
import generatePoaXml
import xml_generation
from xml_generation import *

# Import test settings last in order to override the regular settings
import poa_test_settings
import test_helpers

class TestParseCsvFiles(unittest.TestCase):

    def setUp(self):
        test_helpers.override_settings()
        test_helpers.create_test_directories()

        self.join_lines_passes = []
        self.join_lines_passes.append(("", "\n", 1, "\n"))
        self.join_lines_passes.append(("", "\n", 10, " "))
        self.join_lines_passes.append(("one\n", '"', 10, 'one"'))
        self.join_lines_passes.append(("one\r\n", '    two', 10, 'onetwo'))
        self.join_lines_passes.append(("\n", "two \n", 10, "two \n"))

        self.do_add_line_passes = []
        self.do_add_line_passes.append(("", 1, True)) # blank header row
        self.do_add_line_passes.append(('"A typical header row"', 1, True))
        self.do_add_line_passes.append(("", 10, False))
        self.do_add_line_passes.append(('"a full line","it is"', 10, True))
        self.do_add_line_passes.append(('"', 10, True))

        self.flatten_lines_passes = []
        self.flatten_lines_passes.append((0, ["\"a\n", "   b\n", '"\n'], '"ab"\n'))

        self.clean_csv_passes = []
        self.clean_csv_passes.append(('manuscript.csv', 'manuscript_expected.csv'))
        self.clean_csv_passes.append(('datasets.csv', 'datasets_expected.csv'))

    def clean_csv_fixture_path(self, path):
        return os.path.join('tests', 'test_data', 'clean_csv', path)

    def test_join_lines(self):
        for (line_one, line_two, line_number, expected) in self.join_lines_passes:
            content = parseCSVFiles.join_lines(line_one, line_two, line_number)
            self.assertEqual(
                content, expected,
                '{line_one} + {line_two} does not equal {expected}, got {content}'.format(
                    line_one=line_one,
                    line_two=line_two,
                    expected=expected,
                    content=content
                    ))

    def test_do_add_line(self):
        for (content, line_number, expected) in self.do_add_line_passes:
            add_line = parseCSVFiles.do_add_line(content, line_number)
            self.assertEqual(
                add_line, expected,
                '{content} as line number {line} does not match {expected}, got {add_line}'.format(
                    content=content,
                    line=line_number,
                    expected=expected,
                    add_line=add_line
                    ))

    def test_flatten_lines(self):
        "test flattening lines separately"
        for (data_start_row, iterable, expected) in self.flatten_lines_passes:
            data = parseCSVFiles.flatten_lines(iterable, data_start_row)
            self.assertEqual(
                data, expected,
                '{iterable} does not flatten to {expected}, got {data}'.format(
                    iterable=iterable,
                    expected=expected,
                    data=data
                    ))

    def test_clean_csv(self):
        "test clean_csv using file read and writes"
        for (input_csv, expected_csv) in self.clean_csv_passes:
            input_csv_path = self.clean_csv_fixture_path(input_csv)
            expected_csv_path = self.clean_csv_fixture_path(expected_csv)
            new_path = parseCSVFiles.clean_csv(input_csv_path)
            data = None
            expected_data = None
            with open(new_path, 'rb') as csv_data:
                data = csv_data.read()
            with open(expected_csv_path, 'rb') as expected_csv_data:
                expected_data = expected_csv_data.read()
            # test assertions
            self.assertIsNotNone(data)
            self.assertIsNotNone(expected_data)
            self.assertEqual(data, expected_data,
                             '{input_csv} does not equal {expected_csv}'.format(
                                input_csv=input_csv,
                                expected_csv=expected_csv
                                ))


if __name__ == '__main__':
    unittest.main()
