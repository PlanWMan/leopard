import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pymongo
from guaziSpider import settings

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
import re

zz = re.compile(r'\d+\.?\d*')
'''
1.分析不同车龄的二手车数量
2.二手车行车里程分析
3.二手车原价与售价分析
'''
mongodb_cline = pymongo.MongoClient(settings.MONGO_HOST, connect=False)
guazi_mongo = mongodb_cline[settings.MONGO_DB]['carInfo']
mongo_list = guazi_mongo.find()
data_list = list(mongo_list)
data = pd.DataFrame(data_list)
data.dropna(how='all', inplace=True)

# 解析不同车龄二手车的数量
data['nianfen'] = pd.to_datetime(data['carTime']).dt.year  # 获取全部年份
data['year'] = 2020 - data['nianfen']
bins = [0, 3, 6, 9, 12, 15, 18]  # 年份区间
pd.cut(data.year, bins).value_counts().plot.bar(title='二手车车龄')  # 横坐标是年份纵坐标是数量
plt.legend()
plt.show()

# 行驶距离直方图
data['licheng'] = data['carKilometres'].map(lambda x: float(zz.search(x).group()))
bins = [0, 3, 6, 9, 12, 20, 30]  # 距离区间
pd.cut(data.licheng, bins).value_counts().plot.bar(title='行驶距离')  # 横坐标是距离纵坐标是数量
plt.legend()
plt.show()

data.dropna()
data['yuanjia'] = data['carMoneyOrigin'].map(lambda x: float(zz.search(x).group()))  # 获取原价
data['shoujia'] = data['carMoney'].map(lambda x: float(zz.search(x).group()))  # 获取售价
bins = [x * 5 for x in range(1000) if x * 5 < data['yuanjia'].max() + 5]  # 价格区间
pd.cut(data.yuanjia, bins).value_counts().plot.bar(title='原价分布图')  # 横坐标是价格纵坐标是数量
plt.legend()
plt.show()

bins = [x * 5 for x in range(1000) if x * 5 < data['shoujia'].max() + 5]  # 价格区间
pd.cut(data.shoujia, bins).value_counts().plot.bar(title='售价分布图')
plt.legend()
plt.show()

data['czl'] = data.shoujia/data.yuanjia  # 获取残值率
data.sort_values(by='year', ascending=True, inplace=True)  # 按年份排序从小到大
# 计算没一年的平均值
max_year = data['year'].max()  # 获取最大年份
czl_l, year_l = [], []
for y in range(1, max_year+1):
    czl_l.append(data['czl'][data.year == y].mean())  # 同一年份中残存率的平均值
    year_l.append(y)
plt.plot(year_l, czl_l, 'o-', color = 'g', label="残值率和车龄的关系")  # 横坐标是年份纵坐标是残存率
plt.legend()
plt.show()

# 获取公里和残值率的关系
#获取整数公里
data['licheng_z'] = round(data['licheng'])  # 里程转型
max_licheng = int(data['licheng_z'].max())
min_licheng = int(data['licheng_z'].min())
czl_l, lichegn_l = [], []
for y in range(min_licheng, max_licheng+1):
    czl_l.append(data['czl'][data.licheng_z == y].mean())  # 获取同一里程的平均残存率
    lichegn_l.append(y)
plt.plot(lichegn_l, czl_l, 'o-', color = 'g',label="残值率和里程的关系")  # 横坐标是里程纵坐标是残存率
plt.legend()
plt.show()

#行驶里程和车龄的关系
max_year = data['year'].max()
licheng_l, year_l = [], []
for y in range(1, max_year+1):
    licheng_l.append(data['licheng'][data.year == y].mean())  # 获取同一年平均里程
    year_l.append(y)
plt.plot(year_l,licheng_l, 'o-', color = 'g',label="里程和车龄的关系")  # 横坐标是年份纵坐标是里程
plt.legend()
plt.show()
