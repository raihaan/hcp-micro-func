#!/bin/bash

nmf_results=$1
python convert.py $nmf_results
for c in $(dirname $nmf_results)/*txt; do wb_command -cifti-convert -from-text $c ../../../raw_data/atlas_files/Schaeffer_template.pscalar.nii $(dirname $c)/$(basename $c .txt).pscalar.nii; done
python plot_Hweights.py --nmf_weights $nmf_results --out_dir $(dirname $nmf_results)
