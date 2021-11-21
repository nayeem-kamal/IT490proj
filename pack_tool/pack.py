'''
Pack tool for making and sending
packages to deployment server

first pass
'''
import fire
import socket
import os
import yaml

def make(pkgname, pkgversion, *args):
    '''takes in strs, makes & sends package'''

    # directory traversal to establish full paths for files
    full_directory_list = []
    installpaths = []
    root = '/home/dmz/Desktop/backup_repo'
    for dir_name, sub_dir_list, file_list in os.walk(root):
        if '.git' not in dir_name:
            if 'pycache' not in dir_name:
                for fname in file_list:
                    # full_directory_list.append(f'{dir_name} + '/' + {fname}')
                    if fname in args:
                        installpaths.append(f'{dir_name}/{fname}')

    yaml_dict = {'pkgname': pkgname, 'pkgversion': pkgversion,
            'sourcenode': socket.gethostname(), 'pkgstatus': 'new',
            'install': installpaths}

    # testing
    with open('./tmp/pkg.yaml', 'w') as file:
        yaml.dump(yaml_dict, file, sort_keys=False)




def install(pkgname):
    pass


def setroot(pathname):
    pass


def help():
    pass


if __name__ == '__main__':
    fire.Fire()
