# -*- coding: utf-8 -*-
import random
import requests
import xlwt
from pymongo import *
from src.components.danmakuDetailsDealing import *
from src.components.log import writeLog

regexVerdictAvNumber = r'[0-9]+'
regexCidAndAid = r'cid=(.*?)&aid=(.*?)&pre_ad='
regexTitle = r'"title":"(.*?)"'
regexDanmaku = r'<d p="(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?)">(.*?)</d>'
regexTitleAvail = r'\:|\\|\/|\?|\*|\[|\]|<|>'
regexPathAvail = r'[^..+\:]|\?|\*|<|>|\|'

videoRootUrl = 'https://www.bilibili.com/video/av%s'
danmakuRootUrl = 'https://comment.bilibili.com/%s.xml'
requestHeader = None

conn = MongoClient('localhost', 27017)
db = conn.danmakuDB


# av号获取视频源码
def getVideoHtmlByAid(avNumber):
    global requestHeader
    requestHeader = randomHeader()
    if not re.match(regexVerdictAvNumber, avNumber):
        raise AttributeError
    videoUrl = videoRootUrl % avNumber
    try:
        htmlResponse = requests.get(videoUrl, headers=requestHeader, timeout=30)
    except (requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout):
        raise TimeoutError
    except requests.exceptions.ConnectionError:
        raise RuntimeError
    if htmlResponse.status_code != 200:
        raise RuntimeError
    print(writeLog("已获取视频源码：%s" % avNumber))
    return htmlResponse.text


# 网页源码提取视频信息
def getCidAndAid(htmlSource):
    # TODO：分P视频的获取
    try:
        CAid = re.findall(regexCidAndAid, htmlSource)[0]
        title = re.findall(regexTitle, htmlSource)[0]
        return {'cid': CAid[0], 'aid': CAid[1], 'title': title}
    except IndexError:
        raise IndexError


# 通过cid获取弹幕源码
def getDanmakuHtml(videoInfo):
    global requestHeader
    danmakuUrl = danmakuRootUrl % videoInfo['cid']
    try:
        danmakuResponse = requests.get(danmakuUrl, headers=requestHeader, timeout=30)
    except (requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout):
        raise TimeoutError
    except requests.exceptions.ConnectionError:
        raise RuntimeError
    if danmakuResponse.status_code != 200:
        raise RuntimeError
    print(writeLog("已获取弹幕源码", videoInfo=videoInfo))
    return danmakuResponse.text


# xml提取弹幕信息
def getDanmaku(danmakuSource):
    danmakuItems = re.findall(regexDanmaku, danmakuSource, re.S)
    danmakuList = []
    try:
        # for i in range(0, 35):  # 测试用数据
        for danmakuItem in danmakuItems:
            # danmakuItem = danmakuItems[i]
            danmaku = {'appearTime': float(danmakuItem[0]),
                       'type': danmakuItem[1],
                       'fontSize': danmakuItem[2],
                       'color': formatColor(danmakuItem[3]),
                       'sentTimestamp': danmakuItem[4],
                       'pool': danmakuItem[5],
                       'feizhaiId': danmakuItem[6],
                       'repository': danmakuItem[7],
                       'content': danmakuItem[8]}
            danmakuList.append(danmaku)
    except:
        raise IndexError
    print(writeLog("已生成弹幕词典"))
    return danmakuList


# 写入excel
def writeDanmakuToExcel(videoInfo, danmakuList, folderPath):
    title = titleAvailable(videoInfo)
    filePath = folderPath + '弹幕信息_%s.xls' % title

    # 介个似类似于游标的东西⁄(⁄ ⁄•⁄ω⁄•⁄ ⁄)⁄
    row = 4
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = book.add_sheet(title, cell_overwrite_ok=True)
    sheet.write(0, 0, 'av号')
    sheet.write(0, 1, str(videoInfo['aid']))
    sheet.write(1, 0, '视频名称')
    sheet.write(1, 1, videoInfo['title'])
    sheet.write(3, 0, '弹幕出现时间')
    sheet.write(3, 1, '弹幕内容')
    sheet.write(3, 2, '弹幕颜色')
    sheet.write(3, 3, '弹幕发送时间')
    sheet.write(3, 4, '弹幕类型')
    sheet.write(3, 5, '字体大小')
    sheet.write(3, 6, '弹幕池')
    sheet.write(3, 7, '发送者id')
    sheet.write(3, 8, '弹幕id')
    defaultStyle = setDefaultStyle()
    # colorStyleList = []
    for danmaku in danmakuList:
        # isExist = False
        # colorStyle = defaultStyle
        # for item in colorStyleList:
        #     if item.font.colour_index == danmaku['color']:
        #         isExist = True
        #         colorStyle = item
        #         break
        # if not isExist:
        #     colorStyle = setColorStyle(danmaku['color'])
        #     colorStyleList.append(colorStyle)
        sheet.write(row, 0, danmaku['appearTime'], defaultStyle)
        sheet.write(row, 1, danmaku['content'], defaultStyle)
        sheet.write(row, 2, danmaku['color'], defaultStyle)
        sheet.write(row, 3, convertTimestampToDateTime(danmaku['sentTimestamp']), defaultStyle)
        sheet.write(row, 4, getDanmakuType(danmaku['type']), defaultStyle)
        sheet.write(row, 5, getDanmakuFontSize(danmaku['fontSize']), defaultStyle)
        sheet.write(row, 6, getDanmakuPool(danmaku['pool']), defaultStyle)
        sheet.write(row, 7, danmaku['feizhaiId'], defaultStyle)
        sheet.write(row, 8, danmaku['repository'], defaultStyle)
        row += 1

    book.save(filePath)
    print(writeLog('写入excel已成功', videoInfo=videoInfo))


def setDefaultStyle():
    style = xlwt.XFStyle()  # 初始化样式
    font = xlwt.Font()  # 为样式创建字体
    # 字体类型：比如宋体、仿宋
    font.name = '宋体'
    # 定义格式
    style.font = font
    return style


# 写入数据库
def writeToMongoDB(videoInfo, danmakuList):
    aid = videoInfo['aid']
    dbSet = db[aid]
    for danmaku in danmakuList:
        danmakuJson = {'appearTime': danmaku['appearTime'],
                       'type': danmaku['type'],
                       'fontSize': danmaku['fontSize'],
                       'color': danmaku['color'],
                       'sentTimestamp': danmaku['sentTimestamp'],
                       'pool': danmaku['pool'],
                       'feizhaiId': danmaku['feizhaiId'],
                       'repository': danmaku['repository'],
                       'content': danmaku['content']}
        dbSet.insert_one(danmakuJson)
    print(writeLog("av%s弹幕已存至数据库" % videoInfo['aid'], videoInfo))


# 查询数据库
def getDanmakuByAid(avNumebr):
    dbSet = db[avNumebr]
    queryArgs = {}
    projectionFields = {'appearTime': True, 'content': True}  # 用字典指定
    result = dbSet.find(queryArgs, projection=projectionFields)
    print(writeLog("查找数据库已完成 av%s" % avNumebr))
    return result


# def setColorStyle(color):
#     style = xlwt.XFStyle()  # 初始化样式
#     font = xlwt.Font()  # 为样式创建字体
#     # 字体类型：比如宋体、仿宋
#     font.name = '宋体'
#     # 设置字体颜色
#     font.colour = color
#     font.bold = True
#     # 字体大小
#     # font.height = height
#     # 定义格式
#     style.font = font
#     return style


# 判断filePath是否正确
def folderPathAvailable(folderPath):
    folderPath = folderPath.strip()
    # folderPath判断
    while not re.match(regexPathAvail, folderPath):
        raise FileExistsError
    return folderPath


def titleAvailable(videoInfo):
    title = videoInfo['title']
    if len(title) >= 31:
        title = 'av' + videoInfo['aid']
    title = re.sub(regexTitleAvail, '', title, re.S)
    return title


# 输出一行数据
def printDanmaku(danmaku):
    print("弹幕内容：%s" % danmaku['content'])
    print("弹幕颜色：%s" % danmaku['color'])
    print("弹幕出现时间：第%s秒" % danmaku['appearTime'])
    print("弹幕发送时间：%s" % convertTimestampToDateTime(danmaku['sentTimestamp']))


# 随机请求头
def randomHeader():
    headConnection = ['Keep-Alive', 'close']
    headAccept = ['text/html, application/xhtml+xml, */*']
    headAcceptLanguage = ['zh-CN,fr-FR;q=0.5', 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3']
    userAgent = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.2; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; Media Center PC 6.0; InfoPath.2; MS-RTC LM 8)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0 Zune 3.0)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; MS-RTC LM 8)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; MS-RTC LM 8)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET CLR 4.0.20402; MS-RTC LM 8)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET CLR 1.1.4322; InfoPath.2)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; Tablet PC 2.0)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET CLR 3.0.04506; Media Center PC 5.0; SLCC1)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; Tablet PC 2.0; .NET CLR 3.0.04506; Media Center PC 5.0; SLCC1)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; FDM; Tablet PC 2.0; .NET CLR 4.0.20506; OfficeLiveConnector.1.4; OfficeLivePatch.1.3)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET CLR 3.0.04506; Media Center PC 5.0; SLCC1; Tablet PC 2.0)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET CLR 1.1.4322; InfoPath.2)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.3029; Media Center PC 6.0; Tablet PC 2.0)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2)',
        'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 6.0)',
        'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)',
        'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1; Media Center PC 3.0; .NET CLR 1.0.3705; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.1)',
        'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1; FDM; .NET CLR 1.1.4322)',
        'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1; .NET CLR 1.1.4322; InfoPath.1; .NET CLR 2.0.50727)',
        'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1; .NET CLR 1.1.4322; InfoPath.1)',
        'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1; .NET CLR 1.1.4322; Alexa Toolbar; .NET CLR 2.0.50727)',
        'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1; .NET CLR 1.1.4322; Alexa Toolbar)',
        'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
        'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.40607)',
        'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1; .NET CLR 1.1.4322)',
        'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1; .NET CLR 1.0.3705; Media Center PC 3.1; Alexa Toolbar; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
        'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
        'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; el-GR)',
        'Mozilla/5.0 (MSIE 7.0; Macintosh; U; SunOS; X11; gu; SV1; InfoPath.2; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648)',
        'Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 6.0; WOW64; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; c .NET CLR 3.0.04506; .NET CLR 3.5.30707; InfoPath.1; el-GR)',
        'Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 6.0; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; c .NET CLR 3.0.04506; .NET CLR 3.5.30707; InfoPath.1; el-GR)',
        'Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 6.0; fr-FR)',
        'Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 6.0; en-US)',
        'Mozilla/5.0 (compatible; MSIE 7.0; Windows NT 5.2; WOW64; .NET CLR 2.0.50727)',
        'Mozilla/4.79 [en] (compatible; MSIE 7.0; Windows NT 5.0; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 1.1.4322; .NET CLR 3.0.04506.30; .NET CLR 3.0.04506.648)',
        'Mozilla/4.0 (Windows; MSIE 7.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)',
        'Mozilla/4.0 (Mozilla/4.0; MSIE 7.0; Windows NT 5.1; FDM; SV1; .NET CLR 3.0.04506.30)',
        'Mozilla/4.0 (Mozilla/4.0; MSIE 7.0; Windows NT 5.1; FDM; SV1)',
        'Mozilla/4.0 (compatible;MSIE 7.0;Windows NT 6.0)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0;)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; YPC 3.2.0; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; InfoPath.2; .NET CLR 3.5.30729; .NET CLR 3.0.30618)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; YPC 3.2.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 3.0.04506)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; WOW64; SLCC1; Media Center PC 5.0; .NET CLR 2.0.50727)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; WOW64; SLCC1; .NET CLR 3.0.04506)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; WOW64; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; InfoPath.2; .NET CLR 3.5.30729; .NET CLR 3.0.30618; .NET CLR 1.1.4322)']
    header = {
        'Connection': headConnection[0],
        'Accept': headAccept[0],
        'Accept-Language': headAcceptLanguage[1],
        'User-Agent': userAgent[random.randrange(0, len(userAgent))]
    }
    return header
