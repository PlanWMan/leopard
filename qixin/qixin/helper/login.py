"""
用selenium登陆企信的操作
使用 chrome 78 的版本 要不会有检测
chromedriver 的路径要注意
检测完成的更新mongo的cookie 数据
"""
import socket
import os
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from DB.mongo import MongoDao
from configs import chromedrivers
from base.imgbase import ImgBase
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from Tools.ydm import Chaojiying_Client

from time import sleep


class SeleQixin(ImgBase):
    def __init__(self, name='', password='', is_vip=False):
        hostname = socket.gethostname()
        chromedriver_path = chromedrivers[1] if hostname == 'ali-p-python' else chromedrivers[0]
        option = ChromeOptions()
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.browser = webdriver.Chrome(chromedriver_path, options=option)
        self.wait = WebDriverWait(self.browser, 3)
        self.name = name
        self.password = password
        self.is_vip = is_vip
        self.mongo = MongoDao()
        self.cjy = Chaojiying_Client()

    def qixinlogin(self, max=0):
        """
        登陆程序
        """
        try:
            self.browser.get('https://www.qixin.com/auth/login')
            sleep(1)
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
            success = self.huakuai(max)
            if success:
                cookies = self.get_cook()
                if cookies:
                    #  测试cookie
                    #  将cookie 存入mongodb
                    self.update_mongo(cookies)
                    return True
        except:
            print("登陆错误 发送邮件")
        finally:
            self.__del__()

    def djan(self, max=0):
        """
        这是属于cookie 被检测出来需要重新点击解锁
        处理点击按钮进行验证
        """
        an = self.browser.find_elements_by_xpath('//button[@class="btn4"]')
        if an and an[0].text == '点击按钮进行验证':
            an[0].click()
            return self.huakuai(max)
        return True

    def huakuai(self, max):
        huakuai = self.browser.find_elements_by_xpath('//div[@class="geetest_widget"]/div')
        if huakuai:
            # 有验证 如果是文字点击就操作
            sleep(1)
            yc = self.browser.find_elements_by_xpath('//span[@class="geetest_mark"]')
            if yc and yc[0].text == '依次':
                return self.get_dj_two()
            else:
                # 有验证 如果是滑块就过滤
                self.browser.delete_all_cookies()
                if max > 4:
                    return False
                max += 1
                return self.qixinlogin(max)
        return True

    def get_dj(self, url, cookies={}):
        """
        传入cookie和url 测试ip是否需要验证
        """
        self.browser.get('https://www.qixin.com/auth/login')
        for k, v in cookies.items():
            # if k in ['sid', 'acw_sc__v2']:
            self.browser.add_cookie({'name': k, 'value': v})
        self.browser.get(url)
        sleep(1)
        return self.djan()

    def get_dj_two(self, num=0):
        """
        提供点击文字的操作
        """
        if num > 2:
            return False
        self.get_img('./captcha.jpg')
        if os.path.exists('./captcha.jpg'):
            # 提交到打码平台进行打码
            im = open('./captcha.jpg', 'rb').read()
            result = self.cjy.get_gif_9004(im)
            if result.get('err_str') == 'OK':
                pic_id = result.get('pic_id')
                pic_str = result.get('pic_str')
                for x_y in pic_str.split("|"):
                    x, y = str(x_y).split(",")
                    self.move_mouse(x=int(x), y=int(y))
                self.browser.find_element_by_xpath('//a[@class="geetest_commit"]').click()
                sleep(1)
                if self.browser.find_element_by_xpath('//a[@class="geetest_commit"]'):
                    # 认证失败
                    num += 1
                    self.cjy.ReportError(pic_id)
                else:
                    return True
            return self.get_dj_two(num)

    def get_cook(self):
        """
        所有操作都通过了
        """
        cookies = "; ".join([f"{i.get('name')}={i.get('value')}" for i in self.browser.get_cookies()])
        return cookies

    def get_img(self, img_path):
        """
        截取图片
        """
        img = self.browser.find_element_by_xpath('//div[@class="geetest_widget"]')
        img.screenshot(img_path)

    def move_mouse(self, x=10, y=10):
        # 拖动鼠标模拟点击
        write = self.browser.find_element_by_xpath('//a[@class="geetest_close"]')
        action = ActionChains(self.browser)
        sleep(1)
        action.move_to_element(write).move_by_offset(x - 20, -(385 - y)).click().perform()

    def update_mongo(self, cookies):
        item = {
            'username': self.name,
            'passwd': self.password,
            'cookie': cookies,
            'is_normal': 0,  # 判断cookie是否能够使用
            'is_vip': self.is_vip,
            'update_time': self.mongo.now_datetime
        }
        self.mongo.add_or_update('qixin_cookie', {'_id': self.name}, item)

    def __del__(self):
        self.browser.quit()
        self.mongo.close_client()


if __name__ == '__main__':
    SeleQixin(name='18306799369', password='123456qwe').qixinlogin()
