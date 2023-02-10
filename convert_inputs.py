#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 11:09:50 2023

@author: francesco
"""

import numpy as np
from utils import ZandA2Name, search_string_in_file
import matplotlib.pyplot as plt

#a or c?
is_a = 1

if is_a:
    mumpower_traj = 'ppnp2016_trajs/a_th0_30_70_30_.20'
else:
    mumpower_traj = 'ppnp2016_trajs/c_th_arc07tr3y310'


#Convert init_Y from Mumpower to winv order
winve = '/home/francesco/skynet_install/data/winvn_v2.0.dat'
mumpower_Y = 'ppnp2016_trajs/a_init_0_30_70_30_.20'
#mumpower_traj = 'ppnp2016_trajs/a_th0_30_70_30_.20'
mumpower_traj = 'ppnp2016_trajs/c_th_arc07tr3y310'
new_Y_filename = 'ppnp2016_trajs/a_new_init_0_30_70_30_.20'
'''
#skynet version that works
sunet_path = 'sunet'
sunet_matr = np.genfromtxt(sunet_path, dtype = str)
init_Y_skynet_path = 'init_Y'
init_Y_skynet_matrix = np.loadtxt(init_Y_skynet_path)


winve_matr = np.genfromtxt(winve, dtype = str, skip_header=2, skip_footer=39263-7854)
mumpower_Y_matr = np.loadtxt(mumpower_Y)
new_mumpower_Y = np.zeros_like(init_Y_skynet_matrix)

for line in mumpower_Y_matr:
    nuclide_name = ZandA2Name(line[1], line[0], invert = True, particle_names = True)
    print(nuclide_name)
    nuclide_index = np.where(sunet_matr == nuclide_name.lower())[0][0]
    
    
    
    new_mumpower_Y[nuclide_index] = line[2]

np.savetxt(new_Y_filename, new_mumpower_Y/sum(new_mumpower_Y))

print(sum(new_mumpower_Y/sum(new_mumpower_Y)))

init_Y_from_skynet = np.loadtxt('init_Y')
print(sum(init_Y_from_skynet))
'''

#forlenge trajectory
t_final = 1e9
traj = np.loadtxt(mumpower_traj)

time_vector_log = np.linspace(np.log(traj[-1,0]), np.log(t_final))
time_vector = np.exp(time_vector_log)




last_bit = traj[traj[:,0]>1.6, :]
x_list = np.log(last_bit[:,0])
temp_list = np.log(last_bit[:,1])
rho_list = np.log(last_bit[:,2])

model_rho = np.polyfit(x_list, rho_list, 1)
rho_log = model_rho[0]*time_vector_log + model_rho[1]
rho_extrap = np.exp(rho_log)

model_temp = np.polyfit(x_list, temp_list, 1)
temp_log = model_temp[0]*time_vector_log + model_temp[1]
temp_extrap = np.exp(temp_log)


plt.plot(traj[:,0], traj[:,2])
plt.plot(time_vector,rho_extrap)

plt.yscale('log')
plt.xscale('log')
plt.show()

extrapolated_traj = np.c_[time_vector, temp_extrap, rho_extrap]

new_traj = np.concatenate((traj[:,:-1],extrapolated_traj[1:,:]))

np.savetxt(mumpower_traj + '_extended', new_traj)






