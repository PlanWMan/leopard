import cv2
import numpy as np


def template_demo():
    template = cv2.imread("./6631054651.jpg")
    target = cv2.imread("./6133370076.jpg")
    methods = [cv2.TM_SQDIFF_NORMED, cv2.TM_CCORR_NORMED, cv2.TM_CCOEFF_NORMED]  # 3种模板匹配方法
    th, tw = target.shape[:2]
    for md in methods:
        print(md)
        result = cv2.matchTemplate(target, template, md)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if md == cv2.TM_SQDIFF_NORMED:
            tl = min_loc
        else:
            tl = max_loc
        br = (tl[0] + tw, tl[1] + th)  # br是矩形右下角的点的坐标
        print(tl, br, max_loc)

# 缺口的查找  二值化是数组长度为五
def get_gap(recovery_png, gap_png):
    target = cv2.imread(recovery_png, 0)
    template = cv2.imread(gap_png, 0)
    w, h = target.shape[::-1]
    temp = 'temp.jpg'
    targ = 'targ.jpg'
    cv2.imwrite(temp, template)
    cv2.imwrite(targ, target)
    target = cv2.imread(targ)
    target = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
    target = abs(255 - target)
    cv2.imwrite(targ, target)
    target = cv2.imread(targ)
    template = cv2.imread(temp)
    result = cv2.matchTemplate(target, template, cv2.TM_CCOEFF_NORMED)
    print(cv2.minMaxLoc(result))
    x, y = np.unravel_index(result.argmax(), result.shape)
    # y就是水平缺口
    return y


def FindPic(target, template):
    """
    找出图像中最佳匹配位置
    :param target: 目标即背景图
    :param template: 模板即需要找到的图
    :return: 返回最佳匹配及其最差匹配和对应的坐标
    """
    target_rgb = cv2.imread(target)
    target_gray = cv2.cvtColor(target_rgb, cv2.COLOR_BGR2GRAY)
    template_rgb = cv2.imread(template, 0)
    res = cv2.matchTemplate(target_gray, template_rgb, cv2.TM_CCOEFF_NORMED)
    value = cv2.minMaxLoc(res)
    print(value)

# template_demo()
# get_gap('patch.jpg', 'bg.webp')
# FindPic('patch.jpg','bg.webp')
