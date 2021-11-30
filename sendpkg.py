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
    '''
    grabs path info of next package for node, then sends
    '''
    db.emit_log(f'Sending QA {node} next package.')

    db.send_qa_package(node)

def send_next_prod(node):
    '''sends passed package to prod node'''

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
