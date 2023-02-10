#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 07:26:15 2023

@author: francesco

Script running SkyNet for the 48 combinations of NLD and GSF, in parallel.
The different modified reaclib files are created by the make_reaclibs.py code.
"""

from SkyNet import *
import numpy as np
import multiprocessing

def run_skynet(args):
    # location of the history files of the different trajectories
    input_dir = "reaclibs/"

    # location of the final SkyNet output files
    output_dir = "output/"
    
    Ye0 = 0.31   # initial Ye
    t0 = 0.00200762    #initial time
    Temp0 = 2.0    # initial temperature in GK
    s0 = 30.0    # initial entropy in k_B / baryon
    tau = 70.0   # expansion timescale in ms
    tfinal = 3.98 #final time
    
    simulation_string = args
    
    reaclib_name = 'reaclib_' + simulation_string
    traj_path = 'ppnp2016_trajs/c_th_arc07tr3y310_extended'
    time_col = 0
    dens_col = 2
    temp_col = 1
    
    nuclib = NuclideLibrary.CreateFromWinv(SkyNetRoot + "/data/winvn_v2.0.dat")
    opts = NetworkOptions()
    opts.ConvergenceCriterion = NetworkConvergenceCriterion.Mass
    opts.MassDeviationThreshold = 1.0E-10
    opts.IsSelfHeating = False
    opts.EnableScreening = True
    screen = SkyNetScreening(nuclib)
    helm = HelmholtzEOS(SkyNetRoot + "/data/helm_table.dat")
    
    strongReactionLibrary = REACLIBReactionLibrary(input_dir + reaclib_name,
                                                   ReactionType.Strong, 
                                                   True, 
                                                   LeptonMode.TreatAllAsDecayExceptLabelEC,
                                                   "Strong reactions", 
                                                   nuclib, 
                                                   opts, 
                                                   True)
    symmetricFission = REACLIBReactionLibrary(SkyNetRoot + "/data/netsu_panov_symmetric_0neut", 
                                              ReactionType.Strong, 
                                              False,
                                              LeptonMode.TreatAllAsDecayExceptLabelEC,
                                              "Symmetric neutron induced fission with 0 neutrons emitted", 
                                              nuclib, 
                                              opts,
                                              False)
    spontaneousFission = REACLIBReactionLibrary(SkyNetRoot + "/data/netsu_sfis_Roberts2010rates", 
                                                ReactionType.Strong, 
                                                False,
                                                LeptonMode.TreatAllAsDecayExceptLabelEC, 
                                                "Spontaneous fission", 
                                                nuclib, 
                                                opts,
                                                False)
    
    # use only REACLIB weak rates
    weakReactionLibrary = REACLIBReactionLibrary(input_dir + reaclib_name,
                                                 ReactionType.Weak, 
                                                 False, 
                                                 LeptonMode.TreatAllAsDecayExceptLabelEC,
                                                 "Weak reactions", 
                                                 nuclib, 
                                                 opts, 
                                                 True)
    
    reactionLibraries = [weakReactionLibrary, strongReactionLibrary, symmetricFission, spontaneousFission]
    
    net = ReactionNetwork(nuclib, 
                          reactionLibraries, 
                          helm, 
                          screen, 
                          opts)
    
    dat = np.loadtxt(traj_path)
    density_vs_time = PiecewiseLinearFunction(dat[:,time_col], dat[:,dens_col], True)
    temperature_vs_time = PiecewiseLinearFunction(dat[:,time_col], dat[:,temp_col], True)
    
    
    
    Outputfile_name = output_dir + 'output_b_orig_' + simulation_string
    output = net.EvolveFromNSE(t0, 
                            tfinal, 
                            temperature_vs_time, 
                            density_vs_time,
                            Ye0, 
                            Outputfile_name)
    
    NetworkOutput.MakeDatFile(Outputfile_name + ".h5")
    
    YvsA = np.array(output.FinalYVsA())
    A = np.arange(len(YvsA))
    
    np.savetxt(output_dir + "final_y_b_orig_" + simulation_string, 
               np.array([A, YvsA]).transpose(),
               "%6i  %30.20E")

if __name__ == '__main__':
    m = 2
    omp = 2
    DZpart = '_noDZ'
    nlds = [1,2,3,4,5,6]
    strengths = [1,2,3,4,5,6,7,8]
    simulation_strings = []
    for nld in nlds:
        for strength in strengths:
            simulation_strings.append('m' + str(m) + 'n' + str(nld) + 's' + str(strength) + 'o' + str(omp) + DZpart)
    
    num_cores = multiprocessing.cpu_count()
    print("Running with %i worker threads" % num_cores)
    pool = multiprocessing.Pool(num_cores)
    
    args = simulation_strings
    pool.map_async(run_skynet, args)
    
    # done submitting jobs
    pool.close()
    pool.join()