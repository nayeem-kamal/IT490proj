#!/usr/bin/python3
import db_accessor as db
import time
import datetime


def send_next_qa(node):
    '''
    grabs path info of next package for node, then sends
    '''

    db.send_next_qa_package(node)


def send_next_prod(node):
    '''sends passed package to prod node'''

    db.send_next_prod_package(node)
    #db.emit_log('Sending PROD {node} next package')
