#!/usr/bin/python3
'''
Listener for signals
for install, rollback, approve
'''
import subprocess
import yaml
import os
import time

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


def install_package(filename):
    subprocess.run('pack install')


def rollback_package(filename):
    subprocess.run('pack rollback')


def approve_package(filename):
    subprocess.run('pack approve')


while True:
    for filename in os.listdir(dir_to_scan):
        if approved_ext in filename:
            approve_package(filename)
        elif rollback_ext in filename:
            rollback_package(filename)
        elif install_ext in filename:
            install_package(filename)

    time.sleep(delay)
