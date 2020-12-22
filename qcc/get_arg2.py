list1 = [15, 35, 29, 24, 33, 16, 1, 38, 10, 9, 19, 31, 40, 27, 22, 23, 25, 13, 6, 11, 39, 18, 20, 8, 14, 21, 32, 26, 2,
         30, 7, 4, 17, 5, 3, 28, 34, 37, 12, 36]
arg1 = 'D70B5D128ABCB064CECF604400B93356F8F379B0'
this_ = list1
for i in range(len(arg1)):
    a = arg1[i]
    for _ in range(len(list1)):
        if list1[_] == (i + 1):
            this_[_] = a
this_2 = "".join(this_)
print(this_2)
string_2 = "3000176000856006061501533003690027800375"
num = 0
arg2 = ""
while num < len(this_2):
    v1 = int(this_2[num: num + 2], 16)
    v2 = int(string_2[num: num + 2], 16)
    v3 = hex(v1 ^ v2)[2:]
    if len(v3) == 1:
        v3 = '0'+str(v3)
    arg2 += v3
    num += 2
print(arg2)
