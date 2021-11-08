import mysql.connector
import json


class DBTransactor:
    def __init__(self) -> None:
        self.config = {}
        with open("database.config", "r") as config_file:
            self.config = json.load(config_file)

        if "hostname" not in self.config:
            exit()

    def get_connection(self):
        connection = mysql.connector.connect(host=self.config['hostname'],
                                             database=self.config['database'],
                                             user=self.config['user'],
                                             password=self.config['password'],
                                             auth_plugin='mysql_native_password')
                                             
        return connection
    def get_cursor(self, conn):
        return conn.cursor()

    def close_cursor(self, curs):
        curs.close()

    def close_connection(self, conn):
        conn.close()

    # Pass in a MySqlConnection (conn) and a query to be executed (query) and needed parameters(params)
    def execute_sql(self, conn, query, params):
        cursor = self.get_cursor(conn)
        cursor.execute(query, params)
        conn.commit()
        if conn.is_connected():
            self.close_cursor(cursor)
            self.close_connection(conn)

    def execute_sql_with_open_connection(self, cursor, query, params):
        cursor.execute(query, params)
    
    #insert into user table
    def insert_user(self, conn, name):
        mySql_insert_query = """"INSERT INTO users(name)
                                    VALUES (%s) """
        self.execute_sql(conn, mySql_insert_query, (name,))

    #create user
    def create_user(self, name):
        try:
            self.insert_user(self.get_connection(), name)
            return True

        except mysql.connector.Error as error:
            print("Failed to insert into MYSQL table {}".format(error))
            return False
    
    #insert transaction
    def insert_transaction(self, conn, name):
        mySql_insert_query = """INSERT INTO transactions (name) 
                                    VALUES (%s) """
        self.execute_sql(conn, mySql_insert_query, (name,))

    #create transaction
    def create_transaction(self, name):
        try:
            self.insert_transaction(self.get_connection(), name)
            return True

        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
            return False
    #insert data into account
    def insert_account(self, conn, name):
        mySql_insert_query = """INSERT INTO Accounts (name)
                                    VALUES (%s) """
        self.execute_sql(conn, mySql_insert_query, (name,))

    # create accounts
    def create_account(self, name):
        try:
            self.insert_account(self.get_connection(), name)
            return True
        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
            return False

    #register function
    def register(self, firstName, lastName, un, email, password):
        conn = self.get_connection()
        cursor = self.get_cursor(conn)
        mySql_insert_query = """INSERT INTO users (firstName, lastName, un, email, password
                                VALUES(%s, %s, %s, %s, %s)"""
        self.execute_sql_with_open_connection(conn, mySql_insert_query, (firstName,), (lastName,), (un,), (email,) (password,) )
    
    # login function
    def login(self, un, pw):
        conn = self.get_connection()
        cursor = self.get_cursor(conn)
        query = """SELECT * FROM user where username = un and password == pw"""
        params = (un, pw)
        self.execute_sql(cursor, query, params)
        columns = cursor.fetchmany(2)
        self.close_cursor(cursor)
        self.close_connection(conn)
        if un == username and pw == password:
            return True
        else:
            return False

    # see if user is already in db
    def get_User(self, un, pwd):
        try:
            conn = self.get_connection()
            cursor = self.get_cursor(conn)
            query = """"select name and password from user where username = %s and password = %s """
            params = (un, pwd)
            self.execute_sql_with_open_connection(cursor, query, params)
            columns = cursor.fetchone()
            self.close_cursor(cursor)
            self.close_connection(conn)
            if un == columns[0]:
                print(columns)
                return True
        except mysql.connector.Error as error:
            print("Failed to get from MySQL table {}".format(error))
            return False

    #get trade history
    def tradeHistory(self):
        try:
            conn = self.get_connection()
            cursor = self.get_cursor(conn)
            query = """select totalCost FROM transactions """
            params = ()
            self.execute_sql(cursor, query, params)
            columns = cursor.fetchall()
            self.close_cursor(cursor)
            self.close_connection(conn)
            tradeHistory = []
            for column in columns:
                tradeHistory.append(tradeHistory[0])
            return tradeHistory
        except mysql.connector.Error as error:
            self.close_cursor(cursor)
            self.close_connection(conn)
            print("Failed to select from MySQL table {}".format(error))
            return False

    #get all transactions
    def get_all_transactions(self):
        try:
            conn = self.get_connection()
            cursor = self.get_cursor(conn)
            query = """select name from transactions """
            params = ()
            self.execute_sql_with_open_connection(cursor, query, params)
            columns = cursor.fetchall()
            self.close_cursor(cursor)
            self.close_connection(conn)
            transactions = []
            for transaction in columns:
                transactions.append(transaction[0])
            return transactions
        except mysql.connector.Error as error:
            self.close_cursor(cursor)
            self.close_connection(conn)
            print("Failed to select from MySQL table {}".format(error))
            return False

db=DBTransactor()
db.get_User("jal97", "toor")