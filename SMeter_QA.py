# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""
# while True:
#     user_password = input('Please input your password:')
#     if user_password == '123':
#         print('Thanks for login!')
#         print('开始运行')
#         break
#     else:
#         print('Your password is wrong!')
#         print('Please input again!')

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QColor
from ui.Ui_SMeter_QA import Ui_MainWindow
from database_setting import database_setting
from db_Oracle import oral_operate
import os
import configparser
from typechange import typechange
from algorithm import algorithm
import traceback
import threads

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """

    def __init__(self, parent=None):
        """
        Constructor

        @param parent reference to the parent widget
        @type QWidget
        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        # self.setWindowFlags(Qt.Window)
        self.showMaximized()
        self.setWindowFlags(Qt.WindowStaysOnBottomHint)
        self.database_set = database_setting()
        self.database_info = []
        self.database_info_old = []

        currentPath = os.getcwd()

        ini_path = currentPath + "\manu_config.ini"
        ini_exist = os.path.exists(ini_path)

        if ini_exist == 0:
            try:
                # -----创建配置文件config.ini---------
                # TODO
                config = configparser.ConfigParser()
                config.add_section("预警图")

                # config.set("预警图", "厂家", "全部公司")
                # self.ComboBox_factory.addItem("全部公司")
                # self.ComboBox_factory_sub.addItem("全部公司")

                config.set("预警图", "起始时间", self.DateTimeEdit_alert_start.text())
                config.set("预警图", "结束时间", self.DateTimeEdit_alert_end.text())

                config.add_section("分项预警图")
                config.set("分项预警图", "起始时间", self.DateTimeEdit_subalert_start.text())
                config.set("分项预警图", "结束时间", self.DateTimeEdit_subalert_end.text())

                config.add_section("日计时误差预警图")
                config.set("日计时误差预警图", "起始时间", self.DateTimeEdit_terror_start.text())
                config.set("日计时误差预警图", "结束时间", self.DateTimeEdit_terror_end.text())
                config.write(open(r"%s" % ini_path, "w"))
            except:
                traceback.print_exc()
        elif ini_exist == 1:

            # ---已存在配置文件，
            try:
                # ---读取当前exist的数值
                config = configparser.ConfigParser()
                config.read_file(open(r"%s" % ini_path))

                # manu_factory = config.get("预警图", "厂家")
                # list_factory = manu_factory.split(',')
                # for i in range(len(list_factory)):
                #     self.ComboBox_factory.addItem(list_factory[i])
                #     self.ComboBox_factory_sub.addItem(list_factory[i])

                alertStartDateTime = config.get("预警图", "起始时间")
                alertEndDateTime = config.get("预警图", "结束时间")
                self.DateTimeEdit_alert_start.setDateTime(QtCore.QDateTime(QtCore.QDate(int(alertStartDateTime[0:4]),
                                                                                       int(alertStartDateTime[5:7]),
                                                                                       int(alertStartDateTime[8:10])),
                                                                          QtCore.QTime(int(alertStartDateTime[11:13]),
                                                                                       int(alertStartDateTime[14:16]),
                                                                                       int(alertStartDateTime[17:]))
                                                                          ))
                self.DateTimeEdit_alert_end.setDateTime(QtCore.QDateTime(QtCore.QDate(int(alertEndDateTime[0:4]),
                                                                                        int(alertEndDateTime[5:7]),
                                                                                        int(alertEndDateTime[8:10])),
                                                                           QtCore.QTime(int(alertEndDateTime[11:13]),
                                                                                        int(alertEndDateTime[14:16]),
                                                                                        int(alertEndDateTime[17:]))
                                                                           ))

                subalertStartDateTime = config.get("分项预警图", "起始时间")
                subalertEndDateTime = config.get("分项预警图", "结束时间")
                self.DateTimeEdit_subalert_start.setDateTime(QtCore.QDateTime(QtCore.QDate(int(subalertStartDateTime[0:4]),
                                                                                        int(subalertStartDateTime[5:7]),
                                                                                        int(subalertStartDateTime[8:10])),
                                                                           QtCore.QTime(int(subalertStartDateTime[11:13]),
                                                                                        int(subalertStartDateTime[14:16]),
                                                                                        int(subalertStartDateTime[17:]))
                                                                           ))
                self.DateTimeEdit_subalert_end.setDateTime(QtCore.QDateTime(QtCore.QDate(int(subalertEndDateTime[0:4]),
                                                                                      int(subalertEndDateTime[5:7]),
                                                                                      int(subalertEndDateTime[8:10])),
                                                                         QtCore.QTime(int(subalertEndDateTime[11:13]),
                                                                                      int(subalertEndDateTime[14:16]),
                                                                                      int(subalertEndDateTime[17:]))
                                                                         ))

                terrorStartDateTime = config.get("日计时误差预警图", "起始时间")
                terrorEndDateTime = config.get("日计时误差预警图", "结束时间")
                self.DateTimeEdit_terror_start.setDateTime(QtCore.QDateTime(QtCore.QDate(int(terrorStartDateTime[0:4]),
                                                                                        int(terrorStartDateTime[5:7]),
                                                                                        int(terrorStartDateTime[8:10])),
                                                                           QtCore.QTime(int(terrorStartDateTime[11:13]),
                                                                                        int(terrorStartDateTime[14:16]),
                                                                                        int(terrorStartDateTime[17:]))
                                                                           ))
                self.DateTimeEdit_terror_end.setDateTime(QtCore.QDateTime(QtCore.QDate(int(terrorEndDateTime[0:4]),
                                                                                      int(terrorEndDateTime[5:7]),
                                                                                      int(terrorEndDateTime[8:10])),
                                                                         QtCore.QTime(int(terrorEndDateTime[11:13]),
                                                                                      int(terrorEndDateTime[14:16]),
                                                                                      int(terrorEndDateTime[17:]))
                                                                         ))
            except:
                traceback.print_exc()

        self.alertData1 = []
        self.alertData2 = []
        self.tableWidget_alert.clicked.connect(self.alert_clicked)
        self.tableWidget_alert.activated.connect(self.alert_clicked)

        self.subalertData1 = []
        self.subalertData2 = []
        self.tableWidget_subalert.clicked.connect(self.subalert_clicked)
        self.tableWidget_subalert.activated.connect(self.subalert_clicked)
        # self.tableWidget_alert.

        self.terrorMData1 = []
        self.terrorSData1 = []
        self.terrorMData2 = []
        self.terrorSData2 = []
        self.tableWidget_terror.clicked.connect(self.terror_clicked)
        self.tableWidget_terror.activated.connect(self.terror_clicked)



    @pyqtSlot()
    def on_pushButton_database_setting_clicked(self):
        """
        Slot documentation goes here.
        """
        try:
            self.database_set.setWindowFlags(Qt.Dialog)
        except Exception as e:
            print(e)
        self.database_set.show()

        self.database_set.signal_connect.connect(self.get_database_setting)
        self.database_set.signal_connect_2.connect(self.get_database_setting2)

    def get_database_setting(self, database_setting):

        try:
            self.database_info = database_setting
            if self.database_info != [] and self.database_info_old != []:
                db_op = oral_operate.oracledb(self.database_info[0], self.database_info[1], self.database_info[2])
                db_op_old = oral_operate.oracledb_old(self.database_info_old[0], self.database_info_old[1], self.database_info_old[2])
                flag = db_op.checkconnect()
                flag_old = db_op_old.checkconnect()
                if flag and flag_old:
                    self.factoryThread = threads.factoryThread()
                    self.factoryThread.setValue(self.database_info, self.database_info_old)
                    self.factoryThread.signal_factorydata.connect(self.factory_exec)
                    self.factoryThread.start()
        except:
            traceback.print_exc()

    def get_database_setting2(self, database_setting):
        try:
            self.database_info_old = database_setting
            if self.database_info != [] and self.database_info_old != []:
                db_op = oral_operate.oracledb(self.database_info[0], self.database_info[1], self.database_info[2])
                db_op_old = oral_operate.oracledb_old(self.database_info_old[0], self.database_info_old[1],
                                                      self.database_info_old[2])
                flag = db_op.checkconnect()
                flag_old = db_op_old.checkconnect()
                if flag and flag_old:
                    self.factoryThread = threads.factoryThread()
                    self.factoryThread.setValue(self.database_info, self.database_info_old)
                    self.factoryThread.signal_factorydata.connect(self.factory_exec)
                    self.factoryThread.start()
        except:
            traceback.print_exc()

    def factory_exec(self, factoryList):
        try:
            self.ComboBox_factory.clear()
            self.ComboBox_factory_sub.clear()
            self.ComboBox_factory.addItem("全部厂家")
            self.ComboBox_factory_sub.addItem("全部厂家")
            for i in range(len(factoryList)):
                self.ComboBox_factory.addItem(factoryList[i])
                self.ComboBox_factory_sub.addItem(factoryList[i])
        except:
            traceback.print_exc()

    @pyqtSlot()
    def on_pushButton_batch_clicked(self):
        self.pushButton_batch.setDisabled(True)
        if self.database_info == [] or self.database_info_old == []:
            QtWidgets.QMessageBox.warning(self, "Warning:", "请先进行数据库配置！")
            self.pushButton_batch.setEnabled(True)
            return
        if self.ComboBox_factory.currentText() == '全部厂家':
            QtWidgets.QMessageBox.warning(self, "Warning:", "请选择厂家！")
            self.pushButton_batch.setEnabled(True)
            return
        try:
            db_op = oral_operate.oracledb(self.database_info[0], self.database_info[1], self.database_info[2])
            db_op_old = oral_operate.oracledb_old(self.database_info_old[0], self.database_info_old[1], self.database_info_old[2])
            flag = db_op.checkconnect()
            flag_old = db_op_old.checkconnect()
            if flag and flag_old:
                self.batchThread = threads.batchThread()
                self.batchThread.setValue(self.database_info, self.database_info_old, self.ComboBox_factory.currentText())
                self.batchThread.signal_batchdata.connect(self.batch_exec)
                self.batchThread.start()
        except:
            traceback.print_exc()
            self.pushButton_batch.setEnabled(True)
            
    def batch_exec(self, batchList):
        self.ComboBox_batch.clear()
        self.ComboBox_batch.addItem("全部批次")
        for i in range(len(batchList)):
            self.ComboBox_batch.addItem(batchList[i])
        self.pushButton_batch.setEnabled(True)

    def on_pushButton_batch_sub_clicked(self):
        self.pushButton_batch_sub.setDisabled(True)
        if self.database_info == [] or self.database_info_old == []:
            QtWidgets.QMessageBox.warning(self, "Warning:", "请先进行数据库配置！")
            self.pushButton_batch_sub.setEnabled(True)
            return
        if self.ComboBox_factory_sub.currentText() == '全部厂家':
            QtWidgets.QMessageBox.warning(self, "Warning:", "请选择厂家！")
            self.pushButton_batch_sub.setEnabled(True)
            return
        try:
            db_op = oral_operate.oracledb(self.database_info[0], self.database_info[1], self.database_info[2])
            db_op_old = oral_operate.oracledb_old(self.database_info_old[0], self.database_info_old[1],
                                                  self.database_info_old[2])
            flag = db_op.checkconnect()
            flag_old = db_op_old.checkconnect()
            if flag and flag_old:
                self.batchsubThread = threads.batchsubThread()
                self.batchsubThread.setValue(self.database_info, self.database_info_old,
                                          self.ComboBox_factory_sub.currentText())
                self.batchsubThread.signal_batchsubdata.connect(self.batchsub_exec)
                self.batchsubThread.start()
        except:
            traceback.print_exc()
            self.pushButton_batch_sub.setEnabled(True)

    def batchsub_exec(self, batchsubList):
        self.ComboBox_batch_sub.clear()
        self.ComboBox_batch_sub.addItem("全部批次")
        for i in range(len(batchsubList)):
            self.ComboBox_batch_sub.addItem(batchsubList[i])
        self.pushButton_batch_sub.setEnabled(True)
        
    @pyqtSlot()
    def on_pushButton_alert_clicked(self):
        self.pushButton_alert.setDisabled(True)
        if self.database_info == [] or self.database_info_old == []:
            QtWidgets.QMessageBox.warning(self, "Warning:", "请先进行数据库配置！")
            self.pushButton_alert.setEnabled(True)
            return
        currentPath = os.getcwd()
        ini_path = currentPath + "\manu_config.ini"
        ini_exist = os.path.exists(ini_path)
        # ---if database_config is not exist created it-------
        config = configparser.ConfigParser()
        if ini_exist == 0:
            QtWidgets.QMessageBox.warning(self, "Warning:", "配置文件丢失，请重启软件！")
            return
        else:
            # -----改写exiest的数值
            try:
                config.read(r"%s" % ini_path)

                # manu_factory = config.get("预警图", "厂家")
                # list_factory = manu_factory.split(',')
                # factoryText = self.ComboBox_factory.currentText()
                # factoryText_sub = self.ComboBox_factory_sub.currentText()
                # if self.ComboBox_factory.currentText() not in list_factory:
                #     list_factory.append(self.ComboBox_factory.currentText())
                # manu_factory = ','.join(list_factory)
                # config.set("预警图", "厂家", manu_factory)
                # self.ComboBox_factory.clear()
                # self.ComboBox_factory_sub.clear()
                # for i in range(len(list_factory)):
                #     self.ComboBox_factory.addItem(list_factory[i])
                #     self.ComboBox_factory_sub.addItem(list_factory[i])
                # self.ComboBox_factory.setCurrentText(factoryText)
                # self.ComboBox_factory_sub.setCurrentText(factoryText_sub)

                config.set("预警图", "起始时间", self.DateTimeEdit_alert_start.text())
                config.set("预警图", "结束时间", self.DateTimeEdit_alert_end.text())
                config.write(open(r"%s" % ini_path, "r+"))
            except:
                traceback.print_exc()

        try:

            db_op = oral_operate.oracledb(self.database_info[0], self.database_info[1], self.database_info[2])
            db_op_old = oral_operate.oracledb_old(self.database_info_old[0], self.database_info_old[1],
                                                  self.database_info_old[2])
            flag = db_op.checkconnect()
            flag_old = db_op_old.checkconnect()
            if flag and flag_old:
                self.alertThread = threads.alertThread()
                self.alertThread.setValue(self.database_info, self.database_info_old, self.DateTimeEdit_alert_start.text(), self.DateTimeEdit_alert_end.text(),
                                          self.ComboBox_factory.currentText(), self.ComboBox_batch.currentText())
                # self.alertThread.signal_zerodata.connect(self.zero_exec)
                self.alertThread.signal_alertdata.connect(self.alert_exec)
                self.alertThread.signal_factory.connect(self.factory_label)
                self.alertThread.start()
        except:
            traceback.print_exc()
            self.pushButton_alert.setEnabled(True)
            # ---------set datas----------
            # meanlist = []
            # for i in range(60):
            #     for j in range(20):
            #         mean = float(self.alertData[i][j][0])
            #         meanlist.append(mean)
            # threesigma = algorithm.pauta(meanlist)

    # def zero_exec(self):
    #     QtWidgets.QMessageBox.warning(self, "Warning:", "无数据！")
    #     self.pushButton_alert.setEnabled(True)

    def factory_label(self, factory):
        self.label_factory.setText("厂家：%s" % factory)

    def alert_exec(self, alertData1, alertData2):
        try:
            self.alertData1 = alertData1
            self.alertData2 = alertData2
            self.label_batch.setText("批次：%s" % self.ComboBox_batch.currentText())
            self.label_StartDate_alert.setText("起始日期：%s" % str(self.DateTimeEdit_alert_start.text())[:13])
            self.label_EndDate_alert.setText("结束日期：%s" % str(self.DateTimeEdit_alert_end.text())[:13])
            self.tableWidget_alert.setColumnCount(40)  # 设置表格的列数
            self.tableWidget_alert.setRowCount(60)  # 设置表格的行数
            for i in range(40):
                if i < 20:
                    self.tableWidget_alert.setHorizontalHeaderItem(i, QtWidgets.QTableWidgetItem(
                        "%s" % (i+1)))
                else:
                    self.tableWidget_alert.setHorizontalHeaderItem(i, QtWidgets.QTableWidgetItem(
                        "%s" % (i-19)))
            for i in range(20):
                for j in range(60):
                    # TODO 预警设置，数据量200，合格率99%
                    num = float(self.alertData1[i][j][0])
                    FPY = float(self.alertData1[i][j][1])
                    item0 = QtWidgets.QTableWidgetItem("%s-%s" % (i+1, j+1))

                    # item0 = QtGui.QTableWidgetItem("%s" % data[i][j].decode('gbk'))
                    item0.setTextAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
                    # -------禁止修改已写入的数据！！！-------
                    item0.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                    self.tableWidget_alert.setItem(j, i, item0)
                    if num <= 0:
                        self.tableWidget_alert.item(j, i).setBackground(QtGui.QBrush(QColor(191, 191, 191)))
                    elif num > 0 and FPY < 0.95:
                        self.tableWidget_alert.item(j, i).setBackground(QtGui.QBrush(QColor(255, 0, 0)))
                        self.tableWidget_alert.item(j, i).setForeground(QtGui.QBrush(QColor(255, 255, 255)))
                    elif num > 0 and FPY >= 0.95 and FPY < 0.96:
                        self.tableWidget_alert.item(j, i).setBackground(QtGui.QBrush(QColor(255, 63, 0)))
                        self.tableWidget_alert.item(j, i).setForeground(QtGui.QBrush(QColor(255, 255, 255)))
                    elif num > 0 and FPY >= 0.96 and FPY < 0.97:
                        self.tableWidget_alert.item(j, i).setBackground(QtGui.QBrush(QColor(255, 127, 0)))
                        self.tableWidget_alert.item(j, i).setForeground(QtGui.QBrush(QColor(255, 255, 255)))
                    elif num > 0 and FPY >= 0.97 and FPY < 0.98:
                        self.tableWidget_alert.item(j, i).setBackground(QtGui.QBrush(QColor(255, 191, 0)))
                        # self.tableWidget_alert.item(j, i).setForeground(QtGui.QBrush(QColor(255, 255, 255)))
                    elif num > 0 and FPY >= 0.98 and FPY < 0.99:
                        self.tableWidget_alert.item(j, i).setBackground(QtGui.QBrush(QColor(255, 255, 0)))
            for i in range(20):
                for j in range(60):
                    # TODO 预警设置，数据量200，合格率99%
                    num = float(self.alertData2[i][j][0])
                    FPY = float(self.alertData2[i][j][1])
                    item0 = QtWidgets.QTableWidgetItem("%s-%s" % (i+1, j+1))

                    # item0 = QtGui.QTableWidgetItem("%s" % data[i][j].decode('gbk'))
                    item0.setTextAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
                    # -------禁止修改已写入的数据！！！-------
                    item0.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                    self.tableWidget_alert.setItem(j, i+20, item0)
                    if num <= 0:
                        self.tableWidget_alert.item(j, i+20).setBackground(QtGui.QBrush(QColor(191, 191, 191)))
                    elif num > 0 and FPY < 0.99:
                        self.tableWidget_alert.item(j, i+20).setBackground(QtGui.QBrush(QColor(255, 0, 0)))
                        self.tableWidget_alert.item(j, i+20).setForeground(QtGui.QBrush(QColor(255, 255, 255)))
            self.tableWidget_alert.resizeColumnsToContents()
            # self.tableWidget_alert.itemClicked(QTableWidgetItem=self.tableWidget_alert.currentItem()).connect(self.alert_clicked)
        except:
            traceback.print_exc()
        self.pushButton_alert.setEnabled(True)

    def alert_clicked(self, item=None):
        try:
            if item == None:
                return
            for currentQTableWidgetItem in self.tableWidget_alert.selectedItems():
                j = currentQTableWidgetItem.column()
                i = currentQTableWidgetItem.row()
                if j < 20:
                    num = int(self.alertData1[j][i][0])
                    FPY = float(self.alertData1[j][i][1])*100
                    mean = float(self.alertData1[j][i][2])
                    var = float(self.alertData1[j][i][3])
                    skew = float(self.alertData1[j][i][4])
                    kurtosis = float(self.alertData1[j][i][5])
                    self.label_stationID.setText("检定单元：%s(1)" % int(j + 1))
                else:
                    num = int(self.alertData2[j-20][i][0])
                    FPY = float(self.alertData2[j-20][i][1]) * 100
                    mean = float(self.alertData2[j-20][i][2])
                    var = float(self.alertData2[j-20][i][3])
                    skew = float(self.alertData2[j-20][i][4])
                    kurtosis = float(self.alertData2[j-20][i][5])
                    self.label_stationID.setText("检定单元：%s(2)" % int(j - 19))
                self.label_meterID.setText("检定表位：%s" % int(i+1))
                self.label_num.setText("数据量：%s" % num)
                self.label_FPY.setText("合格率：%.2f%%" % FPY)
                self.label_mean.setText("期望：%.3f" % mean)
                self.label_var.setText("方差：%.3f" % var)
                self.label_skew.setText("偏度：%.3f" % skew)
                self.label_kurtosis.setText("峰度：%.3f" % kurtosis)
                # print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())
        except:
            traceback.print_exc()

    @pyqtSlot()
    def on_pushButton_subalert_clicked(self):
        self.pushButton_subalert.setDisabled(True)
        if self.database_info == [] or self.database_info_old == []:
            QtWidgets.QMessageBox.warning(self, "Warning:", "请先进行数据库配置！")
            self.pushButton_subalert.setEnabled(True)
            return
        currentPath = os.getcwd()
        ini_path = currentPath + "\manu_config.ini"
        ini_exist = os.path.exists(ini_path)
        # ---if database_config is not exist created it-------
        config = configparser.ConfigParser()
        if ini_exist == 0:
                QtWidgets.QMessageBox.warning(self, "Warning:", "配置文件丢失，请重启软件！")
                return
        else:
            # -----改写exiest的数值
            try:
                config.read(r"%s" % ini_path)

                config.set("分项预警图", "起始时间", self.DateTimeEdit_subalert_start.text())
                config.set("分项预警图", "结束时间", self.DateTimeEdit_subalert_end.text())
                config.write(open(r"%s" % ini_path, "r+"))
            except:
                traceback.print_exc()

        try:

            db_op = oral_operate.oracledb(self.database_info[0], self.database_info[1], self.database_info[2])
            db_op_old = oral_operate.oracledb_old(self.database_info_old[0], self.database_info_old[1],
                                                  self.database_info_old[2])
            flag = db_op.checkconnect()
            flag_old = db_op_old.checkconnect()
            if flag and flag_old:
                self.subalertThread = threads.subalertThread()
                self.subalertThread.setValue(self.database_info, self.database_info_old,
                                             self.DateTimeEdit_subalert_start.text(),self.DateTimeEdit_subalert_end.text(),
                                             self.ComboBox_itemname.currentText(),
                                             self.ComboBox_factory_sub.currentText(), self.ComboBox_batch_sub.currentText())
                # self.subalertThread.signal_zerodata.connect(self.subzero_exec)
                self.subalertThread.signal_alertdata.connect(self.subalert_exec)
                self.subalertThread.signal_factory.connect(self.subfactory_label)
                self.subalertThread.start()
        except:
            traceback.print_exc()
            self.pushButton_subalert.setEnabled(True)


    def subfactory_label(self, factory):
        self.label_factory_sub.setText("厂家：%s" % factory)

    def subalert_exec(self, alertData1, alertData2):
        # TODO
        try:
            self.subalertData1 = alertData1
            self.subalertData2 = alertData2
            self.label_batch_sub.setText("批次：%s" % self.ComboBox_batch_sub.currentText())
            self.label_itemname.setText("项目：%s" % self.ComboBox_itemname.currentText())
            self.label_StartDate_subalert.setText("起始日期：%s" % str(self.DateTimeEdit_subalert_start.text())[:13])
            self.label_EndDate_subalert.setText("结束日期：%s" % str(self.DateTimeEdit_subalert_end.text())[:13])
            self.tableWidget_subalert.setColumnCount(40)  # 设置表格的列数
            self.tableWidget_subalert.setRowCount(60)  # 设置表格的行数
            for i in range(40):
                if i < 20:
                    self.tableWidget_subalert.setHorizontalHeaderItem(i, QtWidgets.QTableWidgetItem(
                        "%s" % (i+1)))
                else:
                    self.tableWidget_subalert.setHorizontalHeaderItem(i, QtWidgets.QTableWidgetItem(
                        "%s" % (i-19)))
            for i in range(20):
                for j in range(60):
                    # TODO 预警设置，数据量200，合格率99%
                    num = float(self.subalertData1[i][j][0])
                    FPY = float(self.subalertData1[i][j][1])
                    item0 = QtWidgets.QTableWidgetItem("%s-%s" % (i+1, j+1))

                    # item0 = QtGui.QTableWidgetItem("%s" % data[i][j].decode('gbk'))
                    item0.setTextAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
                    # -------禁止修改已写入的数据！！！-------
                    item0.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                    self.tableWidget_subalert.setItem(j, i, item0)
                    if num <= 0:
                        self.tableWidget_subalert.item(j, i).setBackground(QtGui.QBrush(QColor(191, 191, 191)))
                    elif num > 0 and FPY < 0.95:
                        self.tableWidget_subalert.item(j, i).setBackground(QtGui.QBrush(QColor(255, 0, 0)))
                        self.tableWidget_subalert.item(j, i).setForeground(QtGui.QBrush(QColor(255, 255, 255)))
                    elif num > 0 and FPY >= 0.95 and FPY < 0.96:
                        self.tableWidget_subalert.item(j, i).setBackground(QtGui.QBrush(QColor(255, 63, 0)))
                        self.tableWidget_subalert.item(j, i).setForeground(QtGui.QBrush(QColor(255, 255, 255)))
                    elif num > 0 and FPY >= 0.96 and FPY < 0.97:
                        self.tableWidget_subalert.item(j, i).setBackground(QtGui.QBrush(QColor(255, 127, 0)))
                        self.tableWidget_subalert.item(j, i).setForeground(QtGui.QBrush(QColor(255, 255, 255)))
                    elif num > 0 and FPY >= 0.97 and FPY < 0.98:
                        self.tableWidget_subalert.item(j, i).setBackground(QtGui.QBrush(QColor(255, 191, 0)))
                        # self.tableWidget_subalert.item(j, i).setForeground(QtGui.QBrush(QColor(255, 255, 255)))
                    elif num > 0 and FPY >= 0.98 and FPY < 0.99:
                        self.tableWidget_subalert.item(j, i).setBackground(QtGui.QBrush(QColor(255, 255, 0)))
            for i in range(20):
                for j in range(60):
                    # TODO 预警设置，数据量200，合格率99%
                    num = float(self.subalertData2[i][j][0])
                    FPY = float(self.subalertData2[i][j][1])
                    item0 = QtWidgets.QTableWidgetItem("%s-%s" % (i+1, j+1))

                    # item0 = QtGui.QTableWidgetItem("%s" % data[i][j].decode('gbk'))
                    item0.setTextAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
                    # -------禁止修改已写入的数据！！！-------
                    item0.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                    self.tableWidget_subalert.setItem(j, i+20, item0)
                    if num <= 0:
                        self.tableWidget_subalert.item(j, i+20).setBackground(QtGui.QBrush(QColor(191, 191, 191)))
                    elif num > 0 and FPY < 0.95:
                        self.tableWidget_subalert.item(j, i+20).setBackground(QtGui.QBrush(QColor(255, 0, 0)))
                        self.tableWidget_subalert.item(j, i+20).setForeground(QtGui.QBrush(QColor(255, 255, 255)))
                    elif num > 0 and FPY >= 0.95 and FPY < 0.96:
                        self.tableWidget_subalert.item(j, i+20).setBackground(QtGui.QBrush(QColor(255, 63, 0)))
                        self.tableWidget_subalert.item(j, i+20).setForeground(QtGui.QBrush(QColor(255, 255, 255)))
                    elif num > 0 and FPY >= 0.96 and FPY < 0.97:
                        self.tableWidget_subalert.item(j, i+20).setBackground(QtGui.QBrush(QColor(255, 127, 0)))
                        self.tableWidget_subalert.item(j, i+20).setForeground(QtGui.QBrush(QColor(255, 255, 255)))
                    elif num > 0 and FPY >= 0.97 and FPY < 0.98:
                        self.tableWidget_subalert.item(j, i+20).setBackground(QtGui.QBrush(QColor(255, 191, 0)))
                        # self.tableWidget_subalert.item(j, i+20).setForeground(QtGui.QBrush(QColor(255, 255, 255)))
                    elif num > 0 and FPY >= 0.98 and FPY < 0.99:
                        self.tableWidget_subalert.item(j, i+20).setBackground(QtGui.QBrush(QColor(255, 255, 0)))
            self.tableWidget_subalert.resizeColumnsToContents()
            # self.tableWidget_alert.itemClicked(QTableWidgetItem=self.tableWidget_alert.currentItem()).connect(self.alert_clicked)
        except:
            traceback.print_exc()
        self.pushButton_subalert.setEnabled(True)

    def subalert_clicked(self, item=None):
        try:
            if item == None:
                return
            for currentQTableWidgetItem in self.tableWidget_subalert.selectedItems():
                j = currentQTableWidgetItem.column()
                i = currentQTableWidgetItem.row()
                if j < 20:
                    num = int(self.subalertData1[j][i][0])
                    FPY = float(self.subalertData1[j][i][1]) * 100
                    mean = float(self.subalertData1[j][i][2])
                    var = float(self.subalertData1[j][i][3])
                    skew = float(self.subalertData1[j][i][4])
                    kurtosis = float(self.subalertData1[j][i][5])
                    self.label_stationID_sub.setText("检定单元：%s(1)" % int(j + 1))
                else:
                    num = int(self.subalertData2[j-20][i][0])
                    FPY = float(self.subalertData2[j-20][i][1]) * 100
                    mean = float(self.subalertData2[j-20][i][2])
                    var = float(self.subalertData2[j-20][i][3])
                    skew = float(self.subalertData2[j-20][i][4])
                    kurtosis = float(self.subalertData2[j-20][i][5])
                    self.label_stationID_sub.setText("检定单元：%s(2)" % int(j - 19))
                self.label_meterID_sub.setText("检定表位：%s" % int(i + 1))
                self.label_num_sub.setText("数据量：%s" % num)
                self.label_FPY_sub.setText("合格率：%.2f%%" % FPY)
                self.label_mean_sub.setText("期望：%.3f" % mean)
                self.label_var_sub.setText("方差：%.3f" % var)
                self.label_skew_sub.setText("偏度：%.3f" % skew)
                self.label_kurtosis_sub.setText("峰度：%.3f" % kurtosis)
                # print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())
        except:
            traceback.print_exc()

    @pyqtSlot()
    def on_pushButton_terror_clicked(self):
        self.pushButton_terror.setDisabled(True)
        if self.database_info == [] or self.database_info_old == []:
            QtWidgets.QMessageBox.warning(self, "Warning:", "请先进行数据库配置！")
            self.pushButton_terror.setEnabled(True)
            return
        currentPath = os.getcwd()
        ini_path = currentPath + "\manu_config.ini"
        ini_exist = os.path.exists(ini_path)
        # ---if database_config is not exist created it-------
        config = configparser.ConfigParser()
        if ini_exist == 0:
            QtWidgets.QMessageBox.warning(self, "Warning:", "配置文件丢失，请重启软件！")
            return
        else:
            # -----改写exiest的数值
            config.read(r"%s" % ini_path)
            config.set("日计时误差预警图", "起始时间", self.DateTimeEdit_terror_start.text())
            config.set("日计时误差预警图", "结束时间", self.DateTimeEdit_terror_end.text())
            config.write(open(r"%s" % ini_path, "r+"))

        try:

            db_op = oral_operate.oracledb(self.database_info[0], self.database_info[1], self.database_info[2])
            db_op_old = oral_operate.oracledb_old(self.database_info_old[0], self.database_info_old[1],
                                                  self.database_info_old[2])
            flag = db_op.checkconnect()
            flag_old = db_op_old.checkconnect()
            if flag and flag_old:
                self.terrorThread = threads.terrorThread()
                self.terrorThread.setValue(self.database_info, self.database_info_old, self.DateTimeEdit_terror_start.text(), self.DateTimeEdit_terror_end.text())
                # self.terrorThread.signal_zerodata.connect(self.terrorzero_exec)
                self.terrorThread.signal_alertdata.connect(self.terror_exec)
                self.terrorThread.start()
        except:
            traceback.print_exc()
            self.pushButton_terror.setEnabled(True)
            # ---------set datas----------
            # meanlist = []
            # for i in range(60):
            #     for j in range(20):
            #         mean = float(self.alertData[i][j][0])
            #         meanlist.append(mean)
            # threesigma = algorithm.pauta(meanlist)



    def terror_exec(self, alertMData1, alertSData1, alertMData2, alertSData2):
        try:
            self.terrorMData1 = alertMData1
            self.terrorSData1 = alertSData1
            self.terrorMData2 = alertMData2
            self.terrorSData2 = alertSData2
            self.label_StartDate_terror.setText("起始日期：%s" % str(self.DateTimeEdit_terror_start.text())[:13])
            self.label_EndDate_terror.setText("结束日期：%s" % str(self.DateTimeEdit_terror_end.text())[:13])
            self.tableWidget_terror.setColumnCount(40)  # 设置表格的列数
            self.tableWidget_terror.setRowCount(60)  # 设置表格的行数

            for i in range(20):
                mlist = []
                for j in range(60):
                    # TODO 预警设置,3σ准则
                    mean = float(self.terrorMData1[i][j][1])
                    mlist.append(mean)
                threesigma = algorithm.pauta(mlist)
                for j in range(60):

                    item0 = QtWidgets.QTableWidgetItem("%.4f" % self.terrorMData1[i][j][1])

                    # item0 = QtGui.QTableWidgetItem("%s" % data[i][j].decode('gbk'))
                    item0.setTextAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
                    # -------禁止修改已写入的数据！！！-------
                    item0.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                    self.tableWidget_terror.setItem(j, i, item0)
                    # if num < 200:
                    #     self.tableWidget_alert.item(j, i).setBackground(QtGui.QBrush(QColor(255, 255, 0)))
                    # elif num >= 200 and FPY < 0.99:
                    #     self.tableWidget_alert.item(j, i).setBackground(QtGui.QBrush(QColor(255, 0, 0)))

                    if float(self.terrorMData1[i][j][1]) <= threesigma[0] or float(self.terrorMData1[i][j][1]) >= threesigma[1]:
                        self.tableWidget_terror.item(j, i).setBackground(QtGui.QBrush(QColor(255, 255, 0)))

            for i in range(20):
                mlist = []
                for j in range(60):
                    # TODO 预警设置,3σ准则
                    mean = float(self.terrorMData2[i][j][1])
                    mlist.append(mean)
                threesigma = algorithm.pauta(mlist)
                for j in range(60):

                    item0 = QtWidgets.QTableWidgetItem("%.4f" % self.terrorMData2[i][j][1])

                    # item0 = QtGui.QTableWidgetItem("%s" % data[i][j].decode('gbk'))
                    item0.setTextAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
                    # -------禁止修改已写入的数据！！！-------
                    item0.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                    self.tableWidget_terror.setItem(j, i+20, item0)
                    # if num < 200:
                    #     self.tableWidget_alert.item(j, i).setBackground(QtGui.QBrush(QColor(255, 255, 0)))
                    # elif num >= 200 and FPY < 0.99:
                    #     self.tableWidget_alert.item(j, i).setBackground(QtGui.QBrush(QColor(255, 0, 0)))

                    if float(self.terrorMData2[i][j][1]) <= threesigma[0] or float(self.terrorMData2[i][j][1]) >= \
                            threesigma[1]:
                        self.tableWidget_terror.item(j, i+20).setBackground(QtGui.QBrush(QColor(255, 255, 0)))
            self.tableWidget_terror.resizeColumnsToContents()

            slist = []
            for i in range(20):
                mean = self.terrorSData1[i][1]
                slist.append(mean)
            for i in range(20):
                self.tableWidget_terror.setHorizontalHeaderItem(i, QtWidgets.QTableWidgetItem(
                    "%s" % (i+1)))
                threesigma = algorithm.pauta(slist[:i] + slist[i+1:])
                if float(self.terrorSData1[i][1]) <= threesigma[0] or float(self.terrorSData1[i][1]) >= threesigma[1]:
                    headItem = self.tableWidget_terror.horizontalHeaderItem(i)
                    headItem.setForeground(QColor(255, 0, 0))
                    for j in range(60):
                        self.tableWidget_terror.item(j, i).setBackground(QtGui.QBrush(QColor(255, 0, 0)))
                        self.tableWidget_terror.item(j, i).setForeground(QtGui.QBrush(QColor(255, 255, 255)))
                    # self.tableWidget_terror.horizontalHeaderItem(i).setBackground(QtGui.QBrush(QColor(255, 0, 0)))

            slist = []
            for i in range(20):
                mean = self.terrorSData2[i][1]
                slist.append(mean)
            for i in range(20):
                self.tableWidget_terror.setHorizontalHeaderItem(i + 20, QtWidgets.QTableWidgetItem(
                    "%s" % (i + 1)))
                threesigma = algorithm.pauta(slist[:i] + slist[i + 1:])
                if float(self.terrorSData2[i][1]) <= threesigma[0] or float(self.terrorSData2[i][1]) >= threesigma[1]:
                    headItem = self.tableWidget_terror.horizontalHeaderItem(i+20)
                    headItem.setForeground(QColor(255, 0, 0))
                    for j in range(60):
                        self.tableWidget_terror.item(j, i+20).setBackground(QtGui.QBrush(QColor(255, 0, 0)))
                        self.tableWidget_terror.item(j, i+20).setForeground(QtGui.QBrush(QColor(255, 255, 255)))

            # self.tableWidget_alert.itemClicked(QTableWidgetItem=self.tableWidget_alert.currentItem()).connect(self.alert_clicked)
        except:
            traceback.print_exc()
        self.pushButton_terror.setEnabled(True)

    def terror_clicked(self, item=None):
        try:
            if item == None:
                return
            for currentQTableWidgetItem in self.tableWidget_terror.selectedItems():
                i = currentQTableWidgetItem.column()
                j = currentQTableWidgetItem.row()
                if i < 20:
                    num = int(self.terrorSData1[i][0])
                    # FPY = float(self.alertData[j][i][1])*100
                    mean = float(self.terrorSData1[i][1])
                # var = float(self.alertData[j][i][3])
                # skew = float(self.alertData[j][i][4])
                # kurtosis = float(self.alertData[j][i][5])
                    self.label_stationID_terror.setText("检定单元：%s(1)" % int(i+1))
                else:
                    num = int(self.terrorSData2[i-20][0])
                    # FPY = float(self.alertData[j][i][1])*100
                    mean = float(self.terrorSData2[i-20][1])
                    # var = float(self.alertData[j][i][3])
                    # skew = float(self.alertData[j][i][4])
                    # kurtosis = float(self.alertData[j][i][5])
                    self.label_stationID_terror.setText("检定单元：%s(2)" % int(i -19))
                # self.label_meterID.setText("检定表位：%s" % int(j+1))
                self.label_num_terror.setText("数据量：%s" % num)
                # self.label_FPY.setText("合格率：%.2f%%" % FPY)
                self.label_mean_terror.setText("期望：%.3f" % mean)
                # self.label_var.setText("方差：%.3f" % var)
                # self.label_skew.setText("偏度：%.3f" % skew)
                # self.label_kurtosis.setText("峰度：%.3f" % kurtosis)
                # print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())
        except:
            traceback.print_exc()

    def closeEvent(self, event):
        """
        重写closeEvent方法，实现dialog窗体关闭时执行一些代码
        :param event: close()触发的事件
        :return: None
        """
        reply = QtWidgets.QMessageBox.question(self,
                                               "本程序",
                                               "是否要退出程序？",
                                               QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.Cancel,
                                               QtWidgets.QMessageBox.Yes)
        if reply == QtWidgets.QMessageBox.Yes:
            self.database_set.close()
            event.accept()
        else:
            event.ignore()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.setrecursionlimit(1000000)
    sys.exit(app.exec_())

#
# def mycodestart():
#     app = QtWidgets.QApplication(sys.argv)
#     ui = MainWindow()
#     ui.show()
#     sys.exit(app.exec_())
#
# if __name__ == '__main__':
#     import sys, threading
#     sys.setrecursionlimit(100000)
#     threading.stack_size(200000000)
#     thread = threading.Thread(target=mycodestart)
#     thread.start()
