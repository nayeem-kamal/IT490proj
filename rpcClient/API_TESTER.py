from API import API
import json
rpc = API()
print(" [x] Requesting current prices")

response = json.loads(rpc.getLedger().decode("utf-8"))["Data"]
print(" [.] Got %r" % response)
