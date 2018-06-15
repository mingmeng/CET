# coding: utf-8
import requests
from PIL import Image
from io import BytesIO
from learn_images import get_classifier_from_learn
from utils import *


def get_validate_code_from_image(img):
    img_piece = do_image_crop(img)
    X = img_list_to_array_list(img_piece)
    clf = get_classifier_from_learn()
    y = clf.predict(X)
    return "".join(y)


if __name__ == '__main__':
    r = requests.get("http://cet.neea.edu.cn/imgs/9e1b8b50cafa4c8db1bc77403f6222f1.png")
    img = Image.open(BytesIO(r.content))
    code = get_validate_code_from_image(img)
    print(code)
