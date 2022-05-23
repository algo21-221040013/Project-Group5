#from .API import *
# 导入函数库top_money_in

# from multiprocessing import context
import random
import pandas as pd
import numpy as np
import datetime as dt
# import statsmodels.api as sm
from jqdatasdk import *

auth('13692899351', 'M0a6n1d7y')

max_stock_count = 20
back_trade_days=80
top_money_in = []
up_ratio = 0.96
window = 90
stdev_up = 2
stdev_dn = 2
mf, upper, lower = None, None, None

quantile_N = 15
quantile_M = 15
buy = -0.1
sell = -0.4
#用于记录回归后的beta值，即斜率
ans = []
#用于计算被决定系数加权修正后的贝塔值
ans_rightdev= []
security = '000300.XSHG'
# global security = ''
N = 18
M = 600

init = True

def initialize(context):
 #dzq
    prices = get_price(security, context.current_dt - dt.timedelta(days=M+1), context.previous_date, '1d', ['high', 'low'])
    highs = prices.high
    lows = prices.low
    global ans

    for i in range(len(highs))[N:]:
        data_high = highs.iloc[i-N+1:i+1]
        data_low = lows.iloc[i-N+1:i+1]
        beta,r2 = get_ols(data_low,data_high)
        ans.append(beta)
        ans_rightdev.append(r2)



def before_market_open(context):
    pre_date = (context.current_dt - dt.timedelta(days=1)).strftime('%Y-%m-%d')
    global mf,upper,lower
    mf,upper,lower = get_boll(pre_date)
    # print('北上资金均值：%.2f  北上资金上界：%.2f 北上资金下界：%.2f' % (mf,upper,lower))

def get_boll(end_date):
    """
    获取北向资金布林带
    """
    # dzq/
    print(end_date)
    table = finance.STK_ML_QUOTA
    q = query(
        table.day, table.quota_daily, table.quota_daily_balance
    ).filter(
        table.link_id.in_(['310001', '310002']), table.day<=end_date
    ).order_by(table.day)
    money_df = finance.run_query(q)
    # print(money_df)

    money_df['net_amount'] = (money_df['quota_daily'] - money_df['quota_daily_balance'])
    # print(money_df['net_amount'])
    # 分组求和
    money_df = money_df.groupby('day')[['net_amount']].sum().iloc[-window:]
    mid = money_df['net_amount'].mean()
    stdev = money_df['net_amount'].std()
    upper = mid + stdev_up * stdev
    lower = mid - stdev_dn * stdev
    mf = money_df['net_amount'].iloc[-1]
    # print('mf:%.2f    upper:%.2f    lower:%.2f')%(mf,upper,lower)
    return mf, upper, lower

# print(get_boll('2021-02-01'))
def calc_change(context,stock_universe = []):
    table = finance.STK_HK_HOLD_INFO
    q = query(table.day, table.name, table.code, table.share_ratio)\
        .filter(table.link_id.in_(['310001', '310002']),
                table.day.in_([context.previous_date]),
                table.code.in_(stock_universe)
                )
    df = finance.run_query(q)

    # df['share_ratio'] = df['share_ratio']
    return df.sort_values(by='share_ratio',ascending=False)[3:max_stock_count]['code'].values
    
def rebalance(context):
    chg_posi = {}
    # stock_universe = get_up_stock(get_index_stocks(global security))
    # stock_universe = get_index_stocks(global security)
    if mf >= upper:
        # s_change_rank=get_up_stock(calc_change(context,get_index_stocks(global security)))
        # s_change_rank = calc_change(context,stock_universe)
        
        s_change_rank = calc_change(context,get_index_stocks(security))
        final = list(s_change_rank)
        # print(final)
        current_hold_funds_set = set([k for k,v in context.position.items() if v])
        rsrs_sell = []
        rsrs_buy = []
        for stock in final:
            rsrs = calc_zscore_Rdev(context,stock)
            if rsrs < sell:
                rsrs_sell.append(stock)
                
        if set(final) != current_hold_funds_set:
            need_buy= set(final).difference(current_hold_funds_set).difference(rsrs_sell)
            need_sell= current_hold_funds_set.difference(set(final).difference(rsrs_sell))
            # print(need_buy)
            for fund in need_sell:
                chg_posi[fund] = 0
            if len(need_buy):
                cash_per_fund=context.total_amt/len(need_buy)
            for fund in need_buy:
                chg_posi[fund] = cash_per_fund
    
    elif mf <= lower:
        current_hold_funds_set = set([k for k,v in context.position.items() if v])
        if len(current_hold_funds_set)!=0:
            for fund in current_hold_funds_set:
                chg_posi[fund] = 0
    return chg_posi
        # purchase(global fund,context.portfolio.total_value)



def calc_zscore_Rdev(context,stock):
    beta=0
    r2=0
    signal = 0
    # print('init', init)
    global init
    if init:
        init = False
        signal = 1
    else:
        #RSRS斜率指标定义
        # signal = 1
        prices = get_price(stock, context.current_dt-dt.timedelta(days=N),context.current_dt, '1d', ['high', 'low','close'])
        highs = prices.high**2
        lows = prices.low**2
        ret = prices.close.pct_change().dropna()
        beta,r2 = get_ols(lows,highs)
        # X = sm.add_constant(lows)
        # model = sm.OLS(highs, X)
        # beta = model.fit().params[1]
        ans.append(beta)
        #计算r2
        # r2=model.fit().rsquared
        ans_rightdev.append(r2)
    
    # 计算标准化的RSRS指标
    # 计算均值序列    
    section = ans[-M:]
    # 计算均值序列
    mu = np.mean(section)
    # 计算标准化RSRS指标序列
    sigma = np.std(section)
    zscore = (section[-1]-mu)/sigma  
    # ret = attribute_history(stock,global N,'1d')
    #计算右偏RSRS标准分
    if signal:
        return zscore*r2
    else:
        return zscore*r2**(2*cal_ret_quantile(ret))

def cal_ret_quantile(price_df):

    # 计算收益波动
    ret_std = np.sqrt(price_df.rolling(quantile_N).std())
    ret_quantile = ret_std.rolling(quantile_M).apply(
        lambda x: x.rank(pct=True)[-1], raw=False)

    return ret_quantile.values[-1]


def get_ols(X,y):
    X = list(X)
    y = list(y)
    if X and y:
        n = len(y)
        cov = np.cov(np.vstack((X,y)))
        beta = cov[0,1]/cov[0,0]
        # r2 =1 - (1- beta**2 * cov[0,0]/cov[1,1])*(n-1)/(n-2)
        r2 = beta**2 * cov[0,0]/cov[1,1]
        return beta,r2
    return 0,0