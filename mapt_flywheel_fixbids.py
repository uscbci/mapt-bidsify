#!/usr/bin/env python
import argparse
import os
import shutil
from subprocess import call


code_dir = os.path.dirname(os.path.realpath(__file__))
bids_folder = "/Volumes/MAPT/fMRI/BIDS_data/"

allsubjects = os.listdir(bids_folder)
allsubjects.sort()
# to_do = []

# for subject_code in allsubjects:

#     subject_folder = "%s/%s" % (bids_folder,subject_code)
#     inner_folder = "%s/ses-pre" % subject_folder
#     anat_folder = "%s/anat" % inner_folder
#     t1file = "%s/sub-%s_ses-pre_t1w.nii.gz" % (anat_folder,subject_code)
#     print("Checking %s" % t1file )
#     if (not os.path.exists(t1file)):
#         to_do.append(subject_code)

to_do = [elem for elem in allsubjects if "sub-" in elem]

exclude = []

to_do = [elem for elem in to_do if elem not in exclude]


print("Subjects to do:")
print(to_do)

for subject_code in to_do:
    print("Working on subject %s" % subject_code)
    subject_folder = "%s/%s" % (bids_folder,subject_code)
    inner_folders = ["ses-pre","ses-post"]
    subject_code = subject_code[4:]

    for inner_folder in inner_folders:

        inner_folder_path = "%s/%s" % (subject_folder,inner_folder)
        if os.path.exists(inner_folder_path):
            print(" Working on session %s " % inner_folder)

            fmap_folder = "%s/%s/fmap" % (subject_folder,inner_folder)
            
            # Fix capitalization of anatomicals
            src_file = "%s/%s/anat/sub-%s_%s_t1w.json" % (subject_folder,inner_folder,subject_code,inner_folder)
            dest_file = "%s/%s/anat/sub-%s_%s_T1w.json" % (subject_folder,inner_folder,subject_code,inner_folder)
            print("Checking for %s" % src_file)
            if (os.path.exists(src_file)):
                print("Renaming %s to %s" % (src_file,dest_file))
                shutil.move(src_file,dest_file)

            src_file = "%s/%s/anat/sub-%s_%s_t1w.nii.gz" % (subject_folder,inner_folder,subject_code,inner_folder)
            dest_file = "%s/%s/anat/sub-%s_%s_T1w.nii.gz" % (subject_folder,inner_folder,subject_code,inner_folder)
            if (os.path.exists(src_file)):
                print("Renaming %s to %s" % (src_file,dest_file))
                shutil.move(src_file,dest_file)

            src_file = "%s/%s/anat/sub-%s_%s_t2w.json" % (subject_folder,inner_folder,subject_code,inner_folder)
            dest_file = "%s/%s/anat/sub-%s_%s_T2w.json" % (subject_folder,inner_folder,subject_code,inner_folder)
            if (os.path.exists(src_file)):
                print("Renaming %s to %s" % (src_file,dest_file))
                shutil.move(src_file,dest_file)

            src_file = "%s/%s/anat/sub-%s_%s_t2w.nii.gz" % (subject_folder,inner_folder,subject_code,inner_folder)
            dest_file = "%s/%s/anat/sub-%s_%s_T2w.nii.gz" % (subject_folder,inner_folder,subject_code,inner_folder)
            if (os.path.exists(src_file)):
                print("Renaming %s to %s" % (src_file,dest_file))
                shutil.move(src_file,dest_file)

            if (os.path.exists(fmap_folder)):
                print("Working fmap folder %s" % fmap_folder)
                fieldmap_jsons = os.listdir(fmap_folder)
                for jsonfile in fieldmap_jsons:
                    command = "sed -i '' 's/t1w/T1w/g' %s/%s" % (fmap_folder,jsonfile)
                    print(command)
                    call(command,shell=True)
                    command = "sed -i '' 's/t2w/T2w/g' %s/%s" % (fmap_folder,jsonfile)
                    print(command)
                    call(command,shell=True)