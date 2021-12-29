import unittest
import qcolor
from base_colors import base_colors
from rgb_hlc import rgb_to_hlc

def label_to_tuple(label):
    s = label.split("_")
    if len(s) == 2:
        return (s[0], s[1], label)
    return (None, label, label)

base_colors = {
    (0.0, 0.6, 0.9): "blue"
}

class TestQColor(unittest.TestCase):

    def test_rgb_to_hlc(self):
        qcd = qcolor.get_qcd()
        for rgb, hlc in rgb_to_hlc.items():
            r, g, b = rgb
            my_hlc = qcd.rgb_to_hlc(r, g, b)
            my_hlc = tuple(map(lambda x: round(x, 6), my_hlc))
            self.assertEqual(my_hlc, hlc)

    def test_rgb_to_qcd(self):
        qcd = qcolor.get_qcd()
        for rgb, qcol in base_colors.items():
            r, g, b = rgb
            label = qcd.rgb_to_qcd(r, g, b)
            self.assertEqual(label, qcol, msg=rgb)

    def test_rgb_to_qcd_tuple(self):
        qcd = qcolor.get_qcd()
        for rgb, qcol in base_colors.items():
            r, g, b = rgb
            label_tuple = qcd.rgb_to_qcd(r, g, b, return_tuple=True)
            self.assertEqual(label_tuple, label_to_tuple(qcol), msg=rgb)

if __name__ == '__main__':
    unittest.main()