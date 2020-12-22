import pymongo
import pandas as pd

client = pymongo.MongoClient('172.16.6.196', 28018)
db = client['py_business']
db.authenticate('py_yangying', 'Cyke746TGSBunbQ8Y')
pk10 = db['qzw_four']
data = pd.DataFrame(list(pk10.find()))
print(data)
data.to_excel('./park.xlsx')
