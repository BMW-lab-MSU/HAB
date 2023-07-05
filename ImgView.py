import numpy as np
import os
from PIL import Image
from tqdm import tqdm
from multiprocessing import Pool

#converts all np images in a folder to png and creates a gif

def numpy_to_png(camera):
    directory = "/media/flint/Elements/HAB/Jul_5_test/Flight_2/"
    dir = directory+"/220277"+camera
    png_dir = directory+"/pngs"+camera
    #makes png directorys
    if not os.path.exists(png_dir):
        os.mkdir(png_dir)
    #converts images
    for image_file in tqdm(os.listdir(dir),position=0,leave=True):
        print("\n")
        try:
            image_np = np.load(dir+"/"+image_file)
            img = Image.fromarray(image_np,"I;16")
            img_fileName = image_file[:-4]+".png"
            img.save(png_dir+"/"+img_fileName)
        except:
            print(image_file)
    #makes gif
    os.system("ffmpeg -framerate 5 -pattern_type glob -i '"+png_dir+"/*.png' "+directory+"/"+camera+".mp4")

#par loop
with Pool(6) as p:
    p.map(numpy_to_png,["58","72","73"])



print("Done")

