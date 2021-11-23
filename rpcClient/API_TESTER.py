from API import API
rpc = API()
print(" [x] Requesting current prices")
response = rpc.getCurrentPrices()
print(" [.] Got %r" % response)
