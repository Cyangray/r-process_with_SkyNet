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
REACLIB_final_y_path = 'final_y_b_orig'

# location of the Mumpower final abundances from the Arcones trajectory
Mumpower_final_y_path = 'ppnp2016_Final_abs/c_ya_frdm95_arc07-tr3ye310.dat'

#divide between microscopic and macroscopic models
nld_microscopic = [4,5,6]
gsf_microscopic = [3,4,5,6,7,8]
plot_hybrid_models = False

# import TALYS SkyNet abundances
m = 2
omp = 2
DZpart = '_noDZ'
nlds = [1,2,3,4,5,6]
strengths = [1,2,3,4,5,6,7,8]
simulation_params = []
simulation_strings = []
for nld in nlds:
    for strength in strengths:
        simulation_params.append([m,nld,strength,omp])
        simulation_strings.append('m' + str(m) + 'n' + str(nld) + 's' + str(strength) + 'o' + str(omp) + DZpart)

SkyNet_abundances = []
for simulation_string in simulation_strings:
    path = output_dir + 'final_y_b_orig_' + simulation_string
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
microscopic_color = 'b'
hybrid_color = 'm'
macroscopic_color = 'r'
for SkyNet_abundance, params, simulation_string in zip(SkyNet_abundances, simulation_params, simulation_strings):
    m,nld,strength,omp = params
    if (nld in nld_microscopic) and (strength in gsf_microscopic):
        color = microscopic_color
        plt.semilogy(SkyNet_abundance[:,0], SkyNet_abundance[:,1], color = color, linestyle = '-', alpha = 0.3)
    elif (nld in nld_microscopic) or (strength in gsf_microscopic):
        if plot_hybrid_models:
            color = hybrid_color
            plt.semilogy(SkyNet_abundance[:,0], SkyNet_abundance[:,1], color = color, linestyle = '-', alpha = 0.3)
    else:
        color = macroscopic_color
        plt.semilogy(SkyNet_abundance[:,0], SkyNet_abundance[:,1], color = color, linestyle = '-', alpha = 0.3)
    # check if NLD and GSF micro or macro, and choose three colours that indicate micro model, hybrid or macro
    #, label = simulation_string)
plt.plot([0],[0],color = microscopic_color, linestyle = '-', label='microscopic')
plt.plot([0],[0],color = macroscopic_color, linestyle = '-', label='macroscopic')
if plot_hybrid_models:
    plt.plot([0],[0],color = hybrid_color, linestyle = '-', label='hybrid')
    
plt.semilogy(REACLIB_YvsA[:,0],REACLIB_YvsA[:,1], 'k-', label = 'SkyNet')
plt.semilogy(Alist,Ylist, 'g-', label = 'Mumpower')

plt.xlim(0,260)
plt.ylim(1e-9,1e-1)
plt.grid()
plt.legend()
plt.show()
