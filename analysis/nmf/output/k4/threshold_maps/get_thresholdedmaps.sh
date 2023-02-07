#!/bin/bash

for thresh in {50,75,90,95};
do
mkdir -p ${thresh}p
for c in {1,2,3,4};
do
python threshold.py c${c}.txt $thresh $c
wb_command -cifti-convert -from-text ${thresh}p/c${c}thresholded.txt Schaeffer_template.pscalar.nii ${thresh}p/c${c}.${thresh}p.pscalar.nii
done
done

#wb_command -cifti-convert -from-text 75p/c1thresholded.txt Schaeffer_template.pscalar.nii 75p/c1thresholded.pscalar.nii
#python threshold.py c1.txt 75 
