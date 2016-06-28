import unittest
import os
import re

os.sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import parsePoaXml
import generatePubMedXml

# Import test settings last in order to override the regular settings
import poa_test_settings as settings


class TestGeneratePubMedXml(unittest.TestCase):

    def setUp(self):
        self.passes = []
        self.passes.append(('elife-02935-v2.xml', 2, 'elife-2016-05-13-140109-PubMed.xml'))
        self.passes.append(('elife_poa_e00003.xml', 1, 'elife-2016-05-13-142048-PubMed.xml'))
        self.passes.append(('elife_poa_e12717.xml', 1, 'elife-2016-06-16-021504-PubMed.xml'))
        self.passes.append(('elife-08206-v3.xml', 3, 'elife-2016-05-13-142852-PubMed.xml'))
        self.passes.append(('elife-15743-v1.xml',1, 'elife-2016-05-13-143615-PubMed.xml'))

    def clean_pubmed_xml_for_comparison(self, xml_content):
        if ('<ELocationID EIdType="doi">10.7554/eLife.00003</ELocationID>' in xml_content
             or '<ELocationID EIdType="doi">10.7554/eLife.12717</ELocationID>' in xml_content):
            xml_content = re.sub(ur'<PubDate PubStatus="aheadofprint">.*</PubDate>',
                                 '', xml_content)
        xml_content = re.sub(ur'<!--.*-->', '', xml_content)
        return xml_content

    def read_file_content(self, file_name):
        fp = open(file_name, 'rb')
        content = fp.read()
        fp.close()
        return content

    def test_parse(self):
        for (article_xml_file, version, pubmed_xml_file) in self.passes:
            file_path = settings.XLS_PATH + article_xml_file
            articles = parsePoaXml.build_articles_from_article_xmls([file_path])
            articles[0].version = version
            pubmed_xml = generatePubMedXml.build_pubmed_xml_for_articles(articles)

            model_pubmed_xml = self.read_file_content(settings.XLS_PATH + pubmed_xml_file)

            clean_generated_pubmed_xml = self.clean_pubmed_xml_for_comparison(pubmed_xml)
            clean_model_pubmed_xml = self.clean_pubmed_xml_for_comparison(model_pubmed_xml)

            self.assertEqual(clean_generated_pubmed_xml, clean_model_pubmed_xml)



if __name__ == '__main__':
    unittest.main()
