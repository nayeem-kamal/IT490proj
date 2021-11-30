#!/usr/bin/python3
'''
Database Accessor Methods

'''
import mysql.connector
import os
import yaml
import shutil
import datetime
import subprocess
import glob

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


def node_ready(node):
    ''' check outstanding status of a node who just received a new package'''

    query = "select * from package where pkgstatus='outstanding' and pkgsource=%s;"
    val = (node,)
    cursor = conn.cursor()
    cursor.execute(query, val)
    query_result = cursor.fetchall()

    if not query_result:
        return True
    else:
        return False


def repack_tar_gz(pkg_yaml):
    '''
    rewrites new pkg.yaml with pkgid
    repacks tar in tmp, mvs to package storage, deletes original package
    '''
    pkgname = pkg_yaml['pkgname']
    pkg_extension = '.tar.gz'

    with open(tmp_path + 'pkg.yaml', 'w') as file:
        yaml.dump(pkg_yaml, file, sort_keys=False)

    # create new tar.gz from tmp files, change working dir to tmp then execute command
    subprocess.run(f'tar -czf {pkgname}{pkg_extension} *', cwd=tmp_path, shell=True)

    # move new tar.gz to storage
    shutil.move(tmp_path+pkgname+pkg_extension, dir_to_store+pkg_yaml['sourcenode'])


def unpack_tar_gz(source_path):
    '''unpacks tar to tmp to pull and easily add pkgid to pkg.yaml'''

    # if anything in tmp, delete it
    #command = f'gio trash {tmp_path}*'
    #os.system(command)

    # unpack tar.gx to tmp
    command = f"tar -xf {source_path} -C {tmp_path}"
    os.system(command)
    pkg_yaml_path = tmp_path + 'pkg.yaml'
    with open(pkg_yaml_path, 'r') as file:
        pkg_yaml = yaml.safe_load(file)

    emit_log('Unpack tar.gz and yaml grab successful')

    return pkg_yaml


def unpack_yaml(source_path):
    '''takes in src path of tar.gz, writes pkg yaml to tmp, returns [yaml, path]'''

    # reading pkg.yaml inside package.tar.gz, stores to tmp dir (was easier this way)
    command = f"tar -xf {source_path} -C {tmp_path} pkg.yaml"
    os.system(command)
    pkg_yaml_path = tmp_path + 'pkg.yaml'
    with open(pkg_yaml_path, 'r') as file:
        pkg_yaml = yaml.safe_load(file)

    # clean file from tmp
    os.remove(pkg_yaml_path)
    emit_log('yaml grab successful')
    return pkg_yaml


def scrub_tmp():
    tmp_file_list = glob.glob(tmp_path+"*")
    for file in tmp_file_list:
        os.remove(file)


def store_fresh_package(filename):
    '''stores new package in db'''

    approved_sourcenodes = ['frontend', 'backend', 'dmz']

    # grab yaml information
    pkg_yaml = unpack_tar_gz(dir_to_scan + filename)

    # checks on hostname of package source, returns if not recognized
    if pkg_yaml['sourcenode'] not in approved_sourcenodes:
        emit_log(f'Hostname {pkg_yaml["sourcenode"]} not approved, removing..')
        scrub_tmp()
        return {'node': pkg_yaml['sourcenode'], 'ready': False}

    # storing package information to database using some supplied yaml information
    query = "insert into package (pkgname, pkgversion, pkgpath, pkgsource, pkgstatus) values (%s, %s, %s, %s, %s)"
    val = (pkg_yaml['pkgname'], pkg_yaml['pkgversion'], filename, pkg_yaml['sourcenode'], pkg_yaml['pkgstatus'])
    cursor = conn.cursor()
    cursor.execute(query, val)
    conn.commit()

    query = 'select pkgid from package order by pkgid desc limit 1;'
    cursor.execute(query)
    pkgid = cursor.fetchall()[0][0]

    # add pkgid to pkg yaml, then repack and delete tmp files
    pkg_yaml['pkgid'] = pkgid
    repack_tar_gz(pkg_yaml)

    # mv file new tar.gz from tmp to package storage
    #shutil.move(dir_to_scan+filename, dir_to_store+pkg_yaml['sourcenode'])

    # delete original tar.gz from incoming
    os.remove(dir_to_scan+filename)

    # remove leftover files in tmp
    tmp_file_list = glob.glob(tmp_path+"*")
    for file in tmp_file_list:
        os.remove(file)

    emit_log("New package successfully stored")

    # if node has no outstanding packages waiting for a pass, node ready for next pkg
    if node_ready(pkg_yaml['sourcenode']):
        return {'node': pkg_yaml['sourcenode'], 'ready': True}
    else:
        return {'node': pkg_yaml['sourcenode'], 'ready': False}


def does_pkg_exist(filename):
    '''checks to see if source submitted duplicate pkgname'''

    pkg_yaml = unpack_yaml(dir_to_scan + filename)

    query = "select * from package where pkgpath=%s and pkgsource=%s"
    val = (filename, pkg_yaml['sourcenode'])
    cursor = conn.cursor()
    cursor.execute(query, val)
    query_result = cursor.fetchall()

    print('does_pkg_exist:')
    print(query_result)
    # will do for now, return true if package exists
    if query_result:
        return True
    else:
        return False


def set_package_passed(filename):
    '''
    change status of package in database
    '''
    pkg_yaml = unpack_yaml(dir_to_scan + filename)

    query = "update package set pkgstatus='passed' where pkgid=%s"
    val = (pkg_yaml['pkgid'],)
    cursor = conn.cursor()
    cursor.execute(query, val)
    conn.commit()


def check_status():
    '''
    checks for new package to send to given node only if that node
    has no current outstanding packages waiting for a pass

    outdated, new paradigm implemeted, this is currently for reference
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


def set_package_outstanding(node, pkgpath):
    '''set given package to outstanding '''

    emit_log(f'Setting {node} {pkgpath} to outstanding')
    query = "update package set pkgstatus='outstanding' where pkgsource=%s and pkgpath=%s;"
    val = (node,)
    cursor = conn.cursor()
    cursor.execute(query, val)
    conn.commit()


def send_next_qa_package(node):
    '''grabs next new package for given QA node, then sends '''

    host = node + '_qa'
    destination = f'{host}:/home/deploy/packages/incoming/'

    query = "select pkgpath from package where pkgsource=%s and pkgstatus='new' order by pkgid asc limit 1;"
    val = (node,)
    cursor = conn.cursor()
    cursor.execute(query, val)
    query_result = cursor.fetchall()

    pkgpath = query_result[0][0]

    full_pkg_path = dir_to_store + node + '/' + pkgpath

    # send package to QA node
    subprocess.run(['scp', full_pkg_path, destination])

    # set sent package to 'outstanding'
    set_package_outstanding(node, pkgpath)
