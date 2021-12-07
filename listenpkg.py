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
rollback_ext = '.rb.'
approved_ext = '.appd.'
log_path = '/home/deploy/packages/pack.log'

# establishing on deck paths for QA and PROD
deck_path = '/home/deploy/packages/on_deck/'
deck_paths = {
        'frontend': deck_path+'frontend/',
        'backend': deck_path+'backend/',
        'dmz': deck_path+'dmz/',
        }
prod_deck_path = '/home/deploy/packages/prod_deck/'
prod_deck_paths = {
        'frontend': prod_deck_path+'frontend/',
        'backend': prod_deck_path+'backend/',
        'dmz': prod_deck_path+'dmz/',
        }


def emit_log(message, filename):
    '''emits logs to log_path'''

    time = datetime.datetime.now().ctime()
    with open(log_path, 'a') as file:
        file.write('*********************\n')
        file.write(f'{message}: {filename} - {time}\n')
        file.write('*********************\n')


def new_package(filename):
    '''
    takes in str filename, mvs file to storage, store pkg info db
    if destination node is ready for a new pkg, send new package
    '''

    emit_log('New Package Detected', filename)
    os.system("notify-send 'New Package Detected.'")

    if db.does_pkg_exist(filename):
        db.emit_log('Duplicate name detected, removing..')
        os.remove(dir_to_scan+filename)
    else:
        node_ready = db.store_fresh_package(filename)

        if node_ready['ready']:
            db.emit_log(f"QA {node_ready['node']} is ready, now sending..")
            send.send_next_qa(node_ready['node'])
        else:
            db.emit_log(f"QA {node_ready['node']} currently not ready.")


def approve_package(filename):
    '''sets the given package to approved, then sends package to prod'''

    emit_log('Appd Packaged Detected.', filename)
    os.system("notify-send 'Approved Package Detected.'")

    # if setting pkg approval successful,
    # send next package to given production node
    prod_ready = db.set_package_approval(filename)

    if prod_ready['ready']:
        db.emit_log(f'PROD {prod_ready["node"]} is ready, now sending..')
        send.send_next_prod(prod_ready['node'])
    else:
        db.emit_log(f'PROD {prod_ready["node"]} currently not ready.')

    # if theres a new package for given QA node, send that back to node
    qa_node = prod_ready['node']
    send.send_next_qa(qa_node)


def rollback_package(filename):
    '''
    takes in str:filename of rolled back pkg
    updates pkgstatus in database
    removes any waiting new packages for that node
    '''

    emit_log('Rollback Package Detected', filename)

    with open(dir_to_scan+filename, 'r') as file:
        pkg_yaml = yaml.safe_load(file)

    node = pkg_yaml['sourcenode']
    os.system(f"notify-send -u critical 'Rollback Detected for {node}.'")

    db.rollback_package(pkg_yaml)
    os.remove(dir_to_scan+filename)

def do_nothing():
    pass


def check_deck():
    '''checks deck for waiting packages, attempts to send'''

    # should only be one file if exists
    for key in deck_paths:
        scp_success = False
        file = os.listdir(deck_paths[key])
        if file:
            #emit_log(f'On deck: QA {key}', file[0])
            os.system(f"notify-send -u low 'On deck QA {key}.'")
            try:
                scp_success = db.use_scp(deck_paths[key]+file[0], key, QA=True)

            except Exception as e:
                #db.emit_log(e)
                do_nothing()

            if scp_success:
                emit_log(f'On deck QA {key} sent success.', file[0])
                os.remove(deck_paths[key]+file[0])


def check_prod_deck():
    '''checks deck for waiting packages, attempts to send'''

    # should only be one file if exists
    for key in prod_deck_paths:
        scp_success = False
        file = os.listdir(prod_deck_paths[key])
        if file:
            #emit_log(f'On deck PROD {key}', file[0])
            os.system(f"notify-send -u low 'On deck PROD {key}.'")
            try:
                scp_success = db.use_scp(prod_deck_paths[key]+file[0], key, PROD=True)

            except Exception as e:
                #db.emit_log(e)
                do_nothing()

            if scp_success:
                emit_log(f'On deck PROD {key} sent success.', file[0])
                os.remove(prod_deck_paths[key]+file[0])


# Main Entry #
# process package that is either new, approved or rolled back
while True:
    try:

        # checks if theres a file on deck for a node
        # sends if node is online
        check_prod_deck()
        check_deck()

        # checks for new files in incoming
        for filename in os.listdir(dir_to_scan):
            if approved_ext in filename:
                approve_package(filename)
            elif rollback_ext in filename:
                rollback_package(filename)
            else:
                if filename.endswith(new_pkg_type):
                    new_package(filename)

    except Exception as e:
        print(e)
        print(traceback.format_exc())

    time.sleep(5)
