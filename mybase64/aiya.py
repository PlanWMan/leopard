import datetime

from datetime import datetime
from time import sleep
now = datetime.now()
one = datetime.strftime(now, '%Y-%m-%d %H:%M:%S')
d = datetime.strptime(one, "%Y-%m-%d %H:%M:%S")
# t = d.timetuple()
sleep(2)
now = datetime.now()
one = datetime.strftime(now, '%Y-%m-%d %H:%M:%S')
s = datetime.strptime(one, "%Y-%m-%d %H:%M:%S")
# s = d.timetuple()
print(s)
print(d)
print(type(s))
print((s-d).days)

