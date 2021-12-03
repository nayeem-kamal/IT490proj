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
import sendpkg as send

dir_to_scan = '/home/deploy/packages/incoming/'
dir_to_store = '/home/deploy/packages/package_storage/'
tmp_path = dir_to_scan + 'tmp/'

new_pkg_type = '.tar.gz'
rollback_type = '.rb.yaml'
pass_type = '.pass.yaml'
fail_type = '.fail.yaml'
log_path = '/home/deploy/packages/pack.log'


def emit_log(filename, new=False, rollback=False, passed=False, failed=False):
    '''emits logs to log_path'''

    time = datetime.datetime.now().ctime()
    if new:
        with open(log_path, 'a') as file:
            file.write(f'New Package Detected: {filename} - {time}\n')

    if rollback:
        with open(log_path, 'a') as file:
            file.write(f'Rollback Detected: {filename} - {time}\n')

    if passed:
        with open(log_path, 'a') as file:
            file.write(f'Passed Packaged Detected: {filename} - {time}\n')

    if failed:
        with open(log_path, 'a') as file:
            file.write(f'Failed Package Detected: {filename} - {time}\n')


def send_revert(filename):
    '''
    probably socket connect which sends revert message
    to a command line tool
    '''
    pass


def new_package(filename):
    '''
    takes in str filename, mvs file to storage, store pkg info db
    if destination node is ready for a new pkg, send new package
    '''

    emit_log(filename, new=True)

    if db.does_pkg_exist(filename):
        db.emit_log('Duplicate name detected, removing..')
        os.remove(dir_to_scan+filename)
    else:
        node_ready = db.store_fresh_package(filename)

        if node_ready['ready']:
            db.emit_log(f"{node_ready['node']} is ready, now sending..")
            send.send_next_qa(node_ready['node'])
        else:
            db.emit_log(f"{node_ready['node']} currently not ready.")

def process_rollback(filename):
    pass


def passed_package(filename):
    '''sets the given package to passed, then sends package to prod'''
    db.set_passed_package(filename)


def failed_package(filename):
    pass


# Main Entry #
# process package that is either new, passed or failed
while True:
    try:
        for filename in os.listdir(dir_to_scan):
            if filename.endswith(new_pkg_type):
                new_package(filename)
            elif filename.endswith(rollback_type):
                emit_log(filename, rollback=True)
                process_rollback(filename)
            elif filename.endswith(pass_type):
                emit_log(filename, passed=True)
                passed_package(filename)
                send.send_next_prod(filename)
            elif filename.endswith(fail_type):
                emit_log(filename, failed=True)
                failed_package(filename)
            else:
                print("No files..")
    except Exception as e:
        print(e)
        print(traceback.format_exc())

    time.sleep(5)
