import os
import zipfile
from typing import List
from itertools import combinations_with_replacement
import matplotlib.pyplot as plt
import numpy as np
from xgboost import XGBRegressor
from .colornaming import ColorNamingModel


palette_model = None

def load_palette_model():
    global palette_model
    if palette_model is None:
        palette_model = XGBRegressor()

        if not os.path.exists("models/xgb_pal5_full.json"):
            if os.path.exists("models/xgb_pal5_full.zip"):
                with zipfile.ZipFile("models/xgb_pal5_full.zip", 'r') as zip_ref:
                    zip_ref.extractall("models/")
        palette_model.load_model("models/xgb_pal5_full.json")

class Palette():
    def __init__(self, colors: List[str], model: ColorNamingModel) -> None:
        self.colors = colors
        self.model = model
        self.scoring_model = None

    
    def plot(self):
        # Plot palette
        rgb = np.array(self.model.to_rgb(c) for c in self.colors)
        p = rgb[np.newaxis, :, :]
        plt.imshow(p)
        plt.axis('off')
        plt.show()

    def _score_pal(self, koba_colors):
        rgb = list(map(self.model.to_rgb, koba_colors))
        feat = np.array(rgb).flatten()
        return palette_model.predict([feat])[0]
        
    def score_palette(self, agg=np.mean):
        load_palette_model()
        #pals = [comb for comb in combinations_with_replacement(koba_colors, 5) if all(elem in comb for elem in koba_colors)]  
        pals = [comb for comb in combinations_with_replacement(self.colors, 5) if list(dict.fromkeys(comb)) == self.colors]  
        # print(pals)
        return agg(list(map(self._score_pal, pals))) 