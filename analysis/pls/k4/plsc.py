import sys
import os
from pyls import behavioral_pls
import numpy as np
import pandas as pd

# Import the two matrices

my_data={}
my_data['X'] = pd.read_csv(sys.argv[1])
my_data['Y'] = pd.read_csv(sys.argv[2])
my_data['n_boot'] = int(sys.argv[3])
my_data['n_perm'] = int(sys.argv[4])
my_data['n_proc']='max'

#X = numpy_array_with_matrix_X
#Y = numpy_array_with_matrix_Y

# Create a directory in which to save the outputs
# note that if output_dir already exists, your run will stop here. 
#output_dir = “/path/to/directory/where/you/save/PLS/outputs”
output_dir = sys.argv[5]

if not os.path.exists(output_dir): #make output directory
    try:
        os.makedirs(output_dir)
    except OSError as exc:
        if exc.errno == errno.EEXIST:
            pass
        else:
            raise 
#os.mkdir(f“{output_dir}")

#do checks
print('X is')
print(my_data['X'].head())
print('Y is')
print(my_data['Y'].head())
print(my_data['n_boot'], "bootstraps and", my_data['n_perm'], "permutations")
print("saving to", output_dir)

# Run plsc
bpls = behavioral_pls(**my_data)
#bpls = behavioral_pls(X,Y, n_perm = desired_number_of_permutations, n_boot = desired_number_of_bootstrap_resamplings, n_proc = number_of_desired_processors)
# n_proc can be set to ‘max’ on niagara

np.savetxt(f'{output_dir}/x_weights.csv', bpls['x_weights'], delimiter=',') # p x m
np.savetxt(f'{output_dir}/y_weights.csv', bpls['y_weights'], delimiter=',') # m x m
np.savetxt(f'{output_dir}/x_scores.csv', bpls['x_scores'], delimiter=',') # n x m
np.savetxt(f'{output_dir}/y_scores.csv', bpls['y_scores'], delimiter=',') # n x m
np.savetxt(f'{output_dir}/y_loadings.csv', bpls['y_loadings'], delimiter=',') # m x m 
np.savetxt(f'{output_dir}/sinvals.csv', bpls['singvals'], delimiter=',') # (m,)
np.savetxt(f'{output_dir}/varexp.csv', bpls['varexp'], delimiter=',') # (m,)
np.savetxt(f'{output_dir}/permres_pvals.csv', bpls['permres']['pvals'], delimiter=',') # shape: (m,)
np.savetxt(f'{output_dir}/permres_permsamples.csv', bpls['permres']['permsamples'], delimiter=',') 
np.savetxt(f'{output_dir}/bootres_x_weights_normed.csv', bpls['bootres']['x_weights_normed'], delimiter=',') 
np.savetxt(f'{output_dir}/bootres_x_weights_stderr.csv', bpls['bootres']['x_weights_stderr'], delimiter=',')
np.savetxt(f'{output_dir}/bootres_bootsamples.csv', bpls['bootres']['bootsamples'], delimiter=',')
np.savetxt(f'{output_dir}/bootres_y_loadings.csv', bpls['bootres']['y_loadings'], delimiter=',')

# to save your bootstrapped samples (for the very, very cautious)
#os.mkdir(f'{output_dir}/y_loadings_boot')
#for i in range(bpls['bootres']['y_loadings_boot'].shape[0]):
#    np.savetxt(f'{output_dir}/y_loadings_boot/bootres_y_loadings_boot_{i}.csv', bpls['bootres']['y_loadings_boot'][i], delimiter=',')

# saving your confidence intervals 
os.mkdir(f'{output_dir}/y_loadings_ci')
for i in range(bpls['bootres']['y_loadings_ci'].shape[0]):
    np.savetxt(f'{output_dir}/y_loadings_ci/bootres_y_loadings_ci_behaviour_{i}.csv', bpls['bootres']['y_loadings_ci'][i], delimiter=',')

np.savetxt(f'{output_dir}/cvres_pearson_r.csv', bpls['cvres']['pearson_r'], delimiter=',') 
np.savetxt(f'{output_dir}/cvres_r_squared.csv', bpls['cvres']['r_squared'], delimiter=',')

# Saving your input information (makes the code longer, but quite valuable when trouble shooting, or if you've done several runs and want to keep track of the parameters of each):
np.savetxt(f'{output_dir}/inputs_X.csv', bpls['inputs']['X'], delimiter=',')
np.savetxt(f'{output_dir}/inputs_Y.csv', bpls['inputs']['Y'], delimiter=',')
f=open(f'{output_dir}/input_info.txt','w')
f.write(f"Groups: {bpls['inputs']['groups']}\n") # [n]
f.write(f"Num of conditions: {bpls['inputs']['n_cond']}\n") # 1
f.write(f"Num of permutations: {bpls['inputs']['n_perm']}\n") # perm
f.write(f"Bootstrapping: {bpls['inputs']['n_boot']}\n") # boot
f.write(f"Bootstrapping: {bpls['inputs']['test_split']}\n") # default=100
f.write(f"Bootstrapping: {bpls['inputs']['test_size']}\n") # default=0.25
f.write(f"Bootstrapping: {bpls['inputs']['covariance']}\n") # default=False
f.write(f"Rotations: {bpls['inputs']['rotate']}\n") # True
f.write(f"Confidence Intervals: {bpls['inputs']['ci']}\n") # default=95
f.write(f"Verbose: {bpls['inputs']['verbose']}\n") # True
f.close()


