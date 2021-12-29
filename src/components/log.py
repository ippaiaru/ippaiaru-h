import os
import time

from pymongo import *

conn = MongoClient('localhost', 27017)
db = conn.logDB


def setLogFile(rootPath):
    global logFile
    logFile = os.path.join(rootPath, 'log.txt')
    global errorLogFile
    errorLogFile = os.path.join(rootPath, 'errorLog.txt')


def writeLog(information, videoInfo=None):
    now = str(time.strftime('%Y-%m-%d %H-%M-%S', time.localtime(time.time())))
    if videoInfo is None:
        logInfo = '事件：%s\n时间：%s\n\n' % (information, now)
        logDB = {'av号': None, '标题': None, '事件': information, '时间': now}
    else:
        logInfo = 'av%s\n事件：%s\n时间：%s\n\n' % (videoInfo['aid'] + videoInfo['title'], information, now)
        logDB = {'av号': videoInfo['aid'], '标题': videoInfo['title'], '事件': information, '时间': now}
    with open(logFile, 'a')as log:
        log.write(logInfo)
    dbSet = db['log']
    dbSet.insert_one(logDB)
    return logInfo


def writeErrorLog(information, avNumber):
    now = str(time.strftime('%Y-%m-%d %H-%M-%S', time.localtime(time.time())))
    errorLogInfo = 'av号：%s\n事件：%s\n时间：%s\n\n' % (avNumber, information, now)
    errorLogDB = {'av号': avNumber, '事件': information, '时间': now}
    with open(errorLogFile, 'a')as errorLog:
        errorLog.write(errorLogInfo)
    dbSet = db['errorLog']
    dbSet.insert_one(errorLogDB)
    return errorLogInfo

# def writeErrorLog(information, videoInfo=None):
#     now = str(time.strftime('%Y-%m-%d %H-%M-%S', time.localtime(time.time())))
#     if videoInfo is None:
#         errorLogInfo = '事件：%s\n时间：%s\n\n' % (information, now)
#         errorLogDB = {'av号': None, '标题': None, '事件': information, '时间': now}
#     else:
#         errorLogInfo = 'av%s\n事件：%s\n时间：%s\n\n' % (videoInfo['aid'] + videoInfo['title'], information, now)
#         errorLogDB = {'av号': videoInfo['aid'], '标题': videoInfo['title'], '事件': information, '时间': now}
#     with open(errorLogFile, 'a')as errorLog:
#         errorLog.write(errorLogInfo)
#     dbSet = db['errorLog']
#     dbSet.insert_one(errorLogDB)
#     return errorLogInfo
