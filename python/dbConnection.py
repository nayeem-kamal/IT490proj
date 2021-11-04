import mysql.connector

cnx = mysql.connector.connect(user = 'jal97', password = 'toor', host = '127.0.0.1', database = 'kommando')

cnx.close()