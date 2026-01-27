#!/usr/bin/env python
import argparse
from subprocess import call
import flywheel
import os

#Command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("api_key_file", help="flywheel api key file")
args = parser.parse_args()
# subject_code = args.subject
api_key_file = args.api_key_file

with open(api_key_file,'r') as file:
    api_key = file.read().replace('\n','')

#Set up the flywheel API
fw = flywheel.Client(api_key)

#Get the MAPT project
project_id = "6917882482ed73886201c816"
project = fw.get(project_id)

to_exclude = []

to_bidsify = []
for subject in project.subjects():
    session = subject.sessions()[0]
    print("subject %s" % subject.code)
    if 'BIDS' in session.info.keys():
        print("BIDS already done")
        to_bidsify.append("sub-%s" % subject.code)
    else:
        print("Do BIDS first")


#destination for data to be saved
dest_folder = "/Volumes/MAPT/fMRI/BIDS_data/"

donefolders = os.listdir(dest_folder)
donefolders.sort()
to_bidsify.sort()

numdone = len(to_bidsify)
print("BIDS Done (%d):" % numdone)
print(to_bidsify)

numdone = len(donefolders)
print("Already exported (%d):" % numdone)
print(donefolders)

to_bidsify = [elem for elem in to_bidsify if elem not in donefolders]
numdone = len(to_bidsify)
print("Remaining to export (%d):" % numdone)
print(to_bidsify)

for subject_code in to_bidsify:

    subject_code = subject_code[4:]

    #construct command line command
    command = "fw export bids --project \"MAPT\" --group \"jkaplan\" --subject \"%s\" %s" %(subject_code,dest_folder)

    #run it
    print(command)
    call(command,shell=True)