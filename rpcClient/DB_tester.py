from DB import DB
rpc = DB()
print(" [x] Requesting current prices")

response = rpc.trade(5,4,1000)
#.register("old@gmail.com","old","man","password")
#.trade(32,31,1000)
print(" [.] Got %r" % response)
31