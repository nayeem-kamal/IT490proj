'''
Database Accessor Methods

'''
import mysql.connector

package_path = '/home/dmz/packages/package_storage/'
conn = mysql.connector.connect(
        host='localhost',
        user='deploy',
        password='12345',
        database='deployment'
        )


def store_fresh_package(filename, pkg_yaml):
    '''stores new package in db'''

    # storing package information to database using some supplied yaml information
    query = "insert into package (pkgname, pkgversion, pkgpath, pkgstatus, pkgdesc) values (%s, %s, %s, %s, %s)"
    val = (pkg_yaml['pkgname'], pkg_yaml['pkgversion'], filename, pkg_yaml['pkgstatus'], pkg_yaml['pkgdesc'])
    cursor = conn.cursor()
    cursor.execute(query, val)
    conn.commit()

    print("store fresh pkg success")

def truncate_command(cmd_filename):
    '''strips function command from incoming file name'''

    cmd_filename = cmd_filename.split(":")
    filename = cmd_filename[1]
    return filename
