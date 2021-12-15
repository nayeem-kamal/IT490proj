#!/usr/bin/python3
'''
Listener for signals
for install, rollback, approve
'''
import subprocess
import yaml
import os
import time
import datetime
import glob

delay = 5

rollback_ext = '.rb.'
approved_ext = '.appd.'
install_ext = '.install.'
config_path = os.environ['HOME'] + '/.config/packtool/config.yaml'
dir_to_scan = os.environ['HOME'] + '/.config/packtool/sig_path/'


def get_config():
    '''grabs config into'''

    with open(config_path, 'r') as file:
        config_yaml = yaml.safe_load(file)

    return config_yaml


def emit_log(message):
    '''emit log to logpath'''

    config_yaml = get_config()
    time = datetime.datetime.now().ctime()

    with open(config_yaml['log_path'], 'a') as file:
        file.write('*-\n')
        file.write(message + ':' + time + '\n')


def scrub_signal():
    '''remove file in sig_path directory'''

    sig_file_list = glob.glob(dir_to_scan+"*")
    for file in sig_file_list:
        os.remove(file)


def install_package(filename):
    '''auto call the pack tool to install'''
    emit_log('Remote Install Signal Detected')
    os.system('pack install')

    # rm loose signal file
    scrub_signal()


def rollback_package(filename):
    '''auto call the pack tool to rollback'''
    emit_log('Remote Rollback Signal Detected')
    os.system('pack rollback')

    # rm loose signal file
    scrub_signal()


def approve_package(filename):
    '''auto call the pack tool to approve'''
    emit_log('Remote Approve Signal Detected')
    os.system('pack approve')

    # rm loose signal file
    scrub_signal()


while True:
    for filename in os.listdir(dir_to_scan):
        if approved_ext in filename:
            approve_package(filename)
        elif rollback_ext in filename:
            rollback_package(filename)
        elif install_ext in filename:
            install_package(filename)

    time.sleep(delay)
