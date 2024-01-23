#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 10:55:11 2024

@author: flint
"""
import numpy as np
import pandas as pd
from pysr import PySRRegressor

July_24 = pd.read_csv("10m_radius/2023-07-24-Flight1.csv")
July_25 = pd.read_csv("10m_radius/2023-07-25-Flight2.csv")
July_26 = pd.read_csv("10m_radius/2023-07-26-Flight1.csv")
print("Loading Aug...")
Aug_14_morning1 = pd.read_csv("10m_radius/2023-08-14-10-58.csv")
Aug_14_morning2 = pd.read_csv("10m_radius/2023-08-14-11-16.csv")
Aug_14_afternoon1 = pd.read_csv("10m_radius/2023-08-14-16-29.csv")
Aug_14_afternoon2 = pd.read_csv("10m_radius/2023-08-14-16-40.csv")

#Aug_16 = pd.read_csv("10m_radius/2023-08-16-10-42.csv")

print("Finished loading...")

"""
Train = pd.concat([Aug_14_morning1,Aug_14_afternoon2,Aug_14_afternoon1])
Test = pd.concat([Aug_14_morning2,Aug_16])

Y_train = Train["Chl"]
Y_test = Test["Chl"]

X_test = Test.drop(labels = ["C_over_A_440","C_over_A_550","C_over_A_660","Chl"],axis = 1)
X_train = Train.drop(labels = ["C_over_A_440","C_over_A_550","C_over_A_660","Chl"],axis = 1)

"""
Train = pd.concat([July_24,July_25,July_26,Aug_14_morning1,Aug_14_afternoon2])
Test = pd.concat([Aug_14_morning2,Aug_14_afternoon1])

del July_24,July_25,July_26,Aug_14_afternoon1,Aug_14_afternoon2,Aug_14_morning1,Aug_14_morning2

#Y_test_440 = Test["C_over_A_440"]
Y_test_550 = Test["C_over_A_550"]
#Y_test_660 = Test["C_over_A_660"]
X_test =  Test.drop(labels = ["C_over_A_440","C_over_A_550","C_over_A_660"],axis = 1)


#Y_train_440 = Train["C_over_A_440"]
Y_train_550 = Train["C_over_A_550"]
#Y_train_660 = Train["C_over_A_660"]
X_train =  Train.drop(labels = ["C_over_A_440","C_over_A_550","C_over_A_660"],axis = 1)

drop_keys_G = [key for key in X_train.keys() if not "Green" in key]
X_train_Green = X_train.drop(drop_keys_G,axis=1)
X_test_Green = X_test.drop(drop_keys_G,axis=1)

        
del Test,Train

print("Starting SR...")
model = PySRRegressor(
    niterations=50,  # < Increase me for better results
    binary_operators=["+","-", "*","/"],
    unary_operators=["cos","exp","sin","tan"],
    maxsize = 30,
    model_selection = "accuracy",
    batching = True,

)

model.fit(X_train_Green, Y_train_550)
Y_hat = model.predict(X_test)
Y_test_np = np.array(Y_test_550)

MSE =  np.sum(Y_test_np-Y_hat)/len(Y_test_np) 
print("MSE:",MSE)
print(model.sympy())
print(model.latex_table())
