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
import datetime


dir_to_scan = '/home/dmz/packages/incoming_packages/'
dir_to_store = '/home/dmz/packages/package_storage/'
tmp_path = dir_to_scan + 'tmp/'

new_pkg_type = '.tar.gz'
rollback_type = '.yaml'
log_path = '/home/dmz/packages/pack.log'


def emit_log(filename, new=False, rollback=False):
    '''emits logs to log_path'''

    time = datetime.datetime.now().strftime('%m-%d %H:%M:%S')
    if new:
        with open(log_path, 'a') as file:
            file.write(f'New Package Detected: {filename} - {time}')
    if rollback:
        with open(log_path, 'a') as file:
            file.write(f'Rollback Detected: {filename} - {time}')


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
                emit_log(filename, new=True)
                process_package(filename)
            elif filename.endswith(rollback_type):
                emit_log(filename, rollback=True)
                process_rollback(filename)
            else:
                print("No files..")
    except Exception as e:
        print(e)

    time.sleep(5)
