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

        self.clean_csv_passes = []
        self.clean_csv_passes.append(('manuscript.csv', 'manuscript_expected.csv'))
        self.clean_csv_passes.append(('datasets.csv', 'datasets_expected.csv'))

    def clean_csv_fixture_path(self, path):
        return os.path.join('tests', 'test_data', 'clean_csv', path)

    def test_clean_csv(self):
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
