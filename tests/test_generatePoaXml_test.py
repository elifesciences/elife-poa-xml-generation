import unittest
import os

os.sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import generatePoaXml



class TestGeneratePoaXml(unittest.TestCase):

    def test_escape_unmatched_angle_brackets(self):
        """
        Test some additional examples of unmatched angle brackets specifically
        """
        self.passes = []
        self.passes.append(('<',
                           '&lt;'))

        self.passes.append(('< T << G << C >> A <<i>m</i>',
                           '&lt; T &lt;&lt; G &lt;&lt; C &gt;&gt; A &lt;<i>m</i>'))

        self.passes.append(('<p>**p<0.01; ***p<0.001. SI, aged mice >5 months old.</p>',
                           '<p>**p&lt;0.01; ***p&lt;0.001. SI, aged mice &gt;5 months old.</p>'))

        for string_input, string_output in self.passes:
            self.assertEqual(generatePoaXml.escape_unmatched_angle_brackets(
                string_input), string_output)

    def test_entity_to_unicode(self):
        self.passes = []
        self.passes.append(('N-terminal &#x03B1;-helix into the heterodimer interface',
                           u'N-terminal \u03b1-helix into the heterodimer interface'))

        self.passes.append(('N-terminal &alpha;-helix into the heterodimer interface',
                           u'N-terminal \u03b1-helix into the heterodimer interface'))

        self.passes.append(('&#x00A0; &#x00C5; &#x00D7; &#x00EF; &#x0394; &#x03B1; &#x03B2; &#x03B3; &#x03BA; &#x03BB; &#x2212; &#x223C; &alpha; &amp; &beta; &epsilon; &iuml; &ldquo; &ordm; &rdquo;',
                           u'\xa0 \xc5 \xd7 \xef \u0394 \u03b1 \u03b2 \u03b3 \u03ba \u03bb \u2212 \u223c \u03b1 &amp; \u03b2 \u03b5 \xcf " \xba "'))

        for string_input, string_output in self.passes:
            self.assertEqual(generatePoaXml.entity_to_unicode(
                string_input), string_output)

    def test_xml_escape_ampersand(self):
        self.passes = []
        self.passes.append(('',
                           u''))
        self.passes.append(('a',
                           u'a'))
        self.passes.append(('another & another & another',
                           u'another &amp; another &amp; another'))
        self.passes.append(('a&a',
                           u'a&amp;a'))
        self.passes.append(('a&amp;&a',
                           u'a&amp;&amp;a'))
        self.passes.append(('a&#x0117;a',
                           u'a&#x0117;a'))
        self.passes.append(('fake link http://example.org/?a=b&amp',
                           u'fake link http://example.org/?a=b&amp;amp'))
        self.passes.append(('CUT&RUN is performed',
                           u'CUT&amp;RUN is performed'))

        for string_input, string_output in self.passes:
            self.assertEqual(generatePoaXml.xml_escape_ampersand(
                string_input), string_output)

    def test_do_display_channel(self):
        "test blank and non-blank values for display channel for whether it gets added to the XML"
        doi = "10.7554/eLife.00666"
        title = "Test article"
        # first example has no display channel or categories
        poa_article_1 = generatePoaXml.eLifePOA(doi, title)
        e_xml = generatePoaXml.eLife2XML(poa_article_1)
        self.assertEqual(e_xml.do_display_channel(poa_article_1), False)
        self.assertEqual(e_xml.do_subject_heading(poa_article_1), False)
        self.assertEqual(e_xml.do_article_categories(poa_article_1), False)
        # second example has a display channel, no categories
        poa_article_2 = generatePoaXml.eLifePOA(doi, title)
        poa_article_2.display_channel = 'Display Channel'
        e_xml = generatePoaXml.eLife2XML(poa_article_1)
        self.assertEqual(e_xml.do_display_channel(poa_article_2), True)
        self.assertEqual(e_xml.do_subject_heading(poa_article_2), False)
        self.assertEqual(e_xml.do_article_categories(poa_article_2), True)
        # third example has a display channel and categories
        poa_article_3 = generatePoaXml.eLifePOA(doi, title)
        poa_article_3.display_channel = 'Display Channel'
        poa_article_3.add_article_category('Article Category')
        e_xml = generatePoaXml.eLife2XML(poa_article_3)
        self.assertEqual(e_xml.do_display_channel(poa_article_3), True)
        self.assertEqual(e_xml.do_subject_heading(poa_article_3), True)
        self.assertEqual(e_xml.do_article_categories(poa_article_3), True)
        # fourth example has a blank strings for display channel and categories
        poa_article_4 = generatePoaXml.eLifePOA(doi, title)
        poa_article_4.display_channel = ' '
        poa_article_4.add_article_category('   ')
        e_xml = generatePoaXml.eLife2XML(poa_article_4)
        self.assertEqual(e_xml.do_display_channel(poa_article_4), False)
        self.assertEqual(e_xml.do_subject_heading(poa_article_4), False)
        self.assertEqual(e_xml.do_article_categories(poa_article_4), False)
        # fifth example has None display channel and categories
        poa_article_5 = generatePoaXml.eLifePOA(doi, title)
        poa_article_5.display_channel = None
        poa_article_5.add_article_category(None)
        e_xml = generatePoaXml.eLife2XML(poa_article_5)
        self.assertEqual(e_xml.do_display_channel(poa_article_5), False)
        self.assertEqual(e_xml.do_subject_heading(poa_article_5), False)
        self.assertEqual(e_xml.do_article_categories(poa_article_5), False)


if __name__ == '__main__':
    unittest.main()
