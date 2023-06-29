import scipy.io
import numpy as np
import os
from multiprocessing import Pool

#converts all np images in a folder to mat and creates a dir for them

def npy_to_mat(directory):
    deg_pol = [0,15,30,45,60,75,90,105,120,135,150,165,180,195,210,225,240,255,270,285,300,315,330,345,360]
    angles = [0,-15,-30,-45,-60,-75,-90,-105,-120,-135,-150,-165,-180,-195,-210,-225,-240,-255,-270,-285,-300,-315,-330,-345,-360]
    for cal in os.listdir(directory):
        
        for camera in os.listdir(directory+"/"+cal):
            DIR = directory+"/"+cal+"/"+camera
            mat_dir = directory+"/"+cal+"/mats_"+camera
            
            if not os.path.exists(mat_dir):
                os.mkdir(mat_dir)
        
            for image_file in os.listdir(DIR):

                img_fileName = image_file[:-4]+".mat"
                file_path = mat_dir+"/"+img_fileName
                
                try:
                    image_np = np.load(DIR+"/"+image_file)
                    scipy.io.savemat(file_path, {image_file[:-4]: image_np})
        
                except:
                    print("Not Saved:",image_file)

directorys = ["/media/flint/USB DISK/2023-05-31_CAL/","/media/flint/USB DISK/2023-05-29-CAL/"]
with Pool(6) as p:
    p.map(npy_to_mat,directorys)
print("Done")

#file_path = 'data.mat'
#scipy.io.savemat(file_path, {'data': data})
#image_np = np.load(dir+"/"+image_file)
#img = Image.fromarray(image_np,"I;16")
#img_fileName = image_file[:-4]+".png"
#img.save(mat_dir+"/"+img_fileName)
