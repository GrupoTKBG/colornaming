import os
import zipfile
import sys
from typing import List, Optional
from itertools import combinations_with_replacement
import matplotlib.pyplot as plt
import numpy as np
from xgboost import XGBRegressor
from .colornaming import ColorNamingModel

palette_model : Optional[XGBRegressor] = None

def load_palette_model():
    global palette_model
    if palette_model is None:
        palette_model = XGBRegressor()

        model_dir = os.path.join(os.path.dirname(__file__), "models")
        if not os.path.exists(f"{model_dir}/xgb_pal5_full.json"):
            if os.path.exists(f"{model_dir}/xgb_pal5_full.json.zip"):
                with zipfile.ZipFile(f"{model_dir}/xgb_pal5_full.json.zip", 'r') as zip_ref:
                    zip_ref.extractall(model_dir)
        palette_model.load_model(f"{model_dir}/xgb_pal5_full.json")

def score_rbg(colors):
    load_palette_model()
    feat = np.array(colors).flatten()
    return palette_model.predict([feat])[0] # type: ignore


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
        return score_rbg(rgb)
        
    def score_palette(self, agg=np.mean):
        load_palette_model()
        #pals = [comb for comb in combinations_with_replacement(koba_colors, 5) if all(elem in comb for elem in koba_colors)]  
        pals = [comb for comb in combinations_with_replacement(self.colors, 5) if list(dict.fromkeys(comb)) == self.colors]  
        # print(pals)
        return agg(list(map(self._score_pal, pals))) 
    
