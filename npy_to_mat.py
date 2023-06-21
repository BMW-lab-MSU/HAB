import scipy.io
import numpy as np

 
file_path = 'data.mat'
scipy.io.savemat(file_path, {'data': data})
