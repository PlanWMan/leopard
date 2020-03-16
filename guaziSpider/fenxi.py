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
bins = [0, 3, 6, 9, 12, 15, 18]
pd.cut(data.year, bins).value_counts().plot.bar(title='二手车车龄')
plt.legend()
plt.show()

# 行驶距离直方图
data['licheng'] = data['carKilometres'].map(lambda x: float(zz.search(x).group()))
bins = [0, 3, 6, 9, 12, 20, 30]
pd.cut(data.licheng, bins).value_counts().plot.bar(title='行驶距离')
plt.legend()
plt.show()

data.dropna()
data['yuanjia'] = data['carMoneyOrigin'].map(lambda x: float(zz.search(x).group()))
data['shoujia'] = data['carMoney'].map(lambda x: float(zz.search(x).group()))
bins = [x * 5 for x in range(1000) if x * 5 < data['yuanjia'].max() + 5]
pd.cut(data.yuanjia, bins).value_counts().plot.bar(title='原价分布图')
plt.legend()
plt.show()

bins = [x * 5 for x in range(1000) if x * 5 < data['shoujia'].max() + 5]
pd.cut(data.shoujia, bins).value_counts().plot.bar(title='售价分布图')
plt.legend()
plt.show()
