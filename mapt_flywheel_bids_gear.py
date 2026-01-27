#!/usr/bin/env python
import flywheel
import argparse

#Command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("api_key_file", help="flywheel api key file")
args = parser.parse_args()
api_key_file = args.api_key_file

with open(api_key_file,'r') as file:
    api_key = file.read().replace('\n','')

#Set up the flywheel API
fw = flywheel.Client(api_key)

#Get the SAGE project
project_id = "64935df4a60b3a64d6add007"
project = fw.get(project_id)

#Get the BIDS curation gear
bids_gear = fw.lookup("gears/curate-bids/2.2.12_1.2.26")

#Find the BIDS curation template
for file in project.files:
    if file.name == 'sage_bids_template_0.1.json':
        template_file = file


to_exclude = ["12834"]
to_do = ['sub-13373','sub-13378', 'sub-13381', 'sub-13383', 'sub-13384', 'sub-13385', 'sub-13389', 'sub-13396', 'sub-13399', 'sub-13405', 'sub-13413', 'sub-13433', 'sub-13489', 'sub-13493', 'sub-13510', 'sub-13520', 'sub-13522', 'sub-13524', 'sub-13528', 'sub-13534', 'sub-13536', 'sub-13547', 'sub-13552', 'sub-13557', 'sub-13558', 'sub-13568', 'sub-13575', 'sub-13589', 'sub-13590', 'sub-13598', 'sub-13604', 'sub-13610', 'sub-13612', 'sub-13617', 'sub-13623', 'sub-13626', 'sub-13632', 'sub-13634', 'sub-13645', 'sub-13646', 'sub-13651', 'sub-13654', 'sub-13655', 'sub-13659', 'sub-13660', 'sub-13662', 'sub-13676', 'sub-13682', 'sub-13684', 'sub-13689', 'sub-13691', 'sub-13693', 'sub-13701', 'sub-13707', 'sub-13710', 'sub-13723', 'sub-13738', 'sub-13742', 'sub-13762', 'sub-13766', 'sub-13769', 'sub-13783', 'sub-13810', 'sub-13821', 'sub-13824', 'sub-13844', 'sub-13846', 'sub-13849', 'sub-13852', 'sub-13864', 'sub-13874', 'sub-13898', 'sub-13904', 'sub-13985', 'sub-14087', 'sub-14088', 'sub-14110', 'sub-14124', 'sub-14137']

to_bidsify = []
for subject in project.subjects():
    session = subject.sessions()[0]
    print("subject %s" % subject.code)
    s = "sub-%s" % subject.code
    if s in to_do:
        print("Added")
        to_bidsify.append(subject)
    else:
        print("Not added")

    # if 'BIDS' in session.info.keys():
    #     print("BIDS already done")
    # else:
    #     if subject not in to_exclude:
    #         to_bidsify.append(subject)
    #     else:
    #         print("Excluding this subject")

for subject in to_bidsify:
    print("Working on subject %s" % subject.code)

    #Set up the gear
    analysis_label = "bids curate_3"
    inputs = {'template':template_file}
    dest = subject

    #Run the gear
    job_id = bids_gear.run(analysis_label=analysis_label, inputs=inputs, destination=dest, config={'reset': True})
