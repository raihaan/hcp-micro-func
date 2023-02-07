##imports
import os
import sys
import numpy as np
import scipy
from scipy.io import savemat, loadmat
import sklearn
from sklearn.decomposition import NMF
from sklearn import preprocessing

input_fname = sys.argv[1]
compnum = int(sys.argv[2])
res_dir = sys.argv[3]
res_base = sys.argv[4]  
X_raw = loadmat(input_fname)['X']

X_nmf = X_raw - np.min(X_raw) #make non negative

#run nmf
model = NMF(n_components=compnum, init='nndsvd', max_iter=1000000)
#model = NMF(n_components=compnum, init='nndsvd', max_iter=10000)
model.fit(np.asmatrix(X_nmf))
W_vox = model.fit_transform(np.asmatrix(X_nmf)) # spatial components - each col of W is a component
H_subj = model.components_ #subject-metric weights, describing patterns of each comp

print(compnum, np.shape(W_vox), model.reconstruction_err_, model.n_iter_)

res={}
res['W']=W_vox
res['H']=H_subj
res['err']=model.reconstruction_err_
res['iter']=model.n_iter_
res['comp']=compnum
#save results
fname=res_dir + "/" + res_base + ".mat"
#hdf5storage.savemat(fname, res, format='7.3', options=options)
savemat(fname, res)
