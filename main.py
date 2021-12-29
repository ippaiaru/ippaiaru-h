# # -*- coding: utf-8 -*-
# from os import path
#
# from src.components.danmakuAnalyser import *
# from src.components.getBilibiliDanmaku import *
# from src.components.log import *
#
# avListPath = r'res/avList.txt'
#
# if __name__ == '__main__':
#     d = os.path.dirname(__file__)
#     rootPath = d
#     ifNewFolder = False
#     need = input("是否需要自选文件夹路径(y/n)\n")
#     if need == 'y':
#         ifNewFolder = True
#         rootPath = input("输入文件夹路径\n")
#
#     rootPath = folderPathAvailable(rootPath)
#     if not ifNewFolder:
#         rootPath = path.join(rootPath, r'result/')
#     if not path.exists(rootPath):
#         os.makedirs(rootPath)
#     # 以上创建存储根目录
#
#     setLogFile(rootPath)
#     avListPath = os.path.join(d, avListPath)
#     avNumList = open(avListPath).read().split(',')
#
#     for avNumber in avNumList:
#         avNumber = avNumber.strip()
#         try:
#             html = getVideoHtmlByAid(avNumber)
#         except AttributeError:
#             print(writeErrorLog("av号格式不正确：av%s" % avNumber))
#             continue
#         except TimeoutError:
#             print(writeErrorLog("获取视频网页源代码超时：av%s" % avNumber))
#             continue
#         except RuntimeError:
#             print(writeErrorLog("获取视频源码时连接异常：av%s" % avNumber))
#             continue
#
#         try:
#             videoInfo = getCidAndAid(html)
#         except IndexError:
#             print(writeErrorLog("av%s 视频源码出错" % avNumber))
#             continue
#
#         try:
#             danmakuSource = getDanmakuHtml(videoInfo)
#         except TimeoutError:
#             print(writeErrorLog("获取弹幕源码超时", videoInfo=videoInfo))
#             continue
#         except RuntimeError:
#             print(writeErrorLog("获取弹幕源码时连接异常", videoInfo=videoInfo))
#             continue
#
#         try:
#             danmakuList = getDanmaku(danmakuSource)
#         except IndexError:
#             print(writeErrorLog("弹幕源码出错", videoInfo))
#             continue
#
#         title = titleAvailable(videoInfo)
#         videoPath = path.join(rootPath, '%s/' % title)
#         excelFolderPath = videoPath
#         photoFolderPath = path.join(videoPath, 'photo/')
#         if not os.path.exists(photoFolderPath):
#             os.makedirs(photoFolderPath)
#         print(writeLog('文件夹创建成功 %s' % photoFolderPath))
#
#         writeToMongoDB(videoInfo, danmakuList)
#         writeDanmakuToExcel(videoInfo, danmakuList, excelFolderPath)
#         countOfTime(videoInfo, danmakuList, photoFolderPath)
#         colorAnalyse(videoInfo, danmakuList, photoFolderPath)
#         countPerFeizhai(videoInfo, danmakuList, photoFolderPath)
#         danmakuHeatMap(videoInfo, danmakuList, photoFolderPath)
#         danmakuWordCloud(videoInfo, danmakuList, photoFolderPath)
#
#         # print(convertTimestamp(danmakuList[0]['sentTimestamp'], "%m/%d/%Y"))  # test
#         # for danmaku in danmakuList:
#         #     printDanmaku(danmaku)
#         #     print()
