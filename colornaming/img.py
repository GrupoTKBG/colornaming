from itertools import combinations
import numpy as np
from .mood import MoodModel

class QImage():
    def __init__(self, arr, model, mode=None, from_quantized=None):
        self.cache = {}
        self.arr = arr
        self.model = model
        self._quantized = from_quantized
        self._histogram = None
        if mode is None:
            coords = arr.shape[2]
            if coords == 4:
                self.mode = "RGBA"
            elif coords == 3:
                self.mode = "RGB"
            elif coords == 1:
                if np.max(arr) > 1:
                    self.mode = "L"
                else:
                    self.mode = "1"
            else:
                raise ValueError("Invalid array shape")
        else:
            if mode not in ('1', 'L', 'RGB', 'RGBA'):
                raise ValueError("Invalid mode")
            self.mode = mode
        if self.mode != '1':
            self.arr = arr.astype('float32') / 255.0

    @property
    def quantized(self):
        return self.quantize()
        
    def _convert_1(self, c):
        color = [255, 255, 255] if c == 1 else [0, 0, 0]
        return self._convert_rgb(color)

    def _convert_l(self, c):
        return self._convert_rgb([c, c, c])

    def _convert_rgb(self, rgb):
        t = tuple(rgb)
        if t in self.cache:
            return self.cache[t]
        ret = self.model.from_rgb(*t)
        self.cache[t] = ret
        return ret

    def _convert_rgba(self, rgba):
        if rgba[3] == 0:
            return "#transparent"
        return self._convert_rgb(rgba[:3])

    def _convert_function(self):
        if self.mode == '1':
            return self._convert_1
        if self.mode == 'L':
            return self._convert_1
        if self.mode == 'RGB':
            return self._convert_rgb
        if self.mode == 'RGBA':
            return self._convert_rgba 

    def quantize(self):
        if self._quantized is None:
            arr = np.apply_along_axis(self._convert_function(), 2, self.arr)
            shape = tuple(list(self.arr.shape[:2]) + [1])
            self._quantized = np.reshape(arr, shape)
        return self._quantized

    def histogram(self):
        if self._histogram is None:
            a = self.quantize()
            unique, counts = np.unique(a, return_counts=True)
            self._histogram = dict(zip(unique, counts))
        return self._histogram.copy()
    
    def top_colors(self, n=None, min_weight=0.0):
        h = self.histogram()
        if '#transparent' in h:
            del h['#transparent']
        s = sorted(h.keys(), key=h.get, reverse=True)
        total = sum(h.values()) - h.get("#transparent", 0)
        return [(k, h[k]/total) for k in s[:n] if h[k]/total >= min_weight]
    
    def top_moods(self, n=None, min_weight=0.0):
        if not isinstance(self.model, MoodModel):
            return []
        h = self.histogram()
        total = sum(h.values()) - h.get("#transparent", 0)
        moods = {}
        for c in combinations(h.keys(), self.model.get_mood_palette_size()):
            mood = self.model.get_mood(c)
            if mood is None:
                continue
            weight = sum(h[col] for col in c)/total
            if mood in moods:
                moods[mood] += weight
            else:
                moods[mood] = weight
        s = sorted(moods, key=moods.get, reverse=True)
        return [(m, moods[m]) for m in s[:n] if moods[m] >= min_weight]
