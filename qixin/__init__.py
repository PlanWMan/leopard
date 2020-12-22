import re
def get_phone(phone):
    # 返回手机和电话的方法t电话 s手机
    sx = r"^1[3456789]\d{9}$"  # 正则手机号
    tx = r"^(\(\d{3,4}\)|\d{3,4}-|\s)?\d{7,14}$"  # 正则电话
    s = re.findall(sx, phone)
    t = re.findall(tx, phone)
    return ','.join(t), ','.join(s)

get_phone('0997-4686989/18096905885')

