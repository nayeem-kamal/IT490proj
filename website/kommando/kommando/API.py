import rpcClient
import json


class API:
    def __init__(self) -> None:
        self.rpc = rpcClient.RpcClient("dmz")

    def getCurrentPrices(self):
        return self.rpc.call(json.dumps({"function":"getCurrentPrices"}))
    def getWeekBTC(self):
        return self.rpc.call(json.dumps({"function":"getBTCDailyHistoricalWeek"}))
    def getWeekETH(self):
        return self.rpc.call(json.dumps({"function":"getETHDailyHistoricalWeek"}))
    def getYearBTC(self):
        return self.rpc.call(json.dumps({"function":"getBTCDailyHistoricalTwelveMonth"}))
    def getYearETH(self):
        return self.rpc.call(json.dumps({"function":"getETHDailyHistoricalTwelveMonth"}))
    def getThreeYearsBTC(self):
        return self.rpc.call(json.dumps({"function":"getBTCDailyHistoricalYears"}))
    def getThreeYearsETH(self):
        return self.rpc.call(json.dumps({"function":"getETHDailyHistoricalYears"}))    
    def getLedger(self):
        return self.rpc.call(json.dumps({"function":"getLedger"}))    
