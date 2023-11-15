import scipy.io
import numpy as np
import os
from multiprocessing import Pool

#converts all np images in a folder to mat and creates a dir for them
def get_avg_dark(DIR):

    dark = np.zeros([2048,2448])
    for image_file in os.listdir(DIR):
        if "dark" in image_file.lower():
            image_np = np.load(DIR+"/"+image_file)
            dark = dark+image_np/5
    return(dark)
    

def rad_app(img, eq):
    corrected = np.zeros(np.shape(img))
    for row_idx in range(len(img)):
        for col_idx in range(len(img[0])):
            y = img[row_idx,col_idx]
            m,b = eq[row_idx,col_idx]
            corrected[row_idx,col_idx]=(y-b)/m
    return(corrected)

def polarization_cal(DIR):
    deg_pol = [0,15,30,45,60,75,90,105,120,135,150,165,180,195,210,225,240,255,270,285,300,315,330,345,360]
    angles = [0,-15,-30,-45,-60,-75,-90,-105,-120,-135,-150,-165,-180,-195,-210,-225,-240,-255,-270,-285,-300,-315,-330,-345,-360]
    photos = np.zeros([2048,2448,len(deg_pol)])
    dark = get_avg_dark(DIR)
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
        mdic = {"angles":angles,"deg_pol":deg_pol,"exposure":info[-3],"gain":info[-1],"Pol_image_array": photos}
        return(mdic)
    else:
        return("NoPol")
"""
def dark_cal(DIR):
    to_remove="GETimg_DarknI"
    photos = np.empty([2048,2448])
    for image_file in os.listdir(DIR):
        if "dark" in image_file.lower():
            name = image_file[:-4];name = name.replace("_",".",3)
            for char in to_remove: name = name.replace(char,"")
            name = name.replace("---","-")
            name = name.replace("--","-")
            info = name.split("-")
            info = [float(x) for x in info]
            try:
                image_np = np.load(DIR+"/"+image_file)
                photos=photos+(0.2*image_np)
            except:
                print("not numpy:"+DIR+"/",image_file)
    mdic = {"exposure":info[-3],"gain":info[-1],"Dark": photos}
    return(mdic)

def rad_cal(DIR):
    #photos = np.empty([2048,2448,len(deg_pol)])
    to_remove="nPolCalGETIimgDegr_Rdut"
    numb_pol = 0
    currents = []
    print(DIR)
    for image_file in os.listdir(DIR):
        if "radcal" in image_file.lower():
            numb_pol +=1
            name = image_file[:-4];name = name.replace("_",".")
            for char in to_remove: name = name.replace(char,"")
            name = name.replace("--","-")
            info = [float(x) for x in name.split("-")]
            #print(info)
            image_np = np.load(DIR+"/"+image_file)
            if not info[1] in currents and not np.mean(image_np.astype(float))>60000:
                currents.append(info[1])
    currents.sort()
    photos = np.zeros([2048,2448,len(currents)])
    
    for image_file in os.listdir(DIR):
        if "radcal" in image_file.lower():
            numb_pol +=1
            name = image_file[:-4];name = name.replace("_",".")
            for char in to_remove: name = name.replace(char,"")
            name = name.replace("--","-")
            info = [float(x) for x in name.split("-")]
            #print(info)
            image_np = np.load(DIR+"/"+image_file)
            
            if info[1] in currents:
                idx = currents.index(info[1])
            
                if not np.mean(image_np.astype(float))>60000:
                    photos[:,:,idx] = photos[:,:,idx]+(image_np/5)
                else:
                    photos=np.delete(photos,idx)
                    currents.pop(idx)
                    print("didnt work")
    mdic = {"currents":currents,"exposure":info[-3],"gain":info[-1],"Rad_image_array": photos}
    return(mdic)
"""   
    
def npy_to_mat(cal_day): 
    for camera in os.listdir(cal_day):
        if "." in camera.lower():
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
                mat_dir = cal_day+"/"+camera+"-Dark.mat"
                mdic = dark_cal(DIR)
                scipy.io.savemat(mat_dir,mdic)





directorys = ["/mnt/data/HAB/Flathead-Aug-2023-Cal/2023-08-14/","/mnt/data/HAB/Flathead-Aug-2023-Cal/2023-08-16/"]
for directory in directorys:
    for day in os.listdir(directory):
        print(directory+day+"/")
        npy_to_mat(directory+day+"/")
print("Done")
#file_path = 'data.mat'
#scipy.io.savemat(file_path, {'data': data})
#image_np = np.load(dir+"/"+image_file)
#img = Image.fromarray(image_np,"I;16")
#img_fileName = image_file[:-4]+".png"
#img.save(mat_dir+"/"+img_fileName)
