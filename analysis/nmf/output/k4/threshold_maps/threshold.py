import os
import sys
import numpy as np

component_fname = sys.argv[1]
thresh=int(sys.argv[2])
component_number = int(sys.argv[3])

component = np.loadtxt(component_fname)
component_thresh = np.zeros_like(component)
print(np.shape(component), thresh)
incluster = np.where(component>np.percentile(component,thresh))
component_thresh[incluster] = 1
np.savetxt(str(thresh) + 'p/c' + str(component_number) + 'thresholded.txt',component_thresh.astype('float32'),delimiter='\\t',fmt='%.7f')
