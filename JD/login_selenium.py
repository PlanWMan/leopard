import base64
import random
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from JD.quekou import get_gap
def img_save(img_path, content):
    """
    保存图片
    """
    with open(img_path, 'wb') as f:
        f.write(content)
class SeleQixin():
    def __init__(self):
        option = ChromeOptions()
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.browser = webdriver.Chrome('D:/tool/chromedriver_win32/chromedriver.exe', options=option)
        self.wait = WebDriverWait(self.browser, 3)

    def get_track7(self, distance):
        """
        根据偏移量和手动操作模拟计算移动轨迹
        :param distance: 偏移量
        :return: 移动轨迹
        """
        # 移动轨迹
        tracks = []
        # 当前位移
        current = 0
        # 减速阈值
        mid = distance * 4 / 5
        # 时间间隔
        t = 0.2
        # 初始速度
        v = 0
        sum_ = 0

        while current < distance:
            if current < mid:
                a = random.uniform(2, 5)
            else:
                a = -(random.uniform(12.5, 13.5))
            v0 = v
            v = v0 + a * t
            x = v0 * t + 1 / 2 * a * t * t
            current += x

            if 0.6 < current - distance < 1:
                x = x - 0.53
            elif 1 < current - distance < 1.5:
                x = x - 1.4
            elif 1.5 < current - distance < 3:
                x = x - 1.8
            tt = round(x, 2)
            sum_ += tt
            tracks.append(sum_)

        return tracks

    def login(self, user, password):
        self.browser.get('https://passport.jdpay.com/user/entry.do?')

        self.browser.find_elements_by_xpath('//input[@name="username"]')[0].send_keys(user)
        self.browser.find_elements_by_xpath('//input[@type="password"]')[0].send_keys(password)
        self.browser.find_elements_by_xpath('//a[@name="submit"]')[0].click()
        # 检测登陆的页面
        bg = self.browser.find_element_by_xpath('//div[@class="JDJRV-bigimg"]/img').get_attribute('src')
        patch = self.browser.find_element_by_xpath('//div[@class="JDJRV-smallimg"]/img').get_attribute('src')
        img_save('bg.jpg', base64.b64decode(str(bg).split('base64,')[1]))
        img_save('patch.jpg', base64.b64decode(str(patch).split('base64,')[1]))

        x = (get_gap('patch.jpg', 'bg.webp')) * 0.73 + 25  # 水平缺口距离
        huakuai = self.browser.find_elements_by_xpath('//div[@class="JDJRV-slide-inner JDJRV-slide-btn"]')[0]
        tracks = self.get_track7(x)
        # 拖动滑块

        ActionChains(self.browser).click_and_hold(huakuai).perform()
        A = 0
        for x in tracks:
            x2 = x - A
            A = x
            yoffset_random = random.uniform(-2, 4)
            ActionChains(self.browser).move_by_offset(xoffset=x2, yoffset=yoffset_random).perform()
        ActionChains(self.browser).pause(0.5).release().perform()
        pass




SeleQixin().login(user='18306799369', password='123456')
