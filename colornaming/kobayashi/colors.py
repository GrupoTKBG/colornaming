import os 
import math
import numpy as np 
from ..colornaming import ColorNamingModel, register_model
from ..mood import MoodModel
from .moods import KobayashiMoods

kobayashi_colors = {}

def ensure_koba_data():
    if kobayashi_colors != {}:
        return

    with open(os.path.join(os.path.dirname(__file__), "data/datos colores kobayashi.csv")) as f:
        next(f) # Skip header
        for l in f:
            row = l.replace(",", ".").split(";")
            kobayashi_colors[row[0]] = {
                "rgb255": (int(row[1]), int(row[2]), int(row[3])),
                "rgb": (int(row[1])/255, int(row[2])/255, int(row[3])/255),
                "hlc": (float(row[5]), float(row[6]), float(row[7]))
            }

def distance(r0, b0, g0, r1, b1, g1):
    return math.sqrt((r1-r0)*(r1-r0) + (b1-b0)*(b1-b0) + (g1-g0)*(g1-g0))

class KobayashiModel(ColorNamingModel, MoodModel):
    def __init__(self, mood_model=None):
        ensure_koba_data()
        self.mood = KobayashiMoods(mood_model)

    def from_rgb(self, r, g, b, return_tuple=False):
        # Get nearest RGB
        labels = list(kobayashi_colors.keys())
        distances = [distance(r, g, b, 
                        kobayashi_colors[label]["rgb"][0], 
                        kobayashi_colors[label]["rgb"][1], 
                        kobayashi_colors[label]["rgb"][2]) 
                    for label in labels]
        return labels[np.argmin(distances)]

    def to_rgb(self, label):
        rgb = kobayashi_colors[label]["rgb"]
        return rgb[0], rgb[1], rgb[2]

    def get_mood(self, colors):
        return self.mood.get_mood(colors)

    def get_palettes(self, mood):
        return self.mood.get_palettes(mood)

    def get_mood_palette_size(self):
        return 3

    def get_color_names(self, attrib="rgb"):
        return [(c, kobayashi_colors[c][attrib]) for c in kobayashi_colors]


register_model("kobayashi", KobayashiModel)
