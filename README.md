# Project-Group5
## 1.数据部分
数据获取直接通过jqdata获取
## 2.策略部分
在北向资金布林带选股基础上叠加rsrs择时，在北向资金净流入突破上布林带的时候，挑选出北向资金占其A股比例最大的20只股票，在这20只股票的基础上分别计算每只股票的RSRS值，
高于设定rsrs阈值的股票进行买入，反之卖出
## 3.评价部分
计算策略运行期间的总收益，总收益率，sharpe，回撤，最大回撤等
## 4.UI部分
UI主要是将用户对于资产配置及表现进行可视化展示，通过将我们的业绩表现/具体订单成交结果数据导入本地数据库，再通过pandas、pymysql连接数据库，最后用PYQT5设计简单的UI组件如COMBOBOX、DATEEDITE等，提供用户筛选时间和资产种类、交易所等等功能，从而迅速展示用户指定数据
