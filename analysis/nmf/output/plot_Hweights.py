## LOAD MODULES/SOFTWARE
import os
import glob
import pandas as pd
import numpy as np

import sys
import pickle
import scipy
from scipy.io import savemat, loadmat
from scipy import stats

import matplotlib as mpl
from matplotlib import cm
from matplotlib.ticker import MultipleLocator, FormatStrFormatter, FixedFormatter, FixedLocator
from matplotlib import pyplot as plt
import argparse

parser=argparse.ArgumentParser(
    description='''This script outputs a .png file containing a heatmap of input nmf matrix data''')

group = parser.add_argument_group(title="Execution options")

group.add_argument(
    '--nmf_weights', help='.mat file containing nmf results',required=True)
group.add_argument(
    '--out_dir', help='.mat file containing nmf results',required=True)
group.add_argument(
    '--minimum', type=float, help='min value',required=False)
group.add_argument(
    '--maximum', type=float, help='max value',required=False)
group.add_argument(
    '--width', type=float, help='figure width',required=False,default=16)
group.add_argument(
    '--height', type=float, help='figure height',required=False,default=8)

args=parser.parse_args()

h=loadmat(args.nmf_weights)['H']
n_components = np.shape(h)[0]

#heat mapping for H matrix
def heatmapping(data,minn,maxx,cbar_tix,fig_width,fig_height,title='',fname=''):
    import matplotlib as mpl
    from matplotlib import cm
    from matplotlib.ticker import MultipleLocator, FormatStrFormatter, FixedFormatter, FixedLocator
    plt.rc('figure', titlesize=30)  # fontsize of the figure title
    #Linearly interpoalte a colour gradient 
   
    viridis = cm.get_cmap('viridis', 256)
    newcolors = viridis(np.linspace(0, 1, 256))
    cmap = mpl.colors.ListedColormap(newcolors)
    img = plt.imshow(data,interpolation='nearest', \
    cmap = cmap, origin='upper',vmin=minn,vmax=maxx)
    #Set the axis of the plot so it isn't a long rectangle
    ax = plt.gca()
    ax.set_aspect('auto') #use 'auto' for automatic aspect
    ax.tick_params(axis='both',which='both',bottom='off',top='off',labelbottom='on',left='on',labelleft='on', pad = 5)
    ax.set_xlabel('')
    ax.set_ylabel('Components', fontsize=40)
    ax.yaxis.set_ticklabels([])
    ax.yaxis.labelpad = 5
    ax.tick_params(axis='y',size=15)
    ax.grid(False)
    fig = plt.gcf()
    fig.set_size_inches(fig_width,fig_height)
    cbar = plt.colorbar(img,cmap=cmap)
    
    cbar.set_ticks(np.arange(minn, maxx, cbar_tix))
    cbar.ax.tick_params(labelsize=30)
    if title:
        plt.title(title, fontsize=30)
    plt.savefig(fname, bbox_inches='tight')
    plt.close() 

#plot zscored H
h_z=scipy.stats.zscore(h,axis=1)
fname = args.out_dir + '/H_k' + str(n_components) + '_zscore_components.png'
heatmapping(h_z,-2.5,2.50001,2.5,args.width,args.height,title="Hweights",fname=fname)    


#plot mean normalized H
h_norm=np.zeros_like(h)
for r in range(0,np.shape(h)[0]):
    row_avg = np.mean(h[r,:])
    for c in range(0,np.shape(h)[1]):
        h_norm[r,c] = h[r,c]/row_avg

if args.minimum is None:
    args.minimum = 0.75

if args.maximum is None:
    args.maximum = 1.25
fname = args.out_dir + '/H_k' + str(n_components) + '_meannormalize.png'
heatmapping(h_norm,args.minimum,args.maximum+0.0001,0.25,args.width,args.height,title="Hweights",fname=fname)    

#plot raw h
nticks=2
raw_minn=np.percentile(h,0.01)
raw_maxx=np.percentile(h,99.99)
#space = np.floor((raw_maxx - raw_minn)/nticks)
space = (raw_maxx - raw_minn)/nticks
fname = args.out_dir + '/H_k' + str(n_components) + '_raw.png'
heatmapping(h,raw_minn,raw_maxx,space,args.width,args.height,title="Hweights",fname=fname)

mask =  np.tri(h.shape[0], k=-1)
mx_k4_lower = np.ma.array(np.corrcoef(h), mask=mask).T 
np.fill_diagonal(mx_k4_lower,1)
fig, ax = plt.subplots(figsize=(8,8))
im=ax.imshow(mx_k4_lower,vmin=-0.5,vmax=0.5,cmap='coolwarm')

n_comps = np.shape(h)[0]
components_list = []
for c in range(0,n_comps):
    components_list.append('C'+str(c+1))
#components_list = ['C1','C2','C3','C4']
ax.set_xticks(np.arange(len(components_list)))
ax.set_yticks(np.arange(len(components_list)))
# ... and label them with the respective list entries
ax.set_xticklabels(components_list)
ax.set_yticklabels(components_list)
cbar = fig.colorbar(im,ax=ax,shrink=0.7)
cbar.ax.tick_params(labelsize=30)
ax.tick_params(axis='both', labelsize=45)

# Loop over data dimensions and create text annotations.
for i in range(n_comps):
    for j in range(n_comps):
        text = ax.text(j, i, np.round(mx_k4_lower[i, j],decimals=2),
                       ha="center", va="center", color="k", fontsize=35)
fname = args.out_dir + '/H_k' + str(n_components) + '_corr.png'
plt.savefig(fname, bbox_inches='tight')
