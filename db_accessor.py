#!/usr/bin/python3
'''
Database Accessor Methods

'''
import mysql.connector
import os
import yaml
import shutil

dir_to_scan = '/home/dmz/packages/'
dir_to_store = '/home/dmz/packages/package_storage/'
tmp_path = dir_to_scan + 'tmp/'

conn = mysql.connector.connect(
    host='localhost',
    user='deploy',
    password='12345',
    database='deployment'
    )


def unpack_yaml(source_path):
    '''takes in src path of tar.gz, writes pkg yaml to tmp, returns [yaml, path]'''

    # reading pkg.yaml inside package.tar.gz, stores to tmp dir (was easier this way)
    command = f"tar -xf {source_path} -C {tmp_path} pkg.yaml"
    os.system(command)
    pkg_yaml_path = yaml.safe_load(tmp_path + 'pkg.yaml')
    with open(pkg_yaml_path, 'r') as file:
        pkg_yaml = yaml.safe_load(file)

    os.remove(pkg_yaml_path)

    return pkg_yaml


def store_fresh_package(filename):
    '''stores new package in db'''

    # grab yaml information
    pkg_yaml = unpack_yaml(dir_to_scan + filename)

    # storing package information to database using some supplied yaml information
    query = "insert into package (pkgname, pkgversion, pkgpath, pkgstatus, pkgdesc) values (%s, %s, %s, %s, %s)"
    val = (pkg_yaml['pkgname'], pkg_yaml['pkgversion'], filename, pkg_yaml['pkgstatus'], pkg_yaml['pkgdesc'])
    cursor = conn.cursor()
    cursor.execute(query, val)
    conn.commit()

    # mv file from incoming dir to package storage
    shutil.move(dir_to_scan+filename, dir_to_store)

    print("store fresh pkg success")


def truncate_command(cmd_filename):
    '''strips function command from incoming file name'''

    cmd_filename = cmd_filename.split(":")
    filename = cmd_filename[1]
    return filename
