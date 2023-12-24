import scipy.io
import numpy as np
import os
import multiprocessing as MP
import time
import matplotlib.pyplot as plt
#converts all np images in a folder to mat and creates a dir for them
def get_avg_dark(DIR):
    #gets average dark for camera and flight
    dark = np.zeros([2048,2448])
    for image_file in os.listdir(DIR):
        if "dark" in image_file.lower():
            image_np = np.load(DIR+"/"+image_file)
            dark = dark+image_np/5
    return(dark)
    

def rad_app(img, eq):
    #applies the rad cal
    m = eq[:,:,0]
    m[m==0]= m.mean() #python doesn't like to divide by zero so if its zero it just sets it to the mean
    b = eq[:,:,1]
    corrected = (img-b)/m
    return(corrected)


def polarization_cal(DIR):
    deg_pol = [0,15,30,45,60,75,90,105,120,135,150,165,180,195,210,225,240,255,270,285,300,315,330,345,360]
    angles = [0,-15,-30,-45,-60,-75,-90,-105,-120,-135,-150,-165,-180,-195,-210,-225,-240,-255,-270,-285,-300,-315,-330,-345,-360]
    photos = np.zeros([2048,2448,len(deg_pol)])
    dark = get_avg_dark(DIR)
    to_remove="nPolCalGETIimgDegr_"
    numb_pol = 0
    rad_eq = np.load(DIR+"-RAD.npy")
    for image_file in os.listdir(DIR):
        if "polcal" in image_file.lower():
            numb_pol +=1
            name = image_file[:-4];name = name.replace("_",".")
            for char in to_remove: name = name.replace(char,"")
            name = name.replace("--","-")
            info = [float(x) for x in name.split("-")]
            try:
                image_np = np.load(DIR+"/"+image_file)
                image_np = image_np - dark
                image_np = rad_app(image_np,rad_eq)
                photos[:,:,int(info[1]/15)]=photos[:,:,int(info[1]/15)]+(0.2*image_np)
    
            except:
                print("\n not numpy:"+DIR+"/",image_file)
                return
    if numb_pol>0:
        mdic = {"angles":angles,"deg_pol":deg_pol,"exposure":info[-3],"gain":info[-1],"Pol_image_array": photos}
        return(mdic)
    else:
        return("NoPol")

    
def npy_to_mat(DIR): 
    mat_dir = DIR+"-PolCal.mat"
    mdic=polarization_cal(DIR)
    if mdic != "NoPol":
        print("\nsaving: "+mat_dir)
        scipy.io.savemat(mat_dir, mdic)
        print("\nsaved: "+mat_dir)



Month = "/mnt/data/HAB/Flathead-July-2023-Cal/"

DIRs = [x[0] for x in os.walk(Month) if "nm" in x[0]]


"""
serial
for file in DIRs:
    npy_to_mat(file)

"""
Threads = np.arange(1,11)
time_taken = []
for thread in Threads:
    start = time.time()
    with MP.Pool(thread) as p:
        p.map(npy_to_mat,DIRs)
    end = time.time()
    TIME_TAKEN_TEMP = end-start
    time_taken.append(TIME_TAKEN_TEMP)
    print(TIME_TAKEN_TEMP)

print("Done")
TIME = np.array(time_taken)
TIME = TIME/60
plt.figure()
plt.plot(Threads,TIME)
plt.xlabel("Threads")
plt.ylabel("Time (Min)")
plt.title("Threads vs Time - npy_to_mat.py")
plt.scatter(Threads,TIME)
plt.show()
#file_path = 'data.mat'
#scipy.io.savemat(file_path, {'data': data})
#image_np = np.load(dir+"/"+image_file)
#img = Image.fromarray(image_np,"I;16")
#img_fileName = image_file[:-4]+".png"
#img.save(mat_dir+"/"+img_fileName)
