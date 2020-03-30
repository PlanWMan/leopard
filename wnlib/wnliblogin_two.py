'''
登录
'''
import cv2
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

username = '1234567'
password = '1234567'


class CrackWeiboSlide():
    def __init__(self):
        self.url = 'http://wnlib.com/login.php'
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--incognito')
        self.browser = webdriver.Chrome(executable_path="D:/tool_wbw/chromedriver_win32/chromedriver.exe",
                                        chrome_options=chrome_options)
        self.wait = WebDriverWait(self.browser, 20)

    def __del__(self):
        self.browser.close()

    def imgcheck(self, USERNAME, PASSWORD):
        self.browser.get(self.url)
        sleep(2)
        username = self.wait.until(EC.presence_of_element_located((By.ID, 'login-username')))
        password = self.wait.until(EC.presence_of_element_located((By.ID, 'login-password')))
        submit = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'l-captcha')))
        username.send_keys(USERNAME)
        password.send_keys(PASSWORD)
        submit.click()
        # 截屏
        sleep(2)
        iframe = self.browser.find_element_by_xpath("//div[starts-with(@id,'l-captcha-image_')]/iframe")
        self.browser.switch_to.frame(iframe)
        while True:
            img = self.browser.find_element_by_xpath("//div[@class='captcha-list']")
            img.screenshot("./yanzhengma.png")
            yz_text = self.browser.find_element_by_xpath('//span[@class="word-text"]/i').text
            # 自动打码
            find_list = [['圆', 'yuan'], ['三', 'sj'], ['方', 'zf'], ['星', 'xing']]
            for find_name in find_list:
                if str(yz_text).split(',')[0].find(find_name[0]) > -1:
                    self.move_mouse(find_name[1])
                    break
            for find_name in find_list:
                if str(yz_text).split(',')[1].find(find_name[0]) > -1:
                    self.move_mouse(find_name[1])
                    break
            if len(str(yz_text).split(',')) == 3:
                for find_name in find_list:
                    if str(yz_text).split(',')[2].find(find_name[0]) > -1:
                        self.move_mouse(find_name[1])
                        break
            sleep(2)
            self.browser.switch_to.default_content()
            iframe_two = self.browser.find_element_by_xpath("//div[@class='l-captcha']/iframe")
            self.browser.switch_to.frame(iframe_two)
            gx_text = self.browser.find_element_by_xpath('//span[@class="captcha-widget-text"]').text
            self.browser.switch_to.default_content()
            if (gx_text).find('恭喜') > -1:
                # 跳出图片认证
                break
            else:
                # 重新换了一张图片
                sleep(2)
                self.browser.switch_to.frame(iframe)
                self.browser.find_element_by_xpath('//span[@class="lc-button lc-refresh"]').click()
                continue
        self.browser.find_element_by_xpath('//button[@class="login100-form-btn"]').click()
        sleep(2)
        self.browser.get('http://wnlib.com/user/single.php?ms=wose&id=700')
        submite = self.wait.until(EC.element_to_be_clickable((By.ID, 'clearIcon1')))
        submite.click()
        input_word = self.browser.find_element_by_xpath('//input[contains(@alt, "输入检索词")]')
        input_word.send_keys('GYNECOLOGIC ONCOLOGY')
        sleep(1)
        cbw_click = self.browser.find_element_by_xpath('//td[@class="search-criteria-cell2"]//b[@role="presentation"]')
        cbw_click.click()
        (self.browser.find_element_by_xpath('//ul[@class="select2-results__options"]/li[4]')).click()
        (self.browser.find_element_by_xpath('//span[@class="searchButton"]')).click()
        sleep(1)
        href_ = self.browser.find_element_by_xpath('//a[contains(@alt, "下一页")]').get_attribute('href')
        qid = str(href_).split('qid=')[1].split('&')[0]
        sid = str(href_).split('SID=')[1].split('&')[0]
        self.browser.close()
        return qid, sid
        # 返回pid和sid

    def find_px(self, path_img):
        '''
        识别验证码坐标
        :param path_img:
        :return:
        '''
        target = cv2.imread("./yanzhengma.png")
        template = cv2.imread("./img/%s.jpg" % (path_img))
        result = cv2.matchTemplate(target, template, cv2.TM_SQDIFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        return min_loc[0] + 10, min_loc[1] + 10

    def move_mouse(self, name):
        # 拖动鼠标模拟点击
        x, y = self.find_px(name)
        write = self.browser.find_element_by_xpath('//span[@class="lc-button lc-refresh"]')
        action = ActionChains(self.browser)
        sleep(1)
        action.move_to_element(write).move_by_offset(-(265 - x), -(170 - y)).click().perform()  # 移动点击


if __name__ == '__main__':
    cws = CrackWeiboSlide()
    pid, sid = cws.imgcheck(username, password)
    print(pid, sid)
