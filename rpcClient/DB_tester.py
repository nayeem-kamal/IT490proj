from DB import DB
rpc = DB()
print(" [x] Requesting current prices")
response = rpc.getAccounts("nayeem")
print(" [.] Got %r" % response)
