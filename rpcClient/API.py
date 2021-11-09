import rpcClient
import json


class API:
    def __init__(self) -> None:
        self.rpc = rpcClient.RpcClient("dmz")

    def getCurrentPrices(self):
        return json.loads(self.rpc.call({"function":"getCurrentPrices"}))
    def getWeekBTC(self):
        return json.loads(self.rpc.call({"function":"getBTCDailyHistoricalWeek"}))
    def getWeekETH(self):
        return json.loads(self.rpc.call({"function":"getETHDailyHistoricalWeek"}))
    def getYearBTC(self):
        return json.loads(self.rpc.call({"function":"getBTCDailyHistoricalTwelveMonth"}))
    def getYearETH(self):
        return json.loads(self.rpc.call({"function":"getETHDailyHistoricalTwelveMonth"}))
    def getThreeYearsBTC(self):
        return json.loads(self.rpc.call({"function":"getBTCDailyHistoricalYears"}))
    def getThreeYearsETH(self):
        return json.loads(self.rpc.call({"function":"getETHDailyHistoricalYears"}))    
