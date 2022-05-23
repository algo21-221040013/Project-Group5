from datetime import datetime
from datetime import timedelta
import pandas as pd
from algo_pro import *
from evaluation import *
from jqdatasdk import *

auth('13692899351', 'M0a6n1d7y')
class Context():
    def __init__(self,start,end,securities,amt):
        self.start = start
        self.end = end
        self.secty = securities
        self.position = {key:0 for key in securities}
        self.current_dt = start
        self.his_posi = pd.DataFrame([])
        self.total_amt = amt


    def next_day(self):
        self.his_posi = pd.concat([self.his_posi,pd.DataFrame(self.position.values()).T])
        self.current_dt += timedelta(1)

    def chg_position(self,posi_dict):
        for k,v in posi_dict.items():
            self.position[k] = v
        self.total_amt = np.array(self.position.values()).sum()

    @property
    def history_posi(self):
        self.his_posi.index = get_trade_days(self.start,self.end)
        return self.his_posi
    
class Backtest():
    def __init__(self,start,end,security,total_amt):
        print(1)
        self.start = start
        self.end = end
        self.security = security
        self.securities = get_index_stocks(security)
        self.context = Context(start,end,self.securities,total_amt)
        self.total_amt = total_amt
        

    def backtest(self):
        trade_days = get_trade_days(self.start,self.end)

        initialize(self.context)
        for day in trade_days:
            before_market_open(self.context)
            chg_posi = rebalance(self.context)
            self.context.chg_position(chg_posi)

        self.history_posi = self.context.his_posi
        performance = EvaluationHandler(self.history_posi)
        self.shrp = performance.sharpe
        self.mdd = performance.maxdrawdown

if '__name__' == '__main__':
    bt = Backtest('2017-05-16','2021-02-01','000300.XSHG',100000)
    result = bt.backtest()
    print(result.shrp)
    print(result.mdd)
