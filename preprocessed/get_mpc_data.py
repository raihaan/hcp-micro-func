import sys
import os
import numpy as np
import pandas as pd
import scipy
from scipy.io import loadmat, savemat

#MPC.mat contains one matrix for each of 1206 HCP subjects
mpc=loadmat('mpc/MPC.mat') #load
print(np.shape(mpc['MPC']) )
#has shape 1206 (nsubjects) x 400 (nregions) x 400 (nregions)
#each row is a subject
print(np.shape(mpc['MPC'][0]))

#load in HCP spreadsheet with all ids
df_demo = pd.read_csv('../raw_data/unrestricted_patelmo6_8_19_2021_8_21_44.csv')
all_subjects = df_demo['Subject'].values
print(len(all_subjects)) #1206 subjects, matches the 1206 in MPC.mat

#write out one .txt file for each subject, even for the subjects with no data (for simplicity)
print(np.shape(mpc['MPC']), np.shape(all_subjects)) #1206 of each
for idx,subj in enumerate(all_subjects):
    out_dir = str(subj) + "/"
    if os.path.exists(out_dir): #if in current analysis set, store in subj dir
        fname = out_dir + "mpc/" + str(subj) + "_mpc.txt"
    else:
        fname = "mpc/" + str(subj) + "_mpc.txt"
    mpc_data = mpc['MPC'][idx]
    print("saving index", idx, "to", fname," with shape", np.shape(mpc_data))
    np.savetxt(fname,mpc_data.astype('float32'),delimiter='\t',fmt='%.7f')
