'''
Server for package listening
by directory scan

.tar.gz
.tgz

'''
import os
import shutil
import time
import tarfile
import yaml
import db_accessor as db

dir_to_scan = '/home/dmz/packages/'
dir_to_store = '/home/dmz/packages/package_storage/'
tmp_path = dir_to_scan + 'tmp/'
file_type = '.tar.gz'


def unpack_yaml(source_path):
    '''takes in src path of tar.gz, writes pkg yaml to tmp, returns [yaml, path]'''

    # reading pkg.yaml inside package.tar.gz, stores to tmp dir (was easier this way)
    command = f"tar -xf {source_path} -C {tmp_path} pkg.yaml"
    os.system(command)
    pkg_yaml_path = yaml.safe_load(tmp_path + 'pkg.yaml')
    with open(pkg_yaml_path, 'r') as file:
        pkg_yaml = yaml.safe_load(file)

    return [pkg_yaml, pkg_yaml_path]

def process_package(filename):
    '''takes in str filename, mvs file to storage, calls db'''

    # establishing current path and end path
    source_path = dir_to_scan + filename
    destination_path = dir_to_store + filename

    # grab yaml information
    yaml_info = unpack_yaml(source_path)
    pkg_yaml = yaml_info[0]
    pkg_yaml_path = yaml_info[1]

    # send information to database
    db.store_fresh_package(filename, pkg_yaml)

    # clean up
    # mv file from incoming dir to package storage
    shutil.move(source_path, destination_path)
    print("Move Successful")
    # delete tmp yaml
    os.remove(pkg_yaml_path)


# Main Entry #
 
while True:
    for filename in os.listdir(dir_to_scan):
        if filename.endswith(file_type):
            print(f"File Detected: {filename}")
            process_package(filename)
        else:
            print("No files..")
    time.sleep(5)
