#!/usr/bin/env python
import argparse
import os
import shutil
from subprocess import call
import re

code_dir = os.path.dirname(os.path.realpath(__file__))
bids_folder = "/Volumes/MAPT/fMRI/BIDS_data/"

allsubjects = os.listdir(bids_folder)
allsubjects = [elem for elem in allsubjects if "." not in elem]
allsubjects.sort()
print("Will check these:")
print(allsubjects)
to_do = []

pattern = "sub-(\d*)_.*"

for subject_code in allsubjects:

    subject_number = subject_code[4:]

    subject_folder = "%s/%s" % (bids_folder,subject_code)

    session_folders = os.listdir(subject_folder)
    for session in session_folders:
        session_folder = "%s/%s" % (subject_folder,session)
        modal_folders = os.listdir(session_folder)
        for modal_folder in modal_folders:
            modal_path = "%s/%s" % (session_folder,modal_folder)
            all_files = os.listdir(modal_path)
            for file in all_files:
                results = re.match(pattern,file)
                fn_subj = results.groups()[0]
                if (fn_subj != subject_number):

                    oldpath = "%s/%s" % (modal_path,file)
                    newfilename = re.sub("\d\d\d+",subject_number,file)
                    newpath = "%s/%s" % (modal_path,newfilename)

                    print("Rename %s to %s" % (oldpath,newpath))
                    shutil.move(oldpath,newpath)
