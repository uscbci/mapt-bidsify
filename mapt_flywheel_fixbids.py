#!/usr/bin/env python
import argparse
import os
import shutil
from subprocess import call


code_dir = os.path.dirname(os.path.realpath(__file__))
bids_folder = "/Volumes/MAPT/fMRI/BIDS_data/"

allsubjects = os.listdir(bids_folder)
allsubjects.sort()
print("Will check these:")
print(allsubjects)
to_do = []

for subject_code in allsubjects:

    subject_folder = "%s/%s" % (bids_folder,subject_code)
    inner_folder = "%s/ses-KaplanMAPT" % subject_folder
    anat_folder = "%s/anat" % inner_folder
    t1file = "%s/sub-%s_ses-KaplanMAPT_t1w.nii.gz" % (anat_folder,subject_code)
    print("Checking %s" % t1file )
    if (not os.path.exists(t1file)):
        to_do.append(subject_code)

to_do = [elem for elem in to_do if "sub-" in elem]

exclude = []

to_do = [elem for elem in to_do if elem not in exclude]


print("Subjects to do:")
print(to_do)
to_do = ["sub-03191"]

for subject_code in to_do:
    subject_folder = "%s/%s" % (bids_folder,subject_code)
    inner_folder = "%s/ses-KaplanMAPT" % subject_folder
    fmap_folder = "%s/fmap" % inner_folder

    subject_code = subject_code[4:]

    # Fix capitalization of anatomicals
    src_file = "%s/anat/sub-%s_ses-KaplanMAPT_t1w.json" % (inner_folder,subject_code)
    dest_file = "%s/anat/sub-%s_ses-KaplanMAPT_T1w.json" % (inner_folder,subject_code)
    if (os.path.exists(src_file)):
        shutil.move(src_file,dest_file)

    src_file = "%s/anat/sub-%s_ses-KaplanMAPT_t1w.nii.gz" % (inner_folder,subject_code)
    dest_file = "%s/anat/sub-%s_ses-KaplanMAPT_T1w.nii.gz" % (inner_folder,subject_code)
    if (os.path.exists(src_file)):
        shutil.move(src_file,dest_file)

    src_file = "%s/anat/sub-%s_ses-KaplanMAPT_t2w.json" % (inner_folder,subject_code)
    dest_file = "%s/anat/sub-%s_ses-KaplanMAPT_T2w.json" % (inner_folder,subject_code)
    if (os.path.exists(src_file)):
        shutil.move(src_file,dest_file)

    src_file = "%s/anat/sub-%s_ses-KaplanMAPT_t2w.nii.gz" % (inner_folder,subject_code)
    dest_file = "%s/anat/sub-%s_ses-KaplanMAPT_T2w.nii.gz" % (inner_folder,subject_code)
    if (os.path.exists(src_file)):
        shutil.move(src_file,dest_file)

    fieldmap_jsons = os.listdir(fmap_folder)
    for jsonfile in fieldmap_jsons:
        command = "sed -i '' 's/t1w/T1w/g' %s/%s" % (fmap_folder,jsonfile)
        print(command)
        call(command,shell=True)
        command = "sed -i '' 's/t2w/T2w/g' %s/%s" % (fmap_folder,jsonfile)
        print(command)
        call(command,shell=True)