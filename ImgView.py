import numpy as np
import os
from PIL import Image
from tqdm import tqdm
from multiprocessing import Pool
import imageio.v2 as imageio

#converts all np images in a folder to png and creates a dir for them
camera = "73"

def png_to_gif(camera):
    # filepaths
    directory = "/media/flint/Elements/Jun_19/Flight_1/"
    fp_in = directory+"pngs"+camera+"/"
    
    fp_out = directory+camera+".gif"
    imgs=[]
    for filename in os.listdir(fp_in):
        img_pth = fp_in+"/"+filename
        imgs.append(imageio.imread(img_pth))
    imageio.mimsave(fp_out,imgs,duration =200)
def numpy_to_png(camera):
    directory = "/media/flint/Elements/Jun_19/Flight_1"
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

with Pool(6) as p:
    p.map(numpy_to_png,["58","72","73"])
print("Done")

