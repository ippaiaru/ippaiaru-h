# -*- coding: utf-8 -*-
import os
from datetime import datetime
import random
import jieba
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import matplotlib.dates as mdates
from scipy.misc import imread
from wordcloud import WordCloud, ImageColorGenerator
from src.components.danmakuDetailsDealing import *
from src.components.getBilibiliDanmaku import titleAvailable
from src.components.log import writeLog

regexExoticChar = r"[0-9\s+\.\!\/_,$%^*()?;；:-【】+\"\']+|[+——！，;:。？、~@#￥%……&*（）]+"

currentDir = os.path.dirname(__file__)
backDir = os.path.abspath(os.path.join(os.getcwd(), '../..'))  # 背景图片的目录
stopWordsPath = os.path.join(currentDir, r'stopWords.txt')
# fontPath = r'‪K:/code/bilibiliDanmakuAnalyser/res/font/YaHei.ttf' #字体报错了一下午
fontPath = r'c:\windows\fonts\simsun.ttc'
oriBackImagePath = os.path.join(backDir, r'res/backImg')
# os.path.join(backDir, r'./res/backImg')
font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)


# 弹幕数与视频时间关系
def countOfTime(videoInfo, danmakuList, photoFolderPath):
    appearTimeList = getValueListByKeyFromDict(danmakuList, 'appearTime')
    plt.figure(figsize=(12, 9))
    plt.hist(appearTimeList, bins=20, histtype='bar', rwidth=0.8)
    plt.xlabel('视频时间', fontproperties=font)
    plt.ylabel('弹幕数量', fontproperties=font)
    plt.title('%s\nav%s\n弹幕数与时间图' % (videoInfo['title'], videoInfo['aid']), fontproperties=font)

    # 检查path以及title
    filePath = photoFolderPath + '%s_弹幕数与时间图.png' % titleAvailable(videoInfo)
    plt.savefig(filePath)
    print(writeLog('弹幕数与时间图 已生成并存储', videoInfo=videoInfo))
    plt.show()


# 弹幕颜色
def colorAnalyse(videoInfo, danmakuList, photoFolderPath):
    colorList = []
    for danmaku in danmakuList:
        colorList.append(danmaku['color'])
    colorSet = set(colorList)
    colorCountDictList = []
    for item in colorSet:
        colorCountDict = {'color': item,
                          'count': colorList.count(item)}
        colorCountDictList.append(colorCountDict)
    colorCountDictList = sortDictByKey(colorCountDictList, 'count', True)
    colorSet.clear()
    colorName = []
    colorSet = []
    for item in colorCountDictList:
        colorSet.append(item['color'])
        if item['count'] / len(danmakuList) <= 0.005:
            colorName.append('')
        else:
            colorName.append(item['color'])

    colorCount = getValueListByKeyFromDict(colorCountDictList, 'count')
    # ,autopct='%3.1f %%'
    plt.figure(figsize=(19.2, 16.8))
    plt.pie(colorCount, labels=colorName, colors=colorSet, shadow=True, startangle=90)
    plt.title('%s\nav%s\n弹幕颜色饼图' % (videoInfo['title'], videoInfo['aid']), fontproperties=font, fontsize='xx-large')
    plt.tight_layout()
    plt.legend()

    # 检查path以及title
    filePath = photoFolderPath + '%s_弹幕颜色饼图.png' % titleAvailable(videoInfo)
    plt.savefig(filePath)
    print(writeLog('弹幕颜色饼状图 已生成并存储', videoInfo=videoInfo))
    plt.show()


# 用户发送弹幕数饼图
# 这是一个人数图，不是弹幕数图
# 容易弄混
def countPerFeizhai(videoInfo, danmakuList, photoFolderPath):
    feizhaiList = getValueListByKeyFromDict(danmakuList, 'feizhaiId')
    feizhaiSet = set(feizhaiList)
    countList = []
    for item in feizhaiSet:
        countList.append(feizhaiList.count(item))
    feizhaiCountDictList = []

    danmakuCountSet = set(countList)
    for item in danmakuCountSet:
        feizhaiCountDictList.append({'sendDanmakuCount': item, 'feizhaiCount': countList.count(item)})
    feizhaiCountDictList = sortDictByKey(feizhaiCountDictList, 'sendDanmakuCount')

    feizhaiCountList = []
    danmakuCountList = []
    for item in feizhaiCountDictList:
        feizhaiCountList.append(item['feizhaiCount'])
        if item['feizhaiCount'] / len(danmakuList) <= 0.002:
            danmakuCountList.append('')
        else:
            danmakuCountList.append(item['sendDanmakuCount'])

    plt.figure(figsize=(12, 9))
    plt.pie(feizhaiCountList, labels=danmakuCountList, shadow=True, startangle=90)
    plt.title('%s\nav%s\n用户发送弹幕数饼图' % (videoInfo['title'], videoInfo['aid']), fontproperties=font)
    plt.tight_layout()

    # 检查path以及title
    filePath = photoFolderPath + '%s_用户发送弹幕数饼图.png' % titleAvailable(videoInfo)
    plt.savefig(filePath)
    print(writeLog('用户发送弹幕数饼图 已生成并存储', videoInfo=videoInfo))
    plt.show()


# 弹幕数随时间折线图
def danmakuHeatMap(videoInfo, danmakuList, photoFolderPath):
    # TODO：排除高级弹幕。由于高级弹幕不受弹幕池上限影响，需要排除
    originalTimestampList = getValueListByKeyFromDict(danmakuList, 'sentTimestamp')
    timestampList = []
    for item in originalTimestampList:
        timestampList.append(convertDateTimeToTimestamp(convertTimestampToDateTime(item, "%m/%d/%Y"), "%m/%d/%Y"))
    timestampSet = sorted(set(timestampList))
    # 以上是获取对齐到天的排序好的时间戳集合
    dateSet = []
    for item in timestampSet:
        dateSet.append(convertTimestampToDateTime(item, '%m/%d/%Y'))
    danmakuAccumulateCount = []
    danmakuCountPerDay = []
    isFirst = True
    for item in timestampSet:
        if isFirst:
            danmakuAccumulateCount.append(timestampList.count(item))
            isFirst = False
        else:
            danmakuAccumulateCount.append(danmakuAccumulateCount[-1] + timestampList.count(item))
        danmakuCountPerDay.append(timestampList.count(item))

    # 横坐标信息
    xs = [datetime.strptime(d, '%m/%d/%Y').date() for d in dateSet]
    # 配置横轴坐标
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    # 显示图例
    plt.gcf().autofmt_xdate()  # 自动旋转日期标记
    plt.figure(figsize=(12, 9))
    plt.plot(xs, danmakuAccumulateCount, label='弹幕累计数量')
    plt.plot(xs, danmakuCountPerDay, label='弹幕每日数量')
    plt.title('%s\nav%s\n视频弹幕数折线图' % (videoInfo['title'], videoInfo['aid']), fontproperties=font)
    plt.legend(prop=font, loc='best')
    plt.tight_layout()

    # 检查path以及title
    filePath = photoFolderPath + '%s_视频弹幕数折线图.png' % titleAvailable(videoInfo)
    plt.savefig(filePath)
    print(writeLog('视频弹幕数折线图 已生成并存储', videoInfo=videoInfo))
    plt.show()


# 弹幕词云！
def danmakuWordCloud(videoInfo, danmakuList, photoFolderPath):
    isCN = True
    onlyDanmakuList = getValueListByKeyFromDict(danmakuList, 'content')
    # image_path = os.path.join(d, oriBackImagePath % random.randint(1, 7))
    image_path = os.path.join(oriBackImagePath, r'%d.jpg' % random.randint(1, 7))
    usedImagePath = imread(image_path)

    # 词云属性
    wc = WordCloud(font_path=fontPath, background_color="white", max_words=300,
                   mask=usedImagePath, max_font_size=200, random_state=42, margin=4)
    if isCN:
        onlyDanmakuList = cutAndFilter(onlyDanmakuList)
    wc.generate(onlyDanmakuList)

    # image_colors = ImageColorGenerator(backImagePath)

    filePath = photoFolderPath + '%s_弹幕词云.png' % titleAvailable(videoInfo)
    plt.figure(figsize=(19.2, 16.8))
    # plt.imshow(wc.recolor(color_func=image_colors))
    plt.imshow(wc)
    plt.axis("off")
    plt.show()
    wc.to_file(filePath)
    print(writeLog('弹幕词云 已生成并存储', videoInfo=videoInfo))


# 分词与数据清洗
def cutAndFilter(onlyDanmakuList):
    danmakuText = ""
    for item in onlyDanmakuList:
        danmakuText += item
    preOriginWordList = jieba.cut(danmakuText, cut_all=False)
    originWordList = ','.join(preOriginWordList)
    stopWordList = open(stopWordsPath, encoding='utf-8').read().split('\n')
    # stopWor = stopWord
    # stopWordList = stopWor.split('\n')
    wordList = []
    for item in originWordList.split(','):
        if not (item.strip() in stopWordList) and len(item.strip()) > 1:
            if len(set(item)) > 1:
                wordList.append(item)
    return ' '.join(wordList)
