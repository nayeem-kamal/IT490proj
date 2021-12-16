from DB import DB
rpc = DB()
print(" [x] Requesting current prices")
response = rpc.tradeHistory("a@b")
print(" [.] Got %r" % response)
