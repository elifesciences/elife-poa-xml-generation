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


if __name__ == '__main__':
    unittest.main()
