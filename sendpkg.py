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


while True:
    try:
        nodes = db.check_status()
        for key in nodes:
            if nodes[key]:
                db.send_package(key, nodes[key])

    except Exception as e:
        print(e)

    time.sleep(5)
