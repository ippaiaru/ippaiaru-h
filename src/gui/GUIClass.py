import threading

from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QFileDialog

import os
from src.gui.baseClass import *
from src.components.start import *
from PyQt5 import QtCore, QtGui, QtWidgets


class GUIClass(QtWidgets.QMainWindow, Ui_BilibiliDanmakuWindow):

    def __init__(self):
        super(GUIClass, self).__init__()
        self.setupUi(self)

        initSaveDir = path.join(path.abspath(path.join(os.getcwd(), '../..')), r'result')
        initAVList = path.join(path.abspath(path.join(os.getcwd(), '../..')), r'res/avList.txt')
        self.lineEdit_saveDir.setText(initSaveDir)
        self.lineEdit_avList.setText(initAVList)
        self.pushButton_selectSaveDir.clicked.connect(self.button_save_openfile)
        self.pushButton_selectAvListDir.clicked.connect(self.button_avListFile)
        self.pushButton_avNumberStart.clicked.connect(self.button_startOne)
        self.pushButton_avListStart.clicked.connect(self.button_startList)
        self.pushButton_openSaveDir.clicked.connect(self.button_openSaveDir)
        self.pushButton_getDanmakuAvNumber.clicked.connect(self.button_getDanmakuFromDB)
        setLogFile(self.lineEdit_saveDir.text())

    def button_save_openfile(self):
        dir_path = QFileDialog.getExistingDirectory(self, "选择文件夹")
        if dir_path != "":
            self.lineEdit_saveDir.setText(dir_path)
            self.label_show_status.setText("存储路径选择完成")

    def button_avListFile(self):
        file_name = QFileDialog.getOpenFileName(self, "选择文件", '', '文本文件(*.txt)')
        if file_name != "":
            self.lineEdit_avList.setText(file_name[0])
            self.label_show_status.setText("av号列表文件选择完成")

    def button_startOne(self):
        avNumber = self.lineEdit_avNumber.text()
        savePath = self.lineEdit_saveDir.text()
        self.label_show_status.setText("正在爬取，请稍等")
        updateGuiTh = threading.Thread(target=monitor_start_one, args=(self, avNumber, savePath))
        updateGuiTh.start()

    def button_startList(self):
        listPath = self.lineEdit_avList.text()
        savePath = self.lineEdit_saveDir.text()
        self.label_show_status.setText("正在爬取，请稍等")
        updateGuiTh = threading.Thread(target=monitor_start_list, args=(self, listPath, savePath))
        updateGuiTh.start()

    def button_openSaveDir(self):
        file_path = self.lineEdit_saveDir.text()
        # QDesktopServices::openUrl(QUrl::fromLocalFile(file_path))
        if os.path.exists(file_path):
            os.system('explorer.exe /n,' + file_path)
        else:
            self.label_show_status.setText("文件夹不存在！")

    def button_getDanmakuFromDB(self):
        aid = self.lineEdit_getDanmakuAvNumber.text()
        self.label_show_status.setText("正在查找弹幕av%s" % aid)
        t = threading.Thread(target=newThreadToGetDanmaku, args=(self, aid))
        t.start()


# self.plainTextEdit.setPlainText(self.plainTextEdit.toPlainText() + aid)


def monitor_start_one(self, avNumber, savePath):
    t = threading.Thread(target=startOne, args=(avNumber, savePath))
    t.start()
    t.join()
    self.label_show_status.setText("%s完成" % avNumber)


def monitor_start_list(self, listPath, savePath):
    t = threading.Thread(target=startList, args=(listPath, savePath))
    t.start()
    t.join()
    self.label_show_status.setText("列表爬取完成！")


def newThreadToGetDanmaku(self, aid):
    result = getDanmakuByAid(aid)
    itemString = ""
    for item in result:
        itemString += '%s, %s\n' % (item['appearTime'], item['content'])
    self.plainTextEdit.setPlainText(self.plainTextEdit.toPlainText() + itemString)
    self.label_show_status.setText("查找弹幕完成av%s" % aid)
