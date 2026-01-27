#!/usr/bin/env python
import flywheel
import argparse
from subprocess import call
import os

#Command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("api_key_file", help="file that has flywheel api key")
args = parser.parse_args()
api_key_file = args.api_key_file
code_dir = os.path.dirname(os.path.realpath(__file__))

with open(api_key_file,'r') as file:
    api_key = file.read().replace('\n','')

#Set up the flywheel API
fw = flywheel.Client(api_key)

#Get the SAGE project
project_id = "64935df4a60b3a64d6add007"
project = fw.get(project_id)

to_exclude = ["12834"]

to_bidsify = []
for subject in project.subjects():
    session = subject.sessions()[0]
    print("subject %s" % subject.code)
    if 'BIDS' in session.info.keys():
        print("BIDS already done")
    else:
        if subject not in to_exclude:
            to_bidsify.append(subject.code)
        else:
            print("Excluding this subject")


print("The following subjects will need to have the Curate BIDS gear run:")
print(to_bidsify)

for subject in to_bidsify:
    # Do BIDS curation on flywheel
    command = "%s/sage_flywheel_bids_gear.py %s %s" % (code_dir,subject,api_key)
    print(command)
    call(command,shell=True)

    # Download the BIDS-curated data
    command = "%s/sage_flywheel_export_bids.py %s %s" % (code_dir,subject,api_key)
    print(command)
    call(command,shell=True)

    # Fix BIDS-curated data to meet validation standards
    command = "%s/sage_flywheel_fixbids.py %s" % (code_dir,subject)
    print(command)
    call(command,shell=True)

