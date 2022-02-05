from colornaming import get_model
from colornaming.img import QImage

from PIL import Image
import numpy as np
image = Image.open('/Users/isanz/Papers/IJUFKS/thumbs/comida/image2-comida.png')
print(image.format)
print(image.mode)
print(image.size) 
image.thumbnail((250, 250), Image.NEAREST)
print("Thumbnail size:", image.size)  
arr = np.array(image)
a = QImage(arr, get_model("kobayashi"))
print(a.top_colors(5))
b = QImage(arr, get_model("qcd"))
print(b.top_colors(5))
