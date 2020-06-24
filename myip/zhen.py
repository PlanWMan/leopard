# 导入所需要的库
import cv2
# import numpy as np


# 定义保存图片函数
# image:要保存的图片名字
# addr；图片地址与相片名字的前部分
# num: 相片，名字的后缀。int 类型
def save_image(image, addr, num):
    address = addr + str(num) + '.jpg'
    cv2.imwrite(address, image)


cap = cv2.VideoCapture('./0595917111.gif')
if cap.isOpened():  # 判断是否正常打开
    success, frame = cap.read()
else:
    success = False
# 读帧
i = 0
timeF = 3
img_path = ''
while success:
    success, frame = cap.read()
    i = i + 1
    if (i % timeF == 0):
        img_path = .img_address('.jpg')
        self.cv_save(img_path, frame)
        break
cap.release()
cv2.destroyAllWindows()