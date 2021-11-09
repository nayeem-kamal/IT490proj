import rpcClient
import json
import hashlib



class DB:
    def __init__(self) -> None:
        self.rpc = rpcClient.RpcClient("mysql")

    def register(self,email,firstName,lastName,password):
        key = hashlib.pbkdf2_hmac(
            'sha256', # The hash digest algorithm for HMAC
            password.encode('utf-8'), # Convert the password to bytes
            "123", # Provide the salt
            1000,
            dklen=128 # It is recommended to use at least 100,000 iterations of SHA-256 
        )
        return self.rpc.call(json.dumps({"function":"register","firstName":str(firstName),"lastName":str(lastName)
                                                    ,"email":str(email) , "password":str(key)}))
    def login(self,email,password):
        key = hashlib.pbkdf2_hmac(
            'sha256', # The hash digest algorithm for HMAC
            password.encode('utf-8'), # Convert the password to bytes
            "123", # Provide the salt
            1000,
            dklen=128 # It is recommended to use at least 100,000 iterations of SHA-256 
        )
        return self.rpc.call(json.dumps({"function":"login","email":str(email) , "password":str(key)}))
    def tradeHistory(self,email):
        return self.rpc.call(json.dumps({"function":"get_accounts","email":str(email)}))
    def get_all_transactions(self,email):
        return self.rpc.call(json.dumps({"function":"get_all_transactions","email":str(email)}))
    def update_account(self,email,account_type,balance):
        return self.rpc.call(json.dumps({"function":"update_account","email":str(email),"account_type":str(account_type),"balance":str(balance)}))
       
