# -*- coding: utf-8 -*-
import threading
from os import path

from src.components.danmakuAnalyser import *
from src.components.getBilibiliDanmaku import *
from src.components.log import *

avListPath = r'res/avList.txt'


def startOne(avNumber, savePath):
    try:
        savePath = folderPathAvailable(savePath)
    except FileExistsError:
        return writeLog("存储路径无效")

    if not path.exists(savePath):
        os.makedirs(savePath)
    setLogFile(savePath)

    body(avNumber, savePath)

    return writeLog("爬取完成")


def startList(avNumberListPath, savePath):
    try:
        savePath = folderPathAvailable(savePath)
    except FileExistsError:
        return writeLog("存储路径无效")
    if not path.exists(savePath):
        os.makedirs(savePath)

    setLogFile(savePath)
    avNumList = open(avNumberListPath).read().split(',')

    for avNumber in avNumList:
        # threading.Thread(target=body, args=(avNumber, savePath)).start() # 多线程绘图会炸..
        body(avNumber, savePath)

    return writeLog("爬取完成")


def body(avNumber, savePath):
    writeLog("开始爬取 av%s" % avNumber)
    avNumber = avNumber.strip()
    try:
        html = getVideoHtmlByAid(avNumber)
    except AttributeError:
        writeErrorLog("av号格式不正确", avNumber)
        return
    except TimeoutError:
        writeErrorLog("获取源代码超时", avNumber)
        return
    except RuntimeError:
        writeErrorLog("获取源码时连接异常", avNumber)
        return

    try:
        videoInfo = getCidAndAid(html)
    except IndexError:
        writeErrorLog("源码出错", avNumber)
        return

    try:
        danmakuSource = getDanmakuHtml(videoInfo)
    except TimeoutError:
        writeErrorLog("获取源代码超时", avNumber)
        return
    except RuntimeError:
        writeErrorLog("获取源码时连接异常", avNumber)
        return

    try:
        danmakuList = getDanmaku(danmakuSource)
    except IndexError:
        writeErrorLog("源码出错", avNumber)
        return

    title = titleAvailable(videoInfo)
    videoPath = path.join(savePath, '%s/' % title)
    excelFolderPath = videoPath
    photoFolderPath = path.join(videoPath, 'photo/')
    if not os.path.exists(photoFolderPath):
        os.makedirs(photoFolderPath)
    print(writeLog('文件夹创建成功 %s' % photoFolderPath))

    writeToMongoDB(videoInfo, danmakuList)
    writeDanmakuToExcel(videoInfo, danmakuList, excelFolderPath)
    countOfTime(videoInfo, danmakuList, photoFolderPath)
    colorAnalyse(videoInfo, danmakuList, photoFolderPath)
    countPerFeizhai(videoInfo, danmakuList, photoFolderPath)
    danmakuHeatMap(videoInfo, danmakuList, photoFolderPath)
    danmakuWordCloud(videoInfo, danmakuList, photoFolderPath)
