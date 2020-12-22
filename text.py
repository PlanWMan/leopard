import requests
data = {
    # 'id':'115775121',
    'cname': '安拓锐高新测试技术（苏州）有限公司'
}
print(requests.post("http://localhost:5000/soc/get_info/", data=data).text)