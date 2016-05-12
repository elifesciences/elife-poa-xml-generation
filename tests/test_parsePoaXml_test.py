import unittest
import os
import re

os.sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import parsePoaXml
import generatePoaXml

# Import test settings last in order to override the regular settings
import poa_test_settings as settings


class TestParsePoaXml(unittest.TestCase):

    def setUp(self):
        self.passes = []
        self.passes.append('elife-02935-v2.xml')
        self.passes.append('elife-04637-v2.xml')
        self.passes.append('elife-15743-v1.xml')
        self.passes.append('elife-02043-v2.xml')

    def test_parse(self):
        for xml_file_name in self.passes:
            file_path = settings.XLS_PATH + xml_file_name
            articles = parsePoaXml.build_articles_from_article_xmls([file_path])
            self.assertEqual(len(articles), 1)



if __name__ == '__main__':
    unittest.main()
