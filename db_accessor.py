#!/usr/bin/python3
'''
Database Accessor Methods

'''
from paramiko import SSHClient
from scp import SCPClient
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
deck_path = '/home/deploy/packages/on_deck/'
prod_deck_path = '/home/deploy/packages/prod_deck/'
archive_path = '/home/deploy/packages/archive/'
log_path = '/home/deploy/packages/pack.log'
hosts_config = '/home/deploy/packages/hosts.yaml'

conn = mysql.connector.connect(
    host='localhost',
    user='deploy',
    password='12345',
    database='deployment'
    )


def emit_log(message, send_log=False):
    '''emits logs to log_path'''

    time = datetime.datetime.now().ctime()
    with open(log_path, 'a') as file:
        file.write(f'\t{message} - {time}\n')


def node_ready(node):
    ''' check outstanding status of a node who has an incoming new package'''

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

    # unpack tar.gx to tmp
    command = f"tar -xf {source_path} -C {tmp_path}"
    os.system(command)
    pkg_yaml_path = tmp_path + 'pkg.yaml'
    with open(pkg_yaml_path, 'r') as file:
        pkg_yaml = yaml.safe_load(file)

    emit_log('Unpack tar.gz and yaml grab successful')

    return pkg_yaml


def unpack_yaml(source_path):
    '''takes in src path of tar.gz, writes pkg yaml to tmp, returns yaml'''

    # reading pkg.yaml inside package.tar.gz, stores to tmp dir (was easier this way)
    command = f"tar -xf {source_path} -C {tmp_path} pkg.yaml"
    os.system(command)
    pkg_yaml_path = tmp_path + 'pkg.yaml'
    with open(pkg_yaml_path, 'r') as file:
        pkg_yaml = yaml.safe_load(file)

    # clean file from tmp
    os.remove(pkg_yaml_path)
    emit_log('yaml grab for duplicate checking successful')
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

    # will do for now, return true if package exists
    if query_result:
        return True
    else:
        return False


def prod_ready(node):
    '''check outprod status of a node who has an incoming approved pkg'''

    query = "select * from package where pkgstatus='outprod' and pkgsource=%s;"
    val = (node,)
    cursor = conn.cursor()
    cursor.execute(query, val)
    query_result = cursor.fetchall()

    if not query_result:
        return True
    else:
        return False


def set_package_approval(filename):
    '''
    change status of package in database,
    replace file with corresponding one in package storage
    as to have an updated yaml with rollback information
    '''
    pkg_yaml = unpack_yaml(dir_to_scan + filename)

    # change status
    query = "update package set pkgstatus='approved' where pkgid=%s"
    val = (pkg_yaml['pkgid'],)
    cursor = conn.cursor()
    cursor.execute(query, val)
    conn.commit()

    # replace corresponding pkg in storage with this new version
    # also change name back to pkg.tar.gz from pkg.appd.tar.gz

    pkgname = pkg_yaml['pkgname']+'.tar.gz'

    # instead of straight delete, mv original pkg
    # to tmp for saftey until replace is confirmed
    shutil.move(dir_to_store+pkg_yaml['sourcenode']+'/'+pkgname, tmp_path)

    # mv updated package to storage
    shutil.move(dir_to_scan+filename, dir_to_store+pkg_yaml['sourcenode']+'/'+pkgname)

    # rm old package stored in tmp
    os.remove(tmp_path+pkgname)

    # if prod node has no pkgs waiting for install on that system, 
    # send next package
    if prod_ready(pkg_yaml['sourcenode']):
        return {'node': pkg_yaml['sourcenode'], 'ready': True}
    else:
        return {'node': pkg_yaml['sourcenode'], 'ready': False}


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


def get_hosts():
    '''gets all 9 hosts (user and ip) from hosts config file '''

    with open(hosts_config, 'r') as file:
        hosts_yaml = yaml.safe_load(file)

    return hosts_yaml


def set_package_outstanding(node, pkgname):
    '''set given package to outstanding'''

    # 'outstanding' is the notation used for pkgs being sent
    # to QA and are waiting on approval from QA

    emit_log(f'Setting {node} {pkgname} to outstanding')
    query = "update package set pkgstatus='outstanding' where pkgsource=%s and pkgpath=%s;"
    val = (node, pkgname)
    cursor = conn.cursor()
    cursor.execute(query, val)
    conn.commit()


def set_package_outprod(node, pkgname):
    '''set given package to outprod'''

    # 'outprod' is the notation used for approved pkgs being sent
    # to production which are waiting to be installed on that machine.
    # once installed, this notation is changed to 'production'

    emit_log(f'Setting {node} {pkgname} to outprod')
    query = "update package set pkgstatus='outprod' where pkgsource=%s and pkgpath=%s;"
    val = (node, pkgname)
    cursor = conn.cursor()
    cursor.execute(query, val)
    conn.commit()



def use_scp(full_pkg_path, node, QA=False, PROD=False):
    '''makes ssh connection, sends package scp'''

    hosts_yaml = get_hosts()
    ip = ''
    user = ''
    password = ''
    remote_path = ''

    if QA:
        ip = hosts_yaml['quality_assurance'][node][0]
        user = hosts_yaml['quality_assurance'][node][1]
        password = hosts_yaml['quality_assurance'][node][2]
        remote_path = f'/home/{user}/.config/packtool/new_packages/'
    elif PROD:
        ip = hosts_yaml['production'][node][0]
        user = hosts_yaml['production'][node][1]
        password = hosts_yaml['production'][node][2]
        remote_path = f'/home/{user}/.config/packtool/new_packages/'

    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.connect(hostname=ip, username=user, password=password, port=22)
    scp = SCPClient(ssh.get_transport())

    scp.put(full_pkg_path, remote_path)

    scp.close()
    ssh.close()

    return True


def set_on_deck(full_pkg_path, pkgname, node, QA=False, PROD=False):
    '''
    In event that a node receives a new package, is ready for a new package,
    however sending the package fails due to node being offline, the package will
    be held on_deck and deploy once node is online
    Takes in str:full_pkg_path, str:recipient_node, and whether its for QA or PROD
    '''

    if QA:
        full_deck_path = deck_path + node + '/' + pkgname
        shutil.copy(full_pkg_path, full_deck_path)
        emit_log(f'On QA deck successful for {node}')
    elif PROD:
        full_deck_path = prod_deck_path + node + '/' + pkgname
        shutil.copy(full_pkg_path, full_deck_path)
        emit_log(f'On PROD deck successful for {node}')


def send_next_qa_package(node):
    '''grabs next new package for given QA node, then sends '''

    query = "select pkgpath from package where pkgsource=%s and pkgstatus='new' order by pkgid asc limit 1;"
    val = (node,)
    cursor = conn.cursor()
    cursor.execute(query, val)
    query_result = cursor.fetchall()

    if not query_result:
        emit_log('No new packages detected for QA {node}')
        return

    pkgname = query_result[0][0]

    full_pkg_path = dir_to_store + node + '/' + pkgname

    # send package to QA node
    scp_success = False
    try:
        scp_success = use_scp(full_pkg_path, node, QA=True)
    except Exception as e:
        emit_log(e)
    #subprocess.run(['scp', full_pkg_path, destination])

    if scp_success:
        emit_log(f'Successfully sent QA {node} package.')
        # set sent package to 'outstanding'
    else:
        emit_log(f'QA {node} not available, placing package on deck.')
        set_on_deck(full_pkg_path, pkgname, node, QA=True)

    # package considered outstanding whether on deck or sent
    set_package_outstanding(node, pkgname)

    return True

def send_next_prod_package(node):
    '''grabs next new package for given PROD node, then sends'''

    query = "select pkgpath from package where pkgsource=%s and pkgstatus='approved' order by pkgid asc limit 1;"
    val = (node,)
    cursor = conn.cursor()
    cursor.execute(query, val)
    query_result = cursor.fetchall()

    if not query_result:
        return False

    pkgname = query_result[0][0]

    full_pkg_path = dir_to_store + node + '/' + pkgname

    # send package to QA node
    scp_success = False
    try:
        scp_success = use_scp(full_pkg_path, node, PROD=True)
    except Exception as e:
        emit_log(e)
    #subprocess.run(['scp', full_pkg_path, destination])

    if scp_success:
        emit_log(f'Successfully sent PROD {node} package.')
        # set sent package to 'outstanding'
    else:
        emit_log(f'PROD {node} not available, placing package on prod deck.')
        set_on_deck(full_pkg_path, pkgname, node, PROD=True)

    # package considered outprod whether on deck or sent
    set_package_outprod(node, pkgname)

    return True


def rollback_package(pkg_yaml):
    '''
    updates pkgstatus to failed in database in event of rollback
    marks any remaining new packages for that node as depreciated (due to potential depends issues)
    '''

    query = "update package set pkgstatus='failed' where pkgid=%s"
    val = (pkg_yaml['pkgid'],)
    cursor = conn.cursor()
    cursor.execute(query, val)
    conn.commit()

    emit_log(f'{pkg_yaml["pkgname"]} for {pkg_yaml["sourcenode"]} marked failed.')

    # leaving this here for now, if packages are marked as failed and depreciated in db
    # shouldn't need to move them on filesystem unless to save space

    #pkgname = pkg_yaml['pkgname'] + '.tar.gz'

    # move rolledback pkg from long term storage to archive dir
    # just in case its needed for something
    #shutil.move(dir_to_store+pkgname, archive_path)
    
    # if any new packages are waiting for node, mark as depreciated
    query = "update package set pkgstatus='depreciated' where pkgsource=%s and pkgstatus='new';"
    val = (pkg_yaml['sourcenode'],)
    cursor = conn.cursor()
    cursor.execute(query, val)
    conn.commit()

    emit_log(f'Any remaining new pkgs for {pkg_yaml["sourcenode"]} depreciated.')
