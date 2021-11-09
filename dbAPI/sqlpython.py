import mysql.connector
import json
import log
from mysql.connector.errors import Error


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
        # log.log("mysql"query+"   "+str(params))
        cursor.execute(query, params)
        conn.commit()
        print(conn)
        if conn.is_connected():
            self.close_cursor(cursor)
            self.close_connection(conn)

    def execute_sql_with_open_connection(self, cursor, query, params):
        cursor.execute(query, params)

    # insert into user table
    def insert_user(self, conn, uname, password, first, last):
        mySql_insert_query = """INSERT INTO users
(email,
password,
firstName,
lastName)
VALUES(
%s,%s,%s,%s); """
        self.execute_sql(conn, mySql_insert_query,
                         (uname, password, first, last))

    # create user
    def create_user(self, uname, password, first, last):
        try:
            self.insert_user(self.get_connection(),
                             uname, password, first, last)
            return True

        except mysql.connector.Error as error:
            log.log("mysql""Failed to insert into MYSQL table {}".format(error))
            return False

    # insert transaction
    def insert_transaction(self, conn, name):
        mySql_insert_query = """INSERT INTO transactions (name) 
                                    VALUES (%s) """
        self.execute_sql(conn, mySql_insert_query, (name,))

    # create transaction
    def create_transaction(self, name):
        try:
            self.insert_transaction(self.get_connection(), name)
            return True

        except mysql.connector.Error as error:
            log.log("mysql""Failed to insert into MySQL table {}".format(error))
            return False

    # insert data into account
    def insert_account(self, conn, un, balance, account_type):
        mySql_insert_query = """INSERT INTO Accounts (username,balance,account_type)
                                    VALUES (%s,%s,%s) """
        self.execute_sql(conn, mySql_insert_query,
                         (un, balance, account_type))

    # create accounts
    def create_account(self, uname, balance, account_type):
        try:
            conn = self.get_connection()
            self.insert_account(conn,
                                uname, balance, account_type)
            return True
        except mysql.connector.Error as error:
            log.log("mysql""Failed to insert into MySQL table {}".format(error))
            return False

    # register function
    def register(self, firstName, lastName,email, password):
        try:
            self.create_user(email, password, firstName, lastName)
            self.create_account(email, 10000, "USD")
            self.create_account(email, 0, "BTC")
            self.create_account(email, 0, "ETH")
            return True
        except Error as error:
            log.log("mysql""{}".format(error))
            return False

    # login function

    def login(self, un, pw):
        conn = self.get_connection()
        cursor = self.get_cursor(conn)
        query = """SELECT email,password FROM users where email = %s and password = %s"""
        params = (un, pw)
        self.execute_sql_with_open_connection(cursor, query, params)
        column = cursor.fetchone()
        print(column)
        self.close_cursor(cursor)
        self.close_connection(conn)
        if un == column[0] and str(pw) == str(column[1]):
            return json.dumps({"User": column})
        else:
            return json.dumps({"User": "False"})

    # see if user is already in db
    def get_User(self, un, pwd):
        try:
            conn = self.get_connection()
            cursor = self.get_cursor(conn)
            query = """"select email,password,firstname,lastname from user where email = %s and password = %s """
            params = (un, pwd)
            self.execute_sql_with_open_connection(cursor, query, params)
            columns = cursor.fetchone()
            self.close_cursor(cursor)
            self.close_connection(conn)
            if un == columns[0]:
                return columns
        except mysql.connector.Error as error:
            print("Failed to get from MySQL table {}".format(error))
            return False

    # get account
    def get_accounts(self, un):
        try:
            conn = self.get_connection()
            cursor = self.get_cursor(conn)
            query = """select * from Accounts where username = %s"""
            params = (un,)
            self.execute_sql_with_open_connection(cursor, query, params)
            columns = cursor.fetchall()
            self.close_cursor(cursor)
            self.close_connection(conn)
        
            return json.dumps({"accounts": columns})
        except mysql.connector.Error as error:
            print("Failed to get from MySQL table {}".format(error))
            return json.dumps({"accounts": "False"})

    # get trade history
    def tradeHistory(self):
        try:
            conn = self.get_connection()
            cursor = self.get_cursor(conn)
            query = """select * FROM transactions where source in (select id from"""

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

    # get all transactions
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

    # update balance where username = this and account type is this
    # update account
    def update_account(self, un, account_type, balance):
        try:
            conn = self.get_connection()
            cursor = self.get_cursor(conn)
            query = """"UPDATE balance where username = name AND account_type = cash"""
            params = (un, account_type, balance)
            self.execute_sql_with_open_connection(cursor, query, params)
            clumns = cursor.fetchall()
            self.close_cursor(cursor)
            self.close_connection(conn)
            return json.loads({"accounts": balance})
        except mysql.connector.Error as error:
            self.close_cursor(cursor)
            self.close_connection(conn)
            print("Failed to select from MySQL table {}".format(error))
            return json.loads({"accounts:""False"})

# db=DBTransactor()
# db.get_User("jal97", "toor")
