import scipy.io
import numpy as np
import os
from multiprocessing import Pool

#converts all np images in a folder to mat and creates a dir for them
def polarization_cal(DIR):
    deg_pol = [0,15,30,45,60,75,90,105,120,135,150,165,180,195,210,225,240,255,270,285,300,315,330,345,360]
    angles = [0,-15,-30,-45,-60,-75,-90,-105,-120,-135,-150,-165,-180,-195,-210,-225,-240,-255,-270,-285,-300,-315,-330,-345,-360]
    photos = np.empty([2048,2448,len(deg_pol)])
    to_remove="nPolCalGETIimgDegr_"
    numb_pol = 0
    for image_file in os.listdir(DIR):
        if "polcal" in image_file.lower():
            numb_pol +=1
            name = image_file[:-4];name = name.replace("_",".")
            for char in to_remove: name = name.replace(char,"")
            name = name.replace("--","-")
            info = [float(x) for x in name.split("-")]
            try:
                image_np = np.load(DIR+"/"+image_file)
                photos[:,:,int(info[1]/15)]=photos[:,:,int(info[1]/15)]+(0.2*image_np)
    
            except:
                print("\n not numpy:"+DIR+"/",image_file)
                return
    if numb_pol>0:
        mdic = {"angles":angles,"deg_pol":deg_pol,"exposure":info[4],"gain":info[-1],"image_array": photos}
        return(mdic)
    else:
        return("NoPol")

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
    for camera in os.listdir(cal_day):
        if "mat" in camera.lower():
            continue
        else:
            DIR = cal_day+camera
            if not "mat" in camera.lower() and "nm" in camera.lower():
                mat_dir = cal_day+"/"+camera+"-PolCal.mat"
                mdic=polarization_cal(DIR)
                if mdic != "NoPol":
                    print("\nsaving: "+mat_dir)
                    scipy.io.savemat(mat_dir, mdic)
                    print("\nsaved: "+mat_dir)


directorys = ["/mnt/data/HAB/2023-08-04-CAL/"]
npy_to_mat(directorys[0])
print("Done")

#file_path = 'data.mat'
#scipy.io.savemat(file_path, {'data': data})
#image_np = np.load(dir+"/"+image_file)
#img = Image.fromarray(image_np,"I;16")
#img_fileName = image_file[:-4]+".png"
#img.save(mat_dir+"/"+img_fileName)
