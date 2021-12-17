#!/bin/bash
python3 /home/pdp72/Desktop/IT490proj/website/kommando/manage.py runserver_plus --cert-file cert.pem --key-file key.pem &> /home/pdp72/django.log
