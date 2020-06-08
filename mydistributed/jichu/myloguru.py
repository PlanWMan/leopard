from loguru import logger

def aa():
    logger.debug(f"你好王博文")
    logger.info(f"info wangbowen")
    logger.warning(f"warning wanbowen")

# aa()
# import sys
# print(sys.stdout)
# import random
# print(''.join(str(random.choice(range(10))) for _ in range(10)))

# 正则匹配id
import re
ss = f'url = "https://my.b2b.hc360.com/my/getCompany?userId=67366148&ctoken='
rt = re.findall(r'userId\D*(\d*?)\D+', ss)
print(rt)
