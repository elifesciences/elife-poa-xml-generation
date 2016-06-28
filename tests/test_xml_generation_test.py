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

        self.passes = []
        self.passes.append((3, 'elife_poa_e00003.xml'))
        self.passes.append((2935, 'elife_poa_e02935.xml'))
        self.passes.append((2725, 'elife_poa_e02725.xml'))
        self.passes.append((12, 'elife_poa_e00012.xml'))
        self.passes.append((7, 'elife_poa_e00007.xml'))
        self.passes.append((12717, 'elife_poa_e12717.xml'))
        self.passes.append((14874, 'elife_poa_e14874.xml'))
        self.passes.append((14997, 'elife_poa_e14997.xml'))

        self.pub_date = []
        self.pub_date.append((3, time.strptime("20121113",  "%Y%m%d")))

        self.volume = []
        self.volume.append((3, 1))

        self.fails = []
        self.fails.append((99999, ''))

    def read_uncommented_xml(self, xml_file_name):
        fp = open(xml_file_name, 'rb')
        xml_content = fp.read()
        fp.close()
        # Clean the XML by removing comments
        xml_content = re.sub(ur'<!--.*-->', '', xml_content)
        return xml_content

    def test_generate(self):
        for (article_id, xml_file_name) in self.passes:
            xml = build_xml_for_article(article_id)
            self.assertTrue(xml)
        for (article_id, xml_file_name) in self.fails:
            xml = build_xml_for_article(article_id)
            self.assertFalse(xml)

    def set_pub_date(self, article, article_id):
        for (pub_date_article_id, pub_date) in self.pub_date:
            if pub_date_article_id == article_id:
                date_pub = eLifeDate("pub", pub_date)
                article.add_date(date_pub)

    def set_volume(self, article, article_id):
        for (volume_article_id, volume) in self.volume:
            if volume_article_id == article_id:
                article.volume = volume

    def test_generate_and_compare(self):
        for (article_id, xml_file_name) in self.passes:
            article, error_count = build_article_for_article(article_id)
            self.set_pub_date(article, article_id)
            self.set_volume(article, article_id)
            xml = output_xml_for_article(article, article_id)
            self.assertTrue(xml)

            # To compare XML generated to XML sample,
            #  remove the comments tags that hold the timestamp and git commit hash value
            generated_xml = self.read_uncommented_xml(settings.TARGET_OUTPUT_DIR +
                                                      os.sep + xml_file_name)
            compare_to_xml = self.read_uncommented_xml(settings.XLS_PATH + xml_file_name)
            self.assertEqual(generated_xml, compare_to_xml)

if __name__ == '__main__':
    unittest.main()
