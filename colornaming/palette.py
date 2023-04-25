from typing import List
import matplotlib.pyplot as plt
import numpy as np
from .colornaming import ColorNamingModel

class Palette():
    def __init__(self, colors: List[str], model: ColorNamingModel) -> None:
        self.colors = colors
        self.model = model
    
    def plot(self):
        # Plot palette
        rgb = np.array(self.model.to_rgb(c) for c in self.colors)
        p = rgb[np.newaxis, :, :]
        plt.imshow(p)
        plt.axis('off')
        plt.show()
