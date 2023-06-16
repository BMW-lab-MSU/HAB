import numpy as np
import os
from PIL import Image
from tqdm import tqdm

#converts all np images in a folder to png and creates a dir for them
camera = "58"
directory = "2023-06-16/Flight_1"
dir = directory+"/220277"+camera
png_dir = directory+"/pngs"+camera

if not os.path.exists(png_dir):
    os.mkdir(png_dir)

for image_file in tqdm(os.listdir(dir),position=0,leave=True):
    print("\n")
    try:
        image_np = np.load(dir+"/"+image_file)
        img = Image.fromarray(image_np,"I;16")
        img_fileName = image_file[:-4]+".png"
        img.save(png_dir+"/"+img_fileName)
    except:
        print(image_file)
    

print("Done")
