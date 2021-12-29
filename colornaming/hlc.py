from colorsys import rgb_to_hls

def rgb_to_hlc(r, g, b):
    hls = rgb_to_hls(r, g, b)
    chroma = max(r, g, b) - min(r, g, b)
    return (hls[0], hls[1], chroma)

def rgb_to_hlc360(r, g, b, precision=6):
    hlc = rgb_to_hlc(r, g, b)
    return (round(hlc[0] * 360, precision), round(hlc[1], precision), round(hlc[2], precision))