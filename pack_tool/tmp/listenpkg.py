#!/usr/bin/python3
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
import traceback

dir_to_scan = '/home/dmz/packages/'
dir_to_store = '/home/dmz/packages/package_storage/'
tmp_path = dir_to_scan + 'tmp/'

new_pkg_type = '.tar.gz'
rollback_type = '.yaml'


def send_revert(filename):
    '''
    probably socket connect which sends revert message
    to a command line tool
    '''
    pass


def process_package(filename):
    '''takes in str filename, mvs file to storage, store pkg info db'''

    # check for duplicate pkg, if false send to db
    if db.does_pkg_exist(filename):
        send_revert(filename)
    else:
        db.store_fresh_package(filename)


def process_rollback(filename):
    pass


# Main Entry #

while True:
    try:
        for filename in os.listdir(dir_to_scan):
            if filename.endswith(new_pkg_type):
                print(f"New Package Detected: {filename}")
                process_package(filename)
            elif filename.endswith(rollback_type):
                process_package(filename)
            else:
                print("No files..")
    except Exception as e:
        print(e)

    time.sleep(5)
