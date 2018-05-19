#爬取花瓣网的图片
'''
引入相关库
'''
import requests
import re
null=''

#构建函数，并将地址传入
def huaban(url):
    r=requests.get(url).content.decode('utf-8')                         # 请求网页，编码格式
    pages=re.compile(r'app\.page\["pins"\].*').findall(r)
    if pages == []:
        null = None                                                     #由于python中是没有null的，所以将其变成none
    globals = {
        'null': 0,
        'true': 1
    }
    result = eval(pages[0][19:-1],globals)                              #将字符串str当成有效的表达式来求值并返回计算结果。
    images = []                                                         #将图片存入一个列表
    for i in result:
        info = {}
        info['id']=str(i['pin_id'])                                                                     #解析pins中的内容
        info['url'] = "http://img.hb.aicdn.com/" + i["file"]["key"] + "_fw658"
        if 'image' == i["file"]["type"][:5]:
            info['type'] = i["file"]["type"][6:]
        else:
            info['type'] = 'NoName'
        images.append(info)
    for image in images:
        req = requests.get(image["url"])
        imageName = image["id"] + "." + image["type"]
        print(image)                                                                                                #将图片地址输出到控制台
    new_url="http://huaban.com/favorite/beauty/?i5p998kw&max=" + images[-1]['id'] + "&limit=20&wfl=1"               #对地址的自动化更新
    huaban(new_url)


#调用函数实现
huaban('http://huaban.com/favorite/beauty/')