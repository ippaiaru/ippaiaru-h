import re
import time

regexColor = r'0x'


def convertTimestampToDateTime(timestamp, outputFormat="%Y-%m-%d %H:%M:%S"):
    return time.strftime(outputFormat, time.localtime(int(timestamp)))


def convertDateTimeToTimestamp(dateTime, inputFormat="%Y-%m-%d %H:%M:%S"):
    return int(time.mktime(time.strptime(dateTime, inputFormat)))


def getDanmakuType(typeNumber):
    typeDict = {1: '滚动弹幕', 2: '滚动弹幕', 3: '滚动弹幕', 4: '底端弹幕',
                5: '顶端弹幕', 6: '逆向弹幕', 7: '精准弹幕', 8: '高级弹幕'}
    return typeDict.get(int(typeNumber))


def getDanmakuFontSize(fontSizeNumber):
    fontSizeDict = {12: '非常小', 16: '很小', 18: '小',
                    25: '中', 36: '大', 45: '很大', 64: '特别大'}
    return fontSizeDict.get(int(fontSizeNumber))


def getDanmakuPool(poolNumber):
    poolDict = {0: '普通池', 1: '字幕池', 2: '特殊池'}
    return poolDict.get(int(poolNumber))


def formatColor(color):
    return '#%s' % re.sub(regexColor, '', str(hex(int(color)))).zfill(6)


def getValueListByKeyFromDict(diction, key):
    valueList = []
    for item in diction:
        valueList.append(item[key])
    return valueList


def sortDictByKey(diction, key, ifReverse=False):
    return sorted(diction, key=lambda s: s[key], reverse=ifReverse)
