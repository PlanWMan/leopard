import base64
from PIL import Image

def img_save(img_path, content):
    """
    保存图片
    """
    with open(img_path, 'wb') as f:
        f.write(content)
img_save('bg.webp', base64.b64decode("data:image/webp;base64,UklGRjoAAABXRUJQVlA4IC4AAACyAgCdASoCAAIALmk0mk0iIiIiIgBoSygABc6WWgAA/veff/0PP8bA//LwYAAA"))
# image = Image.open('bg.JPEG')
# image_format = image.format
# print(image_format)
# im = open('avatar.jpg', 'rb').read()
# print(im)
# print(base64.b64encode(im))
