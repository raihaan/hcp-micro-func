#!/bin/bash

# ====================================================================== #
# 2021_03_12 Raihaan Patel
# Creates individual command list file that is submitted by qbatch
# run per subject: for subj in ../raw_data/functional/??????; do ./rsfc_preproc.sh $subj; done
# can then do the following to submit joblists for each subj: 
# for file in ??????/*joblist; do echo bash $file; done > rsfcpreproc_joblist
# and
# module load cobralab/2019b
# qbatch -w 00:30:00 -c 400 preproc_joblist
#
# Performs commands needed to parcellate rsfc surface data according to an atlas
# Mean rsfc in each region is taken
# outputs pscalar.nii file containing mean rsfc in each region, and .txt file containing the vals per region for more general processing
#
# ====================================================================== #

#set vars, just 1 var - input id
input=$1
subj=$(basename $input)
rsfc_out_dir="${subj}/rsfc/"
joblist="${subj}/${subj}.joblist"
#make output dir 
mkdir -p $rsfc_out_dir

#set some paths to raw data
raw_func_dir="../raw_data/functional/${subj}/MNINonLinear/Results/"
#raw_struct_dir="../raw_data/structural/"
#set path to dir with cifti atlases for parcellating
atlas_dir="../raw_data/atlas_files/"



#define input files
atlas_file="${atlas_dir}/Parcellations/HCP/fslr32k/cifti/Schaefer2018_400Parcels_7Networks_order.dlabel.nii"
#atlas_file="${atlas_dir}/Q1-Q6_RelatedValidation210.CorticalAreas_dil_Final_Final_Areas_Group_Colors.32k_fs_LR.dlabel.nii"
#left_surface="${raw_struct_dir}/${subj}/T1w/fsaverage_LR32k/${subj}.L.midthickness_MSMAll.32k_fs_LR.surf.gii"
#right_surface="${raw_struct_dir}/${subj}/T1w/fsaverage_LR32k/${subj}.R.midthickness_MSMAll.32k_fs_LR.surf.gii"

touch ${joblist}

#compute mean time series of each parcel
#use weighted avg based on surface file/vertex area
#create rsfc mx from parcellated tseries (parcel-parcel connectivity mx)
#convert to txt for general analysis
for rs_run in {rfMRI_REST1_LR,rfMRI_REST1_RL}
do
echo wb_command -cifti-parcellate ${raw_func_dir}/${rs_run}/${rs_run}_Atlas_MSMAll_hp2000_clean.dtseries.nii ${atlas_file} COLUMN ${rsfc_out_dir}/${subj}.${rs_run}.ptseries.nii >> ${joblist}
echo wb_command -cifti-correlation -mem-limit 2 ${rsfc_out_dir}/${subj}.${rs_run}.ptseries.nii ${rsfc_out_dir}/${subj}.${rs_run}.netmat.pconn.nii -fisher-z >> ${joblist}
echo wb_command -cifti-convert -to-text ${rsfc_out_dir}/${subj}.${rs_run}.netmat.pconn.nii ${rsfc_out_dir}/${subj}.${rs_run}.netmat.txt >> ${joblist}
done

echo "" >> ${joblist}
#average LR and RL time series to compute 1 netmat per run
echo wb_command -cifti-average ${rsfc_out_dir}/${subj}.rfMRI_REST1_avg.netmat.pconn.nii -cifti ${rsfc_out_dir}/${subj}.rfMRI_REST1_LR.netmat.pconn.nii -cifti ${rsfc_out_dir}/${subj}.rfMRI_REST1_RL.netmat.pconn.nii >> ${joblist}
echo wb_command -cifti-convert -to-text ${rsfc_out_dir}/${subj}.rfMRI_REST1_avg.netmat.pconn.nii ${rsfc_out_dir}/${subj}.rfMRI_REST1.netmat.txt >> ${joblist}


#now demean and var normalize each session, concatenate, then compute fc based on merged timeseries
for rs_run in {rfMRI_REST1_LR,rfMRI_REST1_RL}
do
echo wb_command -cifti-reduce ${raw_func_dir}/${rs_run}/${rs_run}_Atlas_MSMAll_hp2000_clean.dtseries.nii MEAN ${rsfc_out_dir}/${subj}.${rs_run}.mean.dscalar.nii >> ${joblist}
echo wb_command -cifti-reduce ${raw_func_dir}/${rs_run}/${rs_run}_Atlas_MSMAll_hp2000_clean.dtseries.nii STDEV ${rsfc_out_dir}/${subj}.${rs_run}.stdev.dscalar.nii >> ${joblist}
echo wb_command -cifti-math \'\(x - mean\) \/ stdev\' ${rsfc_out_dir}/${subj}.${rs_run}.demean.varnorm.dtseries.nii -fixnan 0 -var x ${raw_func_dir}/${rs_run}/${rs_run}_Atlas_MSMAll_hp2000_clean.dtseries.nii -var mean ${rsfc_out_dir}/${subj}.${rs_run}.mean.dscalar.nii -select 1 1 -repeat -var stdev ${rsfc_out_dir}/${subj}.${rs_run}.stdev.dscalar.nii -select 1 1 -repeat >> ${joblist}
echo "" >> ${joblist}
done


echo wb_command -cifti-merge ${rsfc_out_dir}/${subj}.REST1.demean.varnorm.dtseries.nii -cifti ${rsfc_out_dir}/${subj}.rfMRI_REST1_LR.demean.varnorm.dtseries.nii -cifti ${rsfc_out_dir}/${subj}.rfMRI_REST1_RL.demean.varnorm.dtseries.nii >> ${joblist}
echo "" >> ${joblist}

echo wb_command -cifti-parcellate ${rsfc_out_dir}/${subj}.REST1.demean.varnorm.dtseries.nii ${atlas_file} COLUMN ${rsfc_out_dir}/${subj}.REST1.demean.varnorm.ptseries.nii >> ${joblist}
echo wb_command -cifti-correlation -mem-limit 2 ${rsfc_out_dir}/${subj}.REST1.demean.varnorm.ptseries.nii ${rsfc_out_dir}/${subj}.REST1.demean.varnorm.netmat.pconn.nii -fisher-z >> ${joblist}
echo wb_command -cifti-convert -to-text ${rsfc_out_dir}/${subj}.REST1.demean.varnorm.netmat.pconn.nii ${rsfc_out_dir}/${subj}.REST1.demean.varnorm.netmat.txt >> ${joblist}
echo "" >> ${joblist}

for rs_run in {rfMRI_REST1_LR,rfMRI_REST1_RL}
do
echo rm ${rsfc_out_dir}/${subj}.${rs_run}.mean.dscalar.nii ${rsfc_out_dir}/${subj}.${rs_run}.stdev.dscalar.nii ${rsfc_out_dir}/${subj}.${rs_run}.demean.varnorm.dtseries.nii >> ${joblist}
done

echo rm ${rsfc_out_dir}/${subj}.REST1.demean.varnorm.dtseries.nii >> ${joblist}

