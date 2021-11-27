#!/usr/bin/python3
'''
Database Accessor Methods

'''
import mysql.connector
import os
import yaml
import shutil
import datetime

dir_to_scan = '/home/deploy/packages/incoming/'
dir_to_store = '/home/deploy/packages/package_storage/'
tmp_path = '/home/deploy/packages/tmp/'
log_path = '/home/deploy/packages/pack.log'
log_path2 = '/home/deploy/packages/send.log'

conn = mysql.connector.connect(
    host='localhost',
    user='deploy',
    password='12345',
    database='deployment'
    )


def emit_log(message, send_log=False):
    '''emits logs to log_path'''

    #time = datetime.datetime.now().strftime('%m-%d %H:%M:%S')
    time = datetime.datetime.now().ctime()

    if send_log:
        with open(log_path2, 'a') as file:
            file.write(f'{message} - {time}\n')
    else:
        with open(log_path, 'a') as file:
            file.write(f'\t{message} - {time}\n')


def unpack_yaml(source_path):
    '''takes in src path of tar.gz, writes pkg yaml to tmp, returns [yaml, path]'''

    # reading pkg.yaml inside package.tar.gz, stores to tmp dir (was easier this way)
    command = f"tar -xf {source_path} -C {tmp_path} pkg.yaml"
    os.system(command)
    pkg_yaml_path = yaml.safe_load(tmp_path + 'pkg.yaml')
    with open(pkg_yaml_path, 'r') as file:
        pkg_yaml = yaml.safe_load(file)

    # clean file from tmp
    os.remove(pkg_yaml_path)
    emit_log('yaml grab successful')
    return pkg_yaml


def store_fresh_package(filename):
    '''stores new package in db'''

    # grab yaml information
    pkg_yaml = unpack_yaml(dir_to_scan + filename)

    # storing package information to database using some supplied yaml information
    query = "insert into package (pkgname, pkgversion, pkgpath, pkgsource, pkgstatus) values (%s, %s, %s, %s, %s)"
    val = (pkg_yaml['pkgname'], pkg_yaml['pkgversion'], filename, pkg_yaml['sourcenode'], pkg_yaml['pkgstatus'])
    cursor = conn.cursor()
    cursor.execute(query, val)
    conn.commit()

    # mv file from incoming dir to package storage
    shutil.move(dir_to_scan+filename, dir_to_store)

    emit_log("store pkg successful")


def does_pkg_exist(filename):
    query = "select * from package where pkgpath=%s"
    val = (filename,)
    cursor = conn.cursor()
    cursor.execute(query, val)
    query_result = cursor.fetchall()

    # will do for now, return true if package exists
    if query_result:
        return True
    else:
        return False


def check_status():
    '''
    checks for new package to send to given node only if that node
    has no current outstanding packages waiting for a pass
    '''

    nodes = {'frontend': True, 'backend': True, 'dmz': True}

    query = "select pkgsource from package where pkgstatus='outstanding';"
    cursor = conn.cursor()
    cursor.execute(query)
    query_result = cursor.fetchall()

    # disqualifies any node that has an outstanding package that has
    # yet to be marked as pass
    if query_result:
        for tup in query_result:
            for key in nodes:
                if tup[0] == key:
                    nodes[key] = False

    # checks if any qualifing nodes have a new package waiting
    # will grab the name of the oldest new package
    for key in nodes:
        if nodes[key]:
            query = f"select pkgid, pkgpath from package where pkgstatus='new' and pkgsource='{key}' order by pkgid asc limit 1;"
            cursor.execute(query)
            query_result = cursor.fetchall()

            # if new package found, store pkg filename, else set key to false
            if query_result:
                nodes[key] = [query_result[0][0]]
                nodes[key].append(query_result[0][1])
                emit_log(f'New package for {key}', send_log=True)
            else:
                nodes[key] = False

    return nodes


def send_package(node, pkgid_and_pkgpath):
    '''sends new package to destination node'''

    pkgid = pkgid_and_pkgpath[0]
    pkgpath = pkgid_and_pkgpath[1]

    emit_log(f'\tSending {node}: {pkgpath}, id:{pkgid}', send_log=True)
