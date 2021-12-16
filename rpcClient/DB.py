import rpcClient
import json
import hashlib



class DB:
    def __init__(self) -> None:
        self.rpc = rpcClient.RpcClient("mysql")

    def register(self,email,firstName,lastName,password):
        key = hashlib.md5(password.encode()).hexdigest()
        return self.rpc.call(json.dumps({"function":"register","firstName":str(firstName),"lastName":str(lastName)
                                                    ,"email":str(email) , "password":str(key)}))
    def login(self,email,password):
        key = hashlib.md5(password.encode()).hexdigest()
        return self.rpc.call(json.dumps({"function":"login","email":str(email) , "password":str(key)}))
    def getAccounts(self,email):
        return self.rpc.call(json.dumps({"function":"get_accounts","email":str(email)}))
    def trade(self,source,dest,amt):
        return self.rpc.call(json.dumps({"function":"trade","src":str(source),"dst":str(dest),"amt":str(amt)}))
    def tradeHistory(self,email):
        return self.rpc.call(json.dumps({"function":"get_accounts","email":str(email)}))
    def get_all_transactions(self,email):
        return self.rpc.call(json.dumps({"function":"get_all_transactions","email":str(email)}))
    def update_account(self,email,account_type,balance):
        return self.rpc.call(json.dumps({"function":"update_account","email":str(email),"account_type":str(account_type),"balance":str(balance)}))
       
