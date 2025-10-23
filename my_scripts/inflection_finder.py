#!/usr/bin/env 

import scipy
from scipy.optimize import curve_fit
import numpy as np
import math
import matplotlib.pyplot as plt
import pandas as pd
#import my_functions.files.file_funcs as mf

all_data = []
xvals = []
ydata = []
xdata = []

#READ IN DATA
with open("67NR_CSO36658_SJs.txt","r") as f:
    for item in f.readlines():
        my_items = item.strip().split("\t")
        all_data.append(my_items)

f.close()

#SORT THE LIST

#print(all_data[0:5])

#sorted_data = all_data.sort(key=lambda x: x[1], reverse=True)

#print("len sorted data: " + str(len(sorted_data)))

for idx, values in enumerate(all_data):
    xdata.append(idx+1)
    xvals.append(values[0])
    ydata.append(values[1])

print(ydata[0:5])
print(xdata[0:5])

#GENERATE AVERAGE PER SAMPLE (IF RELEVANT)

#CURVE FIT
#xdata = 1-based index
#ydata = data
#func = function to fit

def func(x,a,b,c):
    """defines a negative exponential function"""
    return a * np.exp(-b*x) + c
def e_inflection_finder(params):
    """finds the point where the derivative of the negative exponential function is equal to -1"""
    return (np.log(1/(params[1]*params[0])))/(-1*params[1])
popt, pcov = curve_fit(func,xdata,ydata)

#print(popt)

my_inflection = e_inflection_finder(popt)

print(my_inflection)

last_num = round(my_inflection)


with open("67NR_cell_inflec.txt","w") as g:
    for idx, val in enumerate(all_data):
        if idx < last_num:
            g.write(val[0] + "\t" + val[1] + "\n")
        else:
            break
g.close()