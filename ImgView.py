import numpy as np
import os
from PIL import Image
camera = "58"
dir = "2023-06-07/Flight_5/220277"+camera

for image_file in os.listdir(dir):
    try:
        image_np = np.load(dir+"/"+image_file)
        img = Image.fromarray(image_np,"I;16")
        img_fileName = image_file[:-4]+".png"
        img.save("2023-06-07/Flight_5/pngs/"+camera"/"+img_fileName)
    except:
        print(image_file)
    

print("Done")
