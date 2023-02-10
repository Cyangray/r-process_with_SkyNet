#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 11:00:40 2020

@author: francesco

Script replacing REACLIB neutron-capture coefficients with coefficients yielding
TALYS neutron-capture rates. It requires a dataset of TALYS calculated n-capture rates.
Under input, put for which parameter combination the script will go through.
"""

import numpy as np
from readlib import *
import time
import shutil

#input
nldmodels = [1,2,3,4,5,6]
strengthmodels = [1,2,3,4,5,6,7,8]
massmodels = [2]
ompmodels = [2]         #two options: 1 and 2. 1 for jlmomp-y and 2 for localomp-n

#Nuclei. The ones that don't exist, are automatically skipped, and a message is printed.
nucs = list(range(26,107))       #isotope from which to extract strength function. one, or a series of names, or Zs
As = list(range(58,185))        #mass number of isotope

ds_location = '/home/francesco/Documents/Talys-calculations/'
tic = time.perf_counter()
for nld in nldmodels:
    for strength in strengthmodels:
        for m in massmodels:
            for omp in ompmodels:
                DZpart = '_noDZ'
                reaclib_name = 'reaclib_' + 'm' + str(m) + 'n' + str(nld) + 's' + str(strength) + 'o' + str(omp) + DZpart
                shutil.copy('reaclib', reaclib_name)
                for nucleus in nucs:
                    for A in As:
                        try:
                            reaclib_replace(nucleus, A, nld, m, strength, omp, replace = True, input_file = reaclib_name, ds_location = ds_location)
                            print('Z: ' + str(nucleus) + ', A: ' + str(A) + ', success.')
                        except:
                            print('Z: ' + str(nucleus) + ', A: ' + str(A) + ', not found.')
toc = time.perf_counter()
el_time = toc-tic
print('time: ' + str(el_time))
