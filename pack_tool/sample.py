import os

root = '/home/dmz/Desktop/backup_repo'
for dir_name, sub_dir_list, file_list in os.walk(root):
    if '.git' not in dir_name:
        if 'pycache' not in dir_name:
            # print("Found Directory: %s" % dir_name)
            for fname in file_list:
                print('\t%s' % dir_name + '/' + fname)
