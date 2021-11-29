#!/usr/bin/python3
import db_accessor as db
import time
import datetime

log_path2 = '/home/deploy/packages/send.log'


def emit_log(message):
    '''emits logs to log_path'''

    time = datetime.datetime.now().ctime()
    with open(log_path2, 'a') as file:
        file.write(f'{message} - {time}\n')


def send_next_qa(node):
    pass
    '''
    hm.. grab path info for next package for node - dbacccesor
    then grab tar.gz from filesystem and scp to QA node - here

    '''
    db.emit_log(f'Sending QA {node} next package.')

def send_next_prod(node):

    db.emit_log('Sending PROD {node} next package')

#while True:
#    try:
#        nodes = db.check_status()
#        for key in nodes:
#            if nodes[key]:
#                db.send_package(key, nodes[key])
#
#    except Exception as e:
#        print(e)
#
#    time.sleep(5)
