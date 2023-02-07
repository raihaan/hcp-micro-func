import os
import sys
import numpy as np
import scipy
from scipy.io import loadmat, savemat

res = loadmat(sys.argv[1])
out_dir = os.path.dirname(sys.argv[1])
print(out_dir)
#need to load in .mat results file, write out one .txt file per component
for c in range(0,np.shape(res['W'])[1]):
    scores = res['W'][:,c]
    np.savetxt(out_dir + '/c' + str(c+1) + '.txt',
               scores.astype('float32'),delimiter='\\t',fmt='%.7f')
    
