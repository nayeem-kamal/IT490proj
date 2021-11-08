from API import API
rpc = API()
print(" [x] Requesting current prices")
response = rpc.getWeekBTC()
print(" [.] Got %r" % response)