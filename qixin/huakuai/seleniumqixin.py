"""
用selenium登陆企信的操作
使用 chrome 78 的版本 要不会有检测
"""
from selenium import webdriver
from selenium.webdriver import ChromeOptions


class SeleQixin:
    def __init__(self, name, password):
        option = ChromeOptions()
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.browser = webdriver.Chrome('D:/tool/chromedriver_win32/chromedriver.exe', options=option)
        self.name = name
        self.password = password

    def qixinlogin(self, max=0):
        self.browser.get(
            'https://www.qixin.com/search?from=baidusemBrand1&key=%E6%99%AE%E9%81%93%E7%A7%91%E6%8A%80&page=1')
        self.djan(max)
        self.browser.get('https://www.qixin.com/auth/login')
        name = self.browser.find_elements_by_xpath('//input[@type="text"]')
        if name:
            name[0].send_keys(self.name)
        else:
            print("显示不正常，页面错误")
        password = self.browser.find_elements_by_xpath('//input[@type="password"]')
        if password:
            password[0].send_keys(self.password)
        submit = self.browser.find_elements_by_xpath('//div[@class="form-group"]/div')
        if submit:
            submit[0].click()
        self.huakuai(max)
        return self.get_cook()

    def djan(self, max):
        """
        处理点击按钮进行验证
        """
        an = self.browser.find_elements_by_xpath('//button[@class="btn4"]')
        if an and an[0].text == '点击按钮进行验证':
            an[0].click()
            self.huakuai(max)

    def huakuai(self, max):
        huakuai = self.browser.find_elements_by_xpath('//div[@class="form-group"]/div')
        if huakuai:
            if max > 4:
                return None
            max += 1
            self.qixinlogin(max)

    def __del__(self):
        self.browser.quit()


    def get_cook(self):
        """
        所有操作都通过了
        """
        cookies = "; ".join([f"{i.get('name')}={i.get('value')}"for i in self.browser.get_cookies()])
        return cookies


if __name__ == '__main__':
    SeleQixin(name='18306799369', password='123456qwe').qixinlogin()
