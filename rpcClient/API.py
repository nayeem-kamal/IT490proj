import rpcClient
import json


class API:
    def __init__(self) -> None:
        self.rpc = rpcClient.RpcClient("dmz")

    def getCurrentPrices(self):
        return json.loads(self.rpc.call(json.dumps({"function":"getCurrentPrices"})))
    def getWeekBTC(self):
        return json.loads(self.rpc.call(json.dumps({"function":"getBTCDailyHistoricalWeek"})))
    def getWeekETH(self):
        return json.loads(self.rpc.call(json.dumps({"function":"getETHDailyHistoricalWeek"})))
    def getYearBTC(self):
        return json.loads(self.rpc.call(json.dumps({"function":"getBTCDailyHistoricalTwelveMonth"})))
    def getYearETH(self):
        return json.loads(self.rpc.call(json.dumps({"function":"getETHDailyHistoricalTwelveMonth"})))
    def getThreeYearsBTC(self):
        return json.loads(self.rpc.call(json.dumps({"function":"getBTCDailyHistoricalYears"})))
    def getThreeYearsETH(self):
        return json.loads(self.rpc.call(json.dumps({"function":"getETHDailyHistoricalYears"})))    
