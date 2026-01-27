#!/usr/bin/env python
import flywheel
import argparse

#Command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("subject", help="Subject code")
parser.add_argument("api_key_file", help="flywheel api key file")
args = parser.parse_args()
api_key_file = args.api_key_file
subject_code = args.subject

with open(api_key_file,'r') as file:
    api_key = file.read().replace('\n','')

#Set up the flywheel API
fw = flywheel.Client(api_key)

#Get the SAGE project
project_id = "64935df4a60b3a64d6add007"
project = fw.get(project_id)

#Get the BIDS curation gear
classifier_gear = fw.lookup("gears/dicom-mr-classifier")

subjects = ["12913","12942","12950","12953","12957","12958","12972","12973","12975","12981","12988","12990","12991","12993","12997",13003]

for subject_code in subjects:

    print("Working on subject %s" % subject_code)

    for subj in project.subjects():
        if (subj.code == subject_code):
            subject = subj

    session = subject.sessions()[0]
    acqs = session.acquisitions()

    for acq in acqs:

        dicom_file = acq.files[0]
        #Set up the gear
        analysis_label = "classifier"
        inputs = {'dicom': dicom_file}
        dest = subject

        #Run the gear
        job_id = classifier_gear.run(inputs=inputs)
