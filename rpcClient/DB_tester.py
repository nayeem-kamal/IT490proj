from DB import DB
rpc = DB()
print(" [x] Requesting current prices")
response = rpc.login("nayeem","qwer")
print(" [.] Got %r" % response)
