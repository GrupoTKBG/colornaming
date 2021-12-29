from math import inf
from colorsys import rgb_to_hls
import numpy as np 

ADJ_LABEL_SEP = "_"

def which(point, intervals, labels):
    dig = np.digitize(point, intervals)
    if dig == 0 or dig > intervals.size:
        return None 
    return labels[dig - 1]

def make_label(adj, label, return_tuple=False):
    full_label = f"{adj}{ADJ_LABEL_SEP}{label}" if adj is not None else label
    if return_tuple:
        return (adj, label, full_label)
    return full_label

class QColorTheory():
    def __init__(self, spec):
        self.spec = spec
        self.gray_threshold = spec["gray_threshold"]
        self.qcdlab1 = spec["qcdlab1"]
        self.qcdlab2 = spec["qcdlab2"]

    def rgb_to_hlc(self, r, g, b):
        hls = rgb_to_hls(r, g, b)
        chroma = max(r, g, b) - min(r, g, b)
        return (hls[0], hls[1], chroma)

    def rgb_to_qcd(self, r, g, b, return_tuple=False):
        h, l, c = self.rgb_to_hlc(r, g, b)
        if c < self.gray_threshold:
            scale = self.qcdlab1
            value = round(l, 6)
        else:
            scale = self.qcdlab2
            value = round(h, 6)
        label = which(value, scale["intervals"], scale["names"])
        adj = None
        if label not in scale["invariable"]:
            adj_table = scale["adj_table"]
            for i, intervals in enumerate(adj_table["intervals"]):
                l0, l1, c0, c1 = intervals
                if l0 <= l < l1 and c0 <= c < c1:
                    adj = adj_table["names"][i]
                    break
        return make_label(adj, label, return_tuple=return_tuple)

default_qcd = QColorTheory({
    "gray_threshold": .2,
    "qcdlab1": {
        "intervals": np.array([0, .20, .80, 1.01]),
        "names": ("black", "grey", "white"),
        "adj_table": {
            "intervals": [[.2, .4, 0, 1.01],
                          [.6, .8, 0, 1.01]],
            "names": ("dark", "light", None)
        },
        "invariable": frozenset(["black", "white"])
    },
    "qcdlab2": {
        "intervals": np.array([0, 20, 50, 80, 160, 200, 260, 297, 335, 360])/360.0,
        "names": ("red", "orange", "yellow", "green", "turquoise", "blue", "purple", "pink", "red"),
        "adj_table": {
            "intervals": [[0, .40, 0, 1.01],
                          [.60, 1.01, 0, 1.01],
                          [.40, .60, 0, .50]],
            "names": ("dark", "light", "pale")
        },
        "invariable": frozenset()
    }
})

qcd_theories = {
    "default": default_qcd 
}

def get_qcd(name="default"):
    return qcd_theories[name]

