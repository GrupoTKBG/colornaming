import os 
import math
import numpy as np 
from .colornaming import ColorNamingModel, register_model

kobayashi_colors = {}

def ensure_koba_data():
    if kobayashi_colors != {}:
        return
    with open(os.path.join(os.path.dirname(__file__), "data/datos colores kobayashi.csv")) as f:
        next(f) # Skip header
        for l in f:
            row = l.replace(",", ".").split(";")
            kobayashi_colors[row[0]] = {
                "rgb": (int(row[1])/255, int(row[2])/255, int(row[3])/255),
                "hlc": (float(row[5]), float(row[6]), float(row[7]))
            }

def distance(r0, b0, g0, r1, b1, g1):
    return math.sqrt((r1-r0)*(r1-r0) + (b1-b0)*(b1-b0) + (g1-g0)*(g1-g0))

class KobayashiModel(ColorNamingModel):
    def __init__(self):
        ensure_koba_data()

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

register_model("kobayashi", KobayashiModel())
