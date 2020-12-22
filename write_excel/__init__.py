import re
def get_num(content):
    ma = re.match(r'^(\d+)', content)
    if ma:
        return ma.group()
    return ''

aa = '12你好'
print(get_num(aa))