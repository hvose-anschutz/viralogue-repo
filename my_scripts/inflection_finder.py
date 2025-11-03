#!/usr/bin/env 

"""Calculates the inflection point from a list of splice
junctions to determine statistically significant sites.
XDATA is the 1-based index, YDATA is the data to graph, XVALS
are the SJ titles, and func is the function to be fit."""

from scipy.optimize import curve_fit
import numpy as np

ALL_DATA = []
XVALS = []
YDATA = []
XDATA = []
SORT_LIST = False

def func(x,a,b,c):
    """defines a negative exponential function"""
    return a * np.exp(-b*x) + c

def e_inflection_finder(params):
    """finds the point where the derivative of the 
    negative exponential function is equal to -1"""
    return (np.log(1/(params[1]*params[0])))/(-1*params[1]) 

#READ IN DATA
with open("67NR_CSO36658_SJs.txt",
          "r",encoding="utf-8") as f:
    for item in f.readlines():
        my_items = item.strip().split("\t")
        ALL_DATA.append(my_items)

f.close()

if SORT_LIST:
    sorted_data = ALL_DATA.sort(key=lambda x: x[1], reverse=True)
    ALL_DATA = sorted_data

for idx, values in enumerate(ALL_DATA):
    XDATA.append(idx+1)
    XVALS.append(values[0])
    YDATA.append(values[1])

popt, pcov = curve_fit(func,XDATA,YDATA)
my_inflection = e_inflection_finder(popt)
#print(my_inflection)
last_num = round(my_inflection)

with open("67NR_cell_inflec.txt","w",encoding="utf-8") as g:
    for idx, val in enumerate(ALL_DATA):
        if idx < last_num:
            g.write(val[0] + "\t" + val[1] + "\n")
        else:
            break
g.close()
