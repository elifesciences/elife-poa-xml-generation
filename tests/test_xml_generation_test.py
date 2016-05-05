import unittest
import os
import re

os.sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import parseCSVFiles
import generatePoaXml
import xml_generation
from xml_generation import *

# Import test settings last in order to override the regular settings
import poa_test_settings as settings


def override_settings():
    # For now need to override settings to use test data
    xml_generation.settings = settings
    parseCSVFiles.settings = settings
    parseCSVFiles.XLS_PATH = settings.XLS_PATH
    generatePoaXml.settings = settings

def create_test_directories():
    try:
        os.mkdir(settings.TEST_TEMP_DIR)
    except OSError:
        pass

    try:
        os.mkdir(settings.TARGET_OUTPUT_DIR)
    except OSError:
        pass


class TestXmlGeneration(unittest.TestCase):

    def setUp(self):
        override_settings()
        create_test_directories()

    def read_uncommented_xml(self, xml_file_name):
        fp = open(xml_file_name, 'rb')
        xml_content = fp.read()
        fp.close()
        # Clean the XML by removing comments
        xml_content = re.sub(ur'<!--.*-->', '', xml_content)
        return xml_content

    def test_generate(self):
        article_id = 3
        xml = build_xml_for_article(article_id)
        self.assertTrue(xml)

    def test_generate_and_compare(self):
        article_id = 3
        xml_file_name = 'elife_poa_e00003.xml'
        xml = build_xml_for_article(article_id)
        self.assertTrue(xml)

        # To compare XML generated to XML sample,
        #  remove the comments tags that hold the timestamp and git commit hash value
        generated_xml = self.read_uncommented_xml(settings.TARGET_OUTPUT_DIR +
                                                  os.sep + xml_file_name)
        compare_to_xml = self.read_uncommented_xml(settings.XLS_PATH + xml_file_name)
        self.assertEqual(generated_xml, compare_to_xml)

if __name__ == '__main__':
    unittest.main()
