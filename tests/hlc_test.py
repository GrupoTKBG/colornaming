import unittest
from colornaming.hlc import rgb_to_hlc, rgb_to_hlc360 
from rgb_hlc import rgb_hlc
from rgb_hlc360 import rgb_hlc360

class TestHLC(unittest.TestCase):

    def test_rgb_to_hlc(self):
        for rgb, hlc in rgb_hlc.items():
            r, g, b = rgb
            my_hlc = rgb_to_hlc(r, g, b)
            my_hlc = tuple(map(lambda x: round(x, 6), my_hlc))
            self.assertEqual(my_hlc, hlc)

    def test_rgb_to_hlc360(self):
        for rgb, hlc in rgb_hlc360.items():
            r, g, b = rgb
            my_hlc = rgb_to_hlc360(r, g, b)
            my_hlc = tuple(map(lambda x: round(x, 6), my_hlc))
            self.assertEqual(my_hlc, hlc)
