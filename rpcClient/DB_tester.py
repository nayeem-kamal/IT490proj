from DB import DB
rpc = DB()
print(" [x] Requesting current prices")
response = rpc.trade(2,1,1000)
print(" [.] Got %r" % response)
