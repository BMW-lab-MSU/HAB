import scipy.io
import numpy as np
import os
from multiprocessing import Pool

#converts all np images in a folder to mat and creates a dir for them
def polarization_cal(DIR):
    deg_pol = [0,15,30,45,60,75,90,105,120,135,150,165,180,195,210,225,240,255,270,285,300,315,330,345,360]
    angles = [0,-15,-30,-45,-60,-75,-90,-105,-120,-135,-150,-165,-180,-195,-210,-225,-240,-255,-270,-285,-300,-315,-330,-345,-360]
    photos = np.empty([2048,2448,len(deg_pol)])
    to_remove="GETimgDegr_"
    
    for image_file in os.listdir(DIR):
        name = image_file[:-4];name = name.replace("_",".",3)
        for char in to_remove: name = name.replace(char,"")
        info = [float(x) for x in name.split("-")]
        try:
            image_np = np.load(DIR+"/"+image_file)
            photos[:,:,int(info[-1]/15)]=photos[:,:,int(info[-1]/15)]+(0.2*image_np)

        except:
            print("\n not numpy:"+DIR+"/",image_file)
            return
    mdic = {"angles":angles,"deg_pol":deg_pol,"exposure":info[1],"gain":info[0],"image_array": photos}
    return(mdic)

def dark_cal(DIR):
    to_remove="GETimg_"
    photos = np.empty([2048,2448])
    
    for image_file in os.listdir(DIR):
        name = image_file[:-4];name = name.replace("_",".",3)
        for char in to_remove: name = name.replace(char,"")
        info = name.split("-")
        info = info[:-1]
        info = [float(x) for x in info]
        try:
            image_np = np.load(DIR+"/"+image_file)
            photos=photos+(0.2*image_np)

        except:
            print("not numpy:"+DIR+"/",image_file)
    mdic = {"exposure":info[1],"gain":info[0],"image_array": photos}
    return(mdic)

def npy_to_mat(cal_day): 
    for cal in os.listdir(cal_day):
        if "mat" in cal.lower():
            continue
        elif "cal" in cal.lower():
            DIR = cal_day+cal
            for camera in os.listdir(DIR):
                if not "mat" in camera.lower():
                    mat_dir = DIR+"/"+DIR.split("/")[-1]+"_"+camera+".mat"
                    mdic=polarization_cal(DIR+"/"+camera)
                    print("\nsaving: "+mat_dir)
                    scipy.io.savemat(mat_dir, mdic)
                    print("\nsaved: "+mat_dir)
        elif "dark" in cal.lower():
            DIR = cal_day+cal
            for camera in os.listdir(DIR):
                if not "mat" in camera.lower():
                    mat_dir = DIR+"/"+DIR.split("/")[-1]+"_"+camera+".mat"
                    mdic=dark_cal(DIR+"/"+camera)
                    print("\nsaving: "+mat_dir)
                    scipy.io.savemat(mat_dir, mdic)
                    print("\nsaved: "+mat_dir)

directorys = ["/media/flint/Elements/HAB/2023-05-29-CAL/"]
with Pool(6) as p:
    p.map(npy_to_mat,directorys)
print("Done")

#file_path = 'data.mat'
#scipy.io.savemat(file_path, {'data': data})
#image_np = np.load(dir+"/"+image_file)
#img = Image.fromarray(image_np,"I;16")
#img_fileName = image_file[:-4]+".png"
#img.save(mat_dir+"/"+img_fileName)
