# coding: utf-8
"""
暴力查询模块
1. 根据输入的前10为准考证号，暴力破解后5为准考证号（考场号3位 + 座位号2位）
2. 指定准考证号ID获取指定验证码图片
3. 图片输入机器学习模块，获取验证码值
4. 提交验证码进行查询，获取相应的结果：验证码错误/无结果/非上述两者，查询成功


准考证号列表

a. 获取验证码
b. 提交查询请求
    如果成功：结束
    如果验证码错误：重新获取验证码并提交
    如果查询结果为空：生成新的准考证号并提交

"""
import requests
import json
from PIL import Image
from io import BytesIO
from get_images import get_image_url_and_filename
from settings import image_api, query_api, img_api_headers, query_api_headers
from validate_api import get_validate_code_from_image

# 四级
# myid = "508160172103913";
# name = "曹世霖"
# type = 4;

# # 六级
# myid = "508160172208624";
# name = "章淑惠";
# type = 6;

# 六级


def log_info(*args):
    print("日志：", *args)


def send_query_until_true(myid, name, type):
    # 生成准考证号
    new_id = myid
    # 获取验证码图片地址
    img_api_url = image_api.format(id=new_id)
    img_api_resp = requests.get(img_api_url, headers=img_api_headers)
    img_url, filename = get_image_url_and_filename(img_api_resp.text)
    # 获取验证码图片并猜测
    img_resp = requests.get(img_url)
    code = get_validate_code_from_image(Image.open(BytesIO(img_resp.content)))
    # 执行查询操作
    data = {}
    if type == 4:
        data = {
            "data": "CET4_172_DANGCI,{id},{name}".format(id=new_id, name=name),
            "v": code
        }
        log_info(data)
        query_resp = requests.post(query_api, data=data, headers=query_api_headers)
        query_text = query_resp.text
        log_info(query_text)

        # if "验证码错误" in query_text:
        #     query_text = send_query_until_true(num, type)
        if "验证码错误" in query_text:
            return False
        return query_text
    else:
        data = {
            "data": "CET6_172_DANGCI,{id},{name}".format(id=new_id, name=name),
            "v": code
        }
        log_info(data)
        query_resp = requests.post(query_api, data=data, headers=query_api_headers)
        query_text = query_resp.text
        log_info(query_text)

        if "验证码错误" in query_text:
            return False
        return query_text


def main():
    query_text = "query error"
    myid = "508160172202910";
    name = "严以宁";
    type = 6;

    myid = "508160172103913";
    name = "曹世霖"
    type = 4;


    for num in range(10):
        query_text = send_query_until_true(myid, name, type)

        if (num == 9) & (query_text == False):
            query_text = "<script>document.domain='neea.edu.cn';</script><script>parent.result.callback(\"{error:'查询错误！'}\");</script>"
        if query_text == False:
            continue
        else:
            break
    data = query_text.replace("<script>document.domain='neea.edu.cn';</script><script>parent.result.callback(\"",
                              "").replace("\");</script>", "")
    print(data)


if __name__ == '__main__':
    main()
