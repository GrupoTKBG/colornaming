import unittest
import qcolor

color_table = {
    (0.2, 0.2, 0.2): "dark_grey",
    (0.5, 0.25, 0.9): "purple"
}

def label_to_tuple(label):
    s = label.split("_")
    if len(s) == 2:
        return (s[0], s[1], label)
    return (None, label, label)

class TestQColor(unittest.TestCase):
    def test_rgb_to_qcd(self):
        qcd = qcolor.get_qcd()
        for rgb, qcol in color_table.items():
            r, g, b = rgb
            label = qcd.rgb_to_qcd(r, g, b)
            self.assertEqual(label, qcol)
            label_tuple = qcd.rgb_to_qcd(r, g, b, return_tuple=True)
            self.assertEqual(label_tuple, label_to_tuple(qcol))

if __name__ == '__main__':
    unittest.main()