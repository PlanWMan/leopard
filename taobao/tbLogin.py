import asyncio
import random
import time
from pyppeteer import launch
from retrying import retry
username = ''
password = ''
url = "https://login.taobao.com/member/login.jhtml"

async def page_evaluate(page):
    # 替换淘宝在检测浏览时采集的一些参数
    await page.evaluate('''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => undefined } }) }''')
    await page.evaluate('''() =>{ window.navigator.chrome = { runtime: {},  }; }''')
    await page.evaluate('''() =>{ Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] }); }''')
    await page.evaluate('''() =>{ Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], }); }''')

async def taobao_login():
    """
    淘宝登录主程序
    :param username: 用户名
    :param password: 密码
    :param url: 登录网址
    :return: 登录cookies
    """
    # 'headless': False如果想要浏览器隐藏更改False为True
    browser = await launch({'headless': False,'userDataDir': r"D:\tool_wbw\laji",  'args': ['–no-sandbox'], 'dumpio': True})
    # context = await browser.createIncogniteBrowserContext() #  开启无痕浏览器模式
    page = await browser.newPage()
    await page.setViewport({'width': 1366, 'height': 768})
    await page.setUserAgent(
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36')
    await page.goto(url)
    # 以下为插入中间js，将淘宝会为了检测浏览器而调用的js修改其结果
    await page_evaluate(page)
    try:
        await page.click('a[class="forget-pwd J_Quick2Static"]')  # 直接点击手机登录
    except:
        pass
    # 选中输入框
    # print(await page.content())  # 获取所有html内容
    element = await page.J('#TPL_username_1')
    input_text = await (await element.getProperty('value')).jsonValue()  # 获取内容
    if input_text:
        # 删除输入框里的内容
        await element.click({'clickCount': 3})  # 单击输入框三次选中
    # 清空输入框里的内容
    await page.waitFor(1000)
    # 输入用户名，密码
    await page.type('#TPL_username_1', username, {'delay': input_time_random() - 50})  # delay是限制输入的时间
    await page.type('#TPL_password_1', password, {'delay': input_time_random()})
    await page.click('#J_SubmitStatic')
    await page.waitFor(5000)
    # 检测页面是否有滑块。原理是检测页面元素。
    await page.goto("https://item.taobao.com/item.htm?spm=a1z10.3-c-s.w4002-21751133153.36.34a71c25sWbtXt&id=603204667734")
    await page.waitFor(3000)
    # 检测是否有新的登录验证
    iframe_element = await page.J('iframe#sufei-dialog-content')
    if iframe_element:
        iframe = await iframe_element.contentFrame()
        try:
            # 重新登录代表gg了
            await iframe.type('#TPL_username_1', username, {'delay': input_time_random() - 50})
            await iframe.type('#TPL_password_1', password, {'delay': input_time_random()})
            await iframe.click('#J_SubmitStatic')
        except:
            # 有滑块就还行
            pass

    await page.waitFor(5000)
    # await page.screenshot({'path': './headless-test-result.png'})
    # time.sleep(2)
    # slider = await page.xpath('//strong[@id="J_SellCounter"]/text()') # 检查销售量查看是否有滑块
    # iframe_element = await page.xpath("//div[@id='content_left']")  # 是否有滑块
    # print('')
    # if slider:
    #     print('当前页面出现滑块')
    #     while True:
    #         print('刷新')
    #         # 用于滑动失败刷新
    #         flag, page = await mouse_slide(page=page)
    #         fresh = ''
    #         try:
    #             fresh = await page.Jeval('.errloading', 'node => node.textContent')
    #         except:
    #             pass
    #         if fresh:
    #             await page.hover('a[href="javascript:noCaptcha.reset(1)"]')
    #             await page.mouse.down()
    #             await page.mouse.up()
    #             time.sleep(1)
    #         else:
    #             break
    cookies2 = await page.cookies()
    cookie = "; ".join(["%s=%s" % (i['name'], i['value']) for i in cookies2])
    print('over')
    await page.waitFor(3000)
    await page.close()
    # await context.close()
    await browser.close()
    return cookie

def retry_if_result_none(result):
    return result is None

@retry(retry_on_result=retry_if_result_none,)
async def mouse_slide(page=None, frame=None):
    await asyncio.sleep(2)
    try:
        # 鼠标移动到滑块，按下，滑动到头（然后延时处理），松开按键
        if frame:
            await frame.hover('#nc_1_n1z')
        else:
            await page.hover('#nc_1_n1z')
        await page.mouse.down()
        await page.mouse.move(2000, 0, {'delay': random.randint(1000, 2000)})
        await page.mouse.up()
    except Exception as e:
        print(e, ':验证失败')
        return None, page
    else:
        await asyncio.sleep(2)
        # 判断是否通过
        slider_again = ''
        try:
            slider_again = await page.Jeval('.nc-lang-cnt', 'node => node.textContent')
        except:
            pass
        if slider_again != '验证通过':
            return None, page
        else:
            print('验证通过')
            return 1, page


def input_time_random():
    return random.randint(100, 151)


if __name__ == '__main__':
    files = open("./cookies.txt", "a")
    for i in range(100):
        task = asyncio.get_event_loop().run_until_complete(taobao_login())
        print(task)
        files.write(task+"\n")

