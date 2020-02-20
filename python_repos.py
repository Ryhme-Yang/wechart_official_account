# -*-coding:utf-8 -*-
import requests
import urllib.request   # 导入读取url网页的模块
import datetime # 获取系统时间参数
import chardet  # 利用chardet里的detect获取文本编码
import re   # 匹配网页的正则表达式
from urllib import error
from random import choice

# 下载新闻配图download_image函数，输入url：图片地址，our_dir：文件存储名称
def download_image(url, our_dir):
    try:
        res = requests.get(url)
        if res.status_code == 200:
            print("download image successfully:{}".format(url))
            filename = our_dir+'.jpg'
            urllib.request.urlretrieve(url, filename=filename)
            return filename
    except Exception as e:
        print(e)
        return None
    print("download image failed:{}".format(url))

# 将新闻内容写入txt文档
def Write_Text(file_name,contant):
    # file_name = 'test.txt'
    with open(file_name,"a+") as f:
        f.writelines(contant)
        f.writelines("\n")

# 科技新闻
def Content_Resp_keji():
    # 接入API的地址，读取相应的json数据
    url = '******'  # API地址
    r = requests.get(url)
    print("Status code:", r.status_code)
    response_dict = r.json()
    #print(response_dict)
    repo_dicts = response_dict['result']
    repo_dicts_re = repo_dicts['data']
    key = choice(repo_dicts_re)
    content = key['title']+'-'+key['author_name']+' '+key['url']
    return content

# 头条新闻
def Content_Resp_top():
    # 接入API的地址，读取相应的json数据
    url = '******'  # API地址
    r = requests.get(url)
    print("Status code:", r.status_code)
    response_dict = r.json()
    #print(response_dict)
    repo_dicts = response_dict['result']
    repo_dicts_re = repo_dicts['data']
    key = choice(repo_dicts_re)
    content = key['title']+'-'+key['author_name']+' '+key['url']
    return content

# 查询天气
def Content_Resp_Weather(city,date_num):
    url = '******' + city + '******'  # API地址
    r = requests.get(url)
    print("Status code:", r.status_code)
    response_dict = r.json()
    repo_dicts = response_dict['result']
    if date_num == 0:
        content = (repo_dicts['city']
        + '现在的天气是：' + repo_dicts['realtime']['info']
        + '\n温度：' + repo_dicts['realtime']['temperature']
        + '\n空气质量：'  + repo_dicts['realtime']['aqi']
        + '\n风向：' + repo_dicts['realtime']['direct']
        + '\n风力：' + repo_dicts['realtime']['power']
        + '\n湿度：' + repo_dicts['realtime']['humidity'])
    elif date_num == 1:
        repo_dict = repo_dicts['future'][0]
        content = (repo_dicts['city']
        + repo_dict['date'] + '的天气是：' + repo_dict['weather']
        + '\n温度：' + repo_dict['temperature']
        + '\n风向：' + repo_dict['direct'])
    elif date_num == 2:
        repo_dict = repo_dicts['future'][1]
        content = (repo_dicts['city']
        + repo_dict['date'] + '的天气是：' + repo_dict['weather']
        + '\n温度：' + repo_dict['temperature']
        + '\n风向：' + repo_dict['direct'])
    elif date_num == 3:
        repo_dict = repo_dicts['future'][2]
        content = (repo_dicts['city']
        + repo_dict['date'] + '的天气是：' + repo_dict['weather']
        + '\n温度：' + repo_dict['temperature']
        + '\n风向：' + repo_dict['direct'])
    elif date_num == 4:
        repo_dict = repo_dicts['future'][3]
        content = (repo_dicts['city']
        + repo_dict['date'] + '的天气是：' + repo_dict['weather']
        + '\n温度：' + repo_dict['temperature']
        + '\n风向：' + repo_dict['direct'])
    elif date_num == 5:
        repo_dict = repo_dicts['future'][4]
        content = (repo_dicts['city']
        + repo_dict['date'] + '的天气是：' + repo_dict['weather']
        + '\n温度：' + repo_dict['temperature']
        + '\n风向：' + repo_dict['direct'])
    return content

# 爬取吾爱破解本周热帖        
def w2pojie_reptile_week():
    url = 'https://www.52pojie.cn/misc.php?mod=ranklist&type=thread&view=replies&orderby=thisweek'
    try:
        response = urllib.request.urlopen(url)
    except error.HTTPError as e:
        print(e.reason)
    except error.URLError as e:
        print(e.reason)
    html = response.read()  # 调用read()进行读取
    chardit1 = chardet.detect(html) # 利用chardet里的detect获取文本编码 

    pattern = re.compile('<th><a href="(.*?)" target="_blank">(.*)</a>')
    results = pattern.findall(html.decode(chardit1['encoding']))

    result = choice(results)
    content = result[1]+'\n'
    content = content+'https://www.52pojie.cn/'+result[0]

    return content


