#!/usr/bin/env python
import argparse
import docker

#Command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("subject", help="subject to be processed")
args = parser.parse_args()
subject_code = args.subject

data_path = "/Users/jonask/fMRI/SAGE/data/sub-%s" % subject_code 

docker_client = docker.from_env()
docker_client.images.pull("bids/validator")


#Docker version
# docker run -ti --rm -v /Users/jonask/fMRI/SAGE/data/sub-13007:/data:ro bids/validator /data