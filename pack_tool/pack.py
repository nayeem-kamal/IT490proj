'''
Pack tool for making and sending
packages to deployment server

first pass

will probably become a class

package naming convention: samplepak-1.0
'''
import fire
import socket
import os
import yaml
import sys
import subprocess
import tarfile
import shutil

deployment_ip = '192.168.100.4'
deployment_server = f'dmz@{deployment_ip}:/home/dmz/packages'
tmp_path = 'tmp/'

def make(pkgname, *args):
    '''takes in strs, makes & sends package'''

    try:
        pkgversion = float(pkgname.split('-')[1])
    except Exception:
        sys.exit('Double check package naming convention')

    # directory traversal to establish full paths for files
    installpaths = {}
    root = '/home/dmz/Desktop/backup_repo'
    for dir_name, sub_dir_list, file_list in os.walk(root):
        if '.git' not in dir_name:
            if 'pycache' not in dir_name:
                for fname in file_list:
                    if fname in args:
                        #installpaths.append(f'{dir_name}/{fname}')
                        installpaths[fname] = f'{dir_name}/{fname}'

    #if len(installpaths) != len(args):
    #    sys.exit("Not all files found, check names")

    yaml_dict = {'pkgname': pkgname, 'pkgversion': str(pkgversion),
            'sourcenode': socket.gethostname(), 'pkgstatus': 'new',
            'install': installpaths}

    # write pkg.yaml to tmp
    with open(tmp_path + 'pkg.yaml', 'w') as file:
        yaml.dump(yaml_dict, file, sort_keys=False)

    # copy pkg files to tmp
    for fname in installpaths:
        shutil.copyfile(installpaths[fname], tmp_path+fname)

    # tar.gz files in tmp
    subprocess.run(f'tar -czf {pkgname}.tar.gz *', cwd=tmp_path, shell=True)

    # send pkg.tar.gz to deployment server
    # subprocess.run(["scp", filepath, 'dmz@192.168.100.4:/home/dmz/packages'])

    # create tar.gz
    #with tarfile.open('./tmp/' + pkgname, 'w:gz') as tar:
    #    tar.add('pkg.yaml')
    #    for path in installpaths:
    #        tar.add(path)


def install(pkgname):
    pass


def setroot(pathname):
    pass


def help():
    pass


if __name__ == '__main__':
    fire.Fire()
