import unittest
import os
import re

os.sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import parsePoaXml
import generateCrossrefXml

# Import test settings last in order to override the regular settings
import poa_test_settings as settings


class TestGenerateCrossrefXml(unittest.TestCase):

    def setUp(self):
        self.passes = []
        self.passes.append(('elife-02935-v2.xml', 'elife-crossref-02935-20160513131503.xml'))
        self.passes.append(('elife_poa_e00003.xml', 'elife-crossref-00003-20160513111437.xml'))
        self.passes.append(('elife-15743-v1.xml', 'elife-crossref-15743-20160513133358.xml'))
        self.passes.append(('elife-02020-v1.xml', 'elife-crossref-02020-20160513134225.xml'))
        self.passes.append(('elife-08206-v3.xml', 'elife-crossref-08206-20160513134247.xml'))
        self.passes.append(('elife-04637-v2.xml', 'elife-crossref-04637-20160513134549.xml'))

    def clean_crossref_xml_for_comparison(self, xml_content):
        # For now running a test on a PoA article ignore the
        # <publication_date media_type="online"> which is set to the date it is generated
        if '<doi_batch_id>elife-crossref-00003' in xml_content:
            xml_content = re.sub(ur'<publication_date media_type="online">.*-->',
                                 '</publication_date>', xml_content)

        xml_content = re.sub(ur'<!--.*-->', '', xml_content)
        xml_content = re.sub(ur'<doi_batch_id>.*</doi_batch_id>', '', xml_content)
        xml_content = re.sub(ur'<timestamp>.*</timestamp>', '', xml_content)
        return xml_content

    def read_file_content(self, file_name):
        fp = open(file_name, 'rb')
        content = fp.read()
        fp.close()
        return content

    def test_parse(self):
        for (article_xml_file, crossref_xml_file) in self.passes:
            file_path = settings.XLS_PATH + article_xml_file
            articles = parsePoaXml.build_articles_from_article_xmls([file_path])
            crossref_xml = generateCrossrefXml.build_crossref_xml_for_articles(articles)

            model_crossref_xml = self.read_file_content(settings.XLS_PATH + crossref_xml_file)

            clean_generated_crossref_xml = self.clean_crossref_xml_for_comparison(crossref_xml)
            clean_model_crossref_xml = self.clean_crossref_xml_for_comparison(model_crossref_xml)

            self.assertEqual(clean_generated_crossref_xml, clean_model_crossref_xml)



if __name__ == '__main__':
    unittest.main()
