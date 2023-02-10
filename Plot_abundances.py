#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 18:18:50 2023

@author: francesco

Code Plotting the final abundances from Mumpower and from SkyNet using both 
JINA REACLIB and the TALYS rates
"""

import numpy as np
import matplotlib.pyplot as plt

# location of the final SkyNet output files
output_dir = 'output/'

# location of the final SkyNet abundances calculated with plain JINA REACLIB
REACLIB_final_y_path = 'final_y_b'

# location of the Mumpower final abundances from the Arcones trajectory
Mumpower_final_y_path = 'ppnp2016_Final_abs/c_ya_frdm95_arc07-tr3ye310.dat'

# import TALYS SkyNet abundances
m = 2
omp = 2
DZpart = '_noDZ'
nlds = [1,2,3,4,5,6]
strengths = [1,2,3,4,5,6,7,8]
simulation_strings = []
for nld in nlds:
    for strength in strengths:        
        simulation_strings.append('m' + str(m) + 'n' + str(nld) + 's' + str(strength) + 'o' + str(omp) + DZpart)

SkyNet_abundances = []
for simulation_string in simulation_strings:
    path = output_dir + 'final_y_b_orig_' + simulation_string
    print(path)
    SkyNet_abundances.append(np.loadtxt(path))

# import Mumpower abundances
Mumpower_YvsA = np.loadtxt(Mumpower_final_y_path)
Alist = np.array(list(range(250)))
Ylist = np.zeros_like(Alist, dtype = float)
for row in Mumpower_YvsA:
    Ylist[int(row[1])] += row[2]

# import REACLIB abundances
REACLIB_YvsA = np.loadtxt(REACLIB_final_y_path)

# plot
plt.semilogy(REACLIB_YvsA[:,0],REACLIB_YvsA[:,1], 'k-', label = 'SkyNet')
plt.semilogy(Alist,Ylist, 'r-', label = 'Mumpower')
for i, simulation_string in enumerate(simulation_strings):
    plt.semilogy(SkyNet_abundances[i][:,0], SkyNet_abundances[i][:,1], alpha = 0.5, label = simulation_string)
plt.xlim(0,260)
plt.ylim(1e-9,1e-1)
plt.grid()
plt.legend()
plt.show()
