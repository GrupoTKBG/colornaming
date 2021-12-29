import unittest
import colornaming
from base_colors import base_colors
from prl15_colors import prl15_colors

def label_to_tuple(label):
    s = label.split("_")
    if len(s) == 2:
        return (s[0], s[1], label)
    return (None, label, label)

# base_colors = {    (0.200000, 0.200000, 1.000000): "blue" }
class TestQCD(unittest.TestCase):
        
    def test_rgb_to_qcd(self):
        qcd = colornaming.get_model("qcd")
        for rgb, qcol in base_colors.items():
            r, g, b = rgb
            label = qcd.from_rgb(r, g, b)
            self.assertEqual(label, qcol, msg=rgb)

    def test_rgb_to_qcd_tuple(self):
        qcd = colornaming.get_model("qcd")
        for rgb, qcol in base_colors.items():
            r, g, b = rgb
            label_tuple = qcd.from_rgb(r, g, b, return_tuple=True)
            self.assertEqual(label_tuple, label_to_tuple(qcol), msg=rgb)

    def test_rgb_to_qcd_prl15(self):
        qcd = colornaming.get_model("qcd:prl15")
        for rgb, qcol in prl15_colors.items():
            r, g, b = rgb
            label = qcd.from_rgb(r, g, b)
            self.assertEqual(label, qcol, msg=rgb)

if __name__ == '__main__':
    unittest.main()