import os
import sys
import numpy as np
import pandas as pd
import scipy


df_demo = pd.read_csv('../raw_data/merged_sorted_r277_unrelated_setA_n384.csv')
subjects_list = df_demo['Subject'].values.tolist()
print(len(subjects_list)) #check
num_roi = 400

for s in subjects_list: #load data
    mpc = np.loadtxt(str(s) + "/mpc/" + str(s) + "_mpc.txt")
    func = np.loadtxt(str(s) + "/rsfc/" + str(s) + ".rfMRI_REST1.netmat.txt")
    np.fill_diagonal(func,0)

    #compute coupling coefficient (row by row corr of mpc and func)
    coupling = np.zeros((num_roi,1))
    for roi in range(0,num_roi):
        coupling[roi,0] = np.corrcoef(mpc[roi,:],func[roi,:])[0,1]
    #writeout
    np.savetxt(str(s) + "/struct-func/" + str(s) + "_mpc_avgfc_coupling.txt",
               coupling.astype('float32'),delimiter='\t',fmt='%.7f')
    del mpc, func, coupling

for s in subjects_list: #load data
    mpc = np.loadtxt(str(s) + "/mpc/" + str(s) + "_mpc.txt")
    func = np.loadtxt(str(s) + "/rsfc/" + str(s) + ".REST1.demean.varnorm.netmat.txt")
    np.fill_diagonal(func,0)

    #compute coupling coefficient (row by row corr of mpc and func)
    coupling = np.zeros((num_roi,1))
    for roi in range(0,num_roi):
        coupling[roi,0] = np.corrcoef(mpc[roi,:],func[roi,:])[0,1]
    #writeout
    np.savetxt(str(s) + "/struct-func/" + str(s) + "_mpc_concatfc_coupling.txt",
               coupling.astype('float32'),delimiter='\t',fmt='%.7f')
    del mpc, func, coupling
