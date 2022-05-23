# standarlize
from sklearn.preprocessing import scale
import numpy as np
# import statsmodels.api as sm
import pandas as pd
from jqdatasdk import *

auth('13692899351', 'M0a6n1d7y')

# neutrulzlie

def neutrulize(raw_data, features, add_constant = True)   ->  np.array :
    '''
    进行针对features的中性化,即使用一段时间内的feature值对原始因子做ols， 用残差代替原始因子值
    '''
    if add_constant:
        x = sm.add_constant(features)
    y = raw_data
    model = sm.OLS(y, x)
    m = model.fit()
    neutruled_features = m.resid
    return neutruled_features

    # performance

class EvaluationHandler:
    
    '''
    input -> dataframe: startegy产生的portfolio序列, index 是time，columns是symbol;
    output:获取策略表现，包括
    pnl:
    maxdwardown:
    profit
    profit_all
    volitality
    sharpe:
    '''

    # global data  # 原始数据
    # global W0   # 初始资金

    def __init__(self, portfolio:pd.DataFrame,data:pd.DataFrame,total_val:float):
        self.portfolio = portfolio
        self.s_t = portfolio.index[0]   # 起始时间
        self.e_t = portfolio.index[-1]  # 终止时间
        assert portfolio.shape() == data.shape()
        self.position = (self.portfolio*data).sum(1)  # 总资金
        self.W0 = total_val
        self.data =  data

    # @property
    def position(self):   # 注意portfolio输出的格式和原始数据是一样的,time_index * symbol_columns,默认用adj close price

        self.position = self.portfolio.sum(1)

        return self.position

    @property
    def pnl(self):   # 注意portfolio输出的格式和原始数据是一样的,time_index * symbol_columns,默认用adj close price
        # self._position()
        # self.pnl = self.position.diff(1)
        return self.position.diff(1)

    @property
    def profit(self):
        # self._position()
        # self.profit = self.position.pct_change()
        # return self.profit
        return self.position.pct_change()

    @property
    def profit_all(self):
        '''
        总收益
        '''
        # self.profit_all = (self.position[-1] - W0) / W0
        # return self.profit_all
        return (self.position[-1] - self.W0) / self.W0

    @property
    def volitality(self):
        '''
        收益波动率
        '''
        # self.volitality = np.std(self.profit)
        # return self.volitality
        return np.std(self.profit)

    @property
    def maxdrawdown(self):
        '''
        输出最大回撤和出现时间
        '''
        position_all = self.position
        draw_down = (position_all.expanding().max() - position_all) / position_all.expanding().max()
        max_draw_down = [draw_down.index[np.argmax(draw_down)], draw_down.max(), draw_down]
        return max_draw_down

    @property
    def sharpe(self):
        '''
        输出策略期间的夏普
        '''
        # self._profit_all()
        # self._volitality()
        return self.profit_all / self.volitality
    

