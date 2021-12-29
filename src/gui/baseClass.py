# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog


class Ui_BilibiliDanmakuWindow(object):
    def setupUi(self, BilibiliDanmakuWindow):
        BilibiliDanmakuWindow.setObjectName("BilibiliDanmakuWindow")
        BilibiliDanmakuWindow.resize(607, 600)

        self.centralwidget = QtWidgets.QWidget(BilibiliDanmakuWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.lable_avNumber = QtWidgets.QLabel(self.centralwidget)
        self.lable_avNumber.setGeometry(QtCore.QRect(80, 30, 24, 16))
        self.lable_avNumber.setObjectName("lable_avNumber")

        self.lineEdit_avNumber = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_avNumber.setGeometry(QtCore.QRect(120, 30, 113, 20))
        self.lineEdit_avNumber.setObjectName("lineEdit_avNumber")

        self.label_avList = QtWidgets.QLabel(self.centralwidget)
        self.label_avList.setGeometry(QtCore.QRect(40, 80, 81, 16))
        self.label_avList.setObjectName("label_avList")

        self.lineEdit_avList = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_avList.setGeometry(QtCore.QRect(120, 80, 331, 20))
        self.lineEdit_avList.setObjectName("lineEdit_avList")

        self.pushButton_avNumberStart = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_avNumberStart.setGeometry(QtCore.QRect(520, 30, 75, 23))
        self.pushButton_avNumberStart.setObjectName("pushButton_avNumberStart")

        self.pushButton_avListStart = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_avListStart.setGeometry(QtCore.QRect(520, 80, 75, 23))
        self.pushButton_avListStart.setObjectName("pushButton_avListStart")

        self.pushButton_openSaveDir = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_openSaveDir.setGeometry(QtCore.QRect(520, 150, 75, 23))
        self.pushButton_openSaveDir.setObjectName("pushButton_openSaveDir")

        self.checkBox = QtWidgets.QLabel(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(120, 120, 121, 16))
        self.checkBox.setObjectName("checkBox")

        self.pushButton_selectAvListDir = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_selectAvListDir.setGeometry(QtCore.QRect(460, 80, 21, 23))
        self.pushButton_selectAvListDir.setObjectName("pushButton_selectAvListDir")

        self.lineEdit_saveDir = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_saveDir.setGeometry(QtCore.QRect(120, 150, 331, 20))
        self.lineEdit_saveDir.setObjectName("lineEdit_saveDir")

        self.pushButton_selectSaveDir = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_selectSaveDir.setGeometry(QtCore.QRect(460, 150, 21, 23))
        self.pushButton_selectSaveDir.setObjectName("pushButton_selectSaveDir")

        self.label_show_status = QtWidgets.QLabel(self.centralwidget)
        self.label_show_status.setGeometry(QtCore.QRect(240, 180, 200, 16))
        self.label_show_status.setObjectName("label_show_status")

        self.lineEdit_getDanmakuAvNumber = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_getDanmakuAvNumber.setGeometry(QtCore.QRect(120, 220, 113, 20))
        self.lineEdit_getDanmakuAvNumber.setObjectName("lineEdit_getDanmakuAvNumber")

        self.pushButton_getDanmakuAvNumber = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_getDanmakuAvNumber.setGeometry(QtCore.QRect(300, 219, 120, 23))
        self.pushButton_getDanmakuAvNumber.setObjectName("pushButton_getDanmakuAvNumber")

        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setGeometry(QtCore.QRect(10, 250, 580, 320))
        self.plainTextEdit.setObjectName("plainTextEdit")

        BilibiliDanmakuWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(BilibiliDanmakuWindow)
        self.statusbar.setObjectName("statusbar")
        BilibiliDanmakuWindow.setStatusBar(self.statusbar)
        self.retranslateUi(BilibiliDanmakuWindow)

        QtCore.QMetaObject.connectSlotsByName(BilibiliDanmakuWindow)

    def retranslateUi(self, BilibiliDanmakuWindow):
        _translate = QtCore.QCoreApplication.translate
        BilibiliDanmakuWindow.setWindowTitle(_translate("BilibiliDanmakuWindow", "MainWindow"))
        self.lable_avNumber.setText(_translate("BilibiliDanmakuWindow", "av号"))
        self.label_avList.setText(_translate("BilibiliDanmakuWindow", "av号文件路径"))
        self.label_show_status.setText(_translate("BilibiliDanmakuWindow", "初始化完成"))
        self.pushButton_avNumberStart.setText(_translate("BilibiliDanmakuWindow", "使用此av号"))
        self.pushButton_avListStart.setText(_translate("BilibiliDanmakuWindow", "签订契约"))
        self.checkBox.setText(_translate("BilibiliDanmakuWindow", "存储路径"))
        self.pushButton_selectAvListDir.setText(_translate("BilibiliDanmakuWindow", "..."))
        self.pushButton_selectSaveDir.setText(_translate("BilibiliDanmakuWindow", "..."))
        self.pushButton_openSaveDir.setText(_translate("BilibiliDanmakuWindow", "打开文件夹"))
        self.pushButton_getDanmakuAvNumber.setText(_translate("BilibiliDanmakuWindow", "查找弹幕数据"))
        BilibiliDanmakuWindow.setWindowTitle(_translate("MainWindow", "弹幕获取分析"))
