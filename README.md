# Project-Group5
## 1.数据部分
数据获取直接通过jqdata获取
## 2.策略部分
在北向资金布林带选股基础上叠加rsrs择时，在北向资金净流入突破上布林带的时候，挑选出北向资金占其A股比例最大的20只股票，在这20只股票的基础上分别计算每只股票的RSRS值，
高于设定rsrs阈值的股票进行买入，反之卖出
## 3.评价部分
计算策略运行期间的总收益，总收益率，sharpe，回撤，最大回撤等
