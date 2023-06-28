import scipy.io
import numpy as np
import os
from multiprocessing import Pool

#converts all np images in a folder to mat and creates a dir for them
camera = "73"

def npy_to_mat(camera)
    directory = "/media/flint/Elements/Jun_19/Flight_1"
    dir = directory+"/220277"+camera
    mat_dir = directory+"/mats_"+camera

    if not os.path.exists(mat_dir):
        os.mkdir(mat_dir)

    for image_file in tqdm(os.listdir(dir),position=0,leave=True):
        print("\n")
        try:
            img_fileName = image_file[:-4]+".mat"
            file_path = mat_dir+"/"+img_fileName
            image_np = np.load(dir+"/"+image_file)
            scipy.io.savemat(file_path, {img_fileName, image_np})

        except:
            print(image_file)

with Pool(6) as p:
    p.map(npy_to_mat,["58","72","73"])
print("Done")


#file_path = 'data.mat'
#scipy.io.savemat(file_path, {'data': data})
#image_np = np.load(dir+"/"+image_file)
#img = Image.fromarray(image_np,"I;16")
#img_fileName = image_file[:-4]+".png"
#img.save(mat_dir+"/"+img_fileName)
