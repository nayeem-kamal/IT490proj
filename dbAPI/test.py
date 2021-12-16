from sqlpython import DBTransactor

d = DBTransactor()
# print(d.register("a","a","a@b","assword"))
# print(d.login("a","a"))
# print(d.get_accounts("a@b"))
print(d.trade(1,2,10))
print(d.tradeHistory("a@b"))
# config = {"hostname" : "localhost","database" : "kommando","user" : "nhk6","password" : "nhk6"}

# connection = mysql.connector.connect(host=config['hostname'],database=config['database'],user=config['user'],password=config['password'],auth_plugin='mysql_native_password')