import pandas as pd

import re

zz = re.compile(r'\d+\.?\d*')
st = '原价7.00万'
print(zz.search(st).group())