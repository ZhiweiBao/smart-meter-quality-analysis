from PyQt5 import QtCore
from db_Oracle import oral_operate
from typechange import typechange
from algorithm import algorithm
import traceback


class factoryThread(QtCore.QThread):
    signal_factorydata = QtCore.pyqtSignal(list)

    def __int__(self, parent=None):
        super(factoryThread, self).__init__(parent)

    def setValue(self, database_info, database_info_old):
        self.database_info = database_info
        self.database_info_old = database_info_old

    def run(self):
        try:
            db_op = oral_operate.oracledb(self.database_info[0], self.database_info[1], self.database_info[2])
            db_op_old = oral_operate.oracledb_old(self.database_info_old[0], self.database_info_old[1],
                                                  self.database_info_old[2])
            facList1 = db_op.getFactoryList()
            facList2 = db_op_old.getFactoryList()
            factoryList = list(set(facList1 + facList2))
            self.signal_factorydata.emit(factoryList)
        except:
            traceback.print_exc()

class batchThread(QtCore.QThread):
    signal_batchdata = QtCore.pyqtSignal(list)


    def __int__(self, parent=None):
        super(batchThread, self).__init__(parent)

    def setValue(self, database_info, database_info_old, factory):
        self.database_info = database_info
        self.database_info_old = database_info_old
        self.factory = factory
        # print(database_info)

    def run(self):
        try:
            db_op = oral_operate.oracledb(self.database_info[0], self.database_info[1], self.database_info[2])
            db_op_old = oral_operate.oracledb_old(self.database_info_old[0], self.database_info_old[1],
                                                  self.database_info_old[2])
            baList1 = db_op.getBatchList(self.factory)
            baList2 = db_op_old.getBatchList(self.factory)
            batchList = list(set(baList1 + baList2))
            self.signal_batchdata.emit(batchList)
        except:
            traceback.print_exc()

class batchsubThread(QtCore.QThread):
    signal_batchsubdata = QtCore.pyqtSignal(list)


    def __int__(self, parent=None):
        super(batchsubThread, self).__init__(parent)

    def setValue(self, database_info, database_info_old, factory):
        self.database_info = database_info
        self.database_info_old = database_info_old
        self.factory = factory
        # print(database_info)

    def run(self):
        try:
            db_op = oral_operate.oracledb(self.database_info[0], self.database_info[1], self.database_info[2])
            db_op_old = oral_operate.oracledb_old(self.database_info_old[0], self.database_info_old[1],
                                                  self.database_info_old[2])
            baList1 = db_op.getBatchList(self.factory)
            baList2 = db_op_old.getBatchList(self.factory)
            batchList = list(set(baList1 + baList2))
            self.signal_batchsubdata.emit(batchList)
        except:
            traceback.print_exc()

class alertThread(QtCore.QThread):
    signal_alertdata = QtCore.pyqtSignal(list, list)
    signal_zerodata = QtCore.pyqtSignal()
    signal_factory = QtCore.pyqtSignal(str)

    def __int__(self, parent=None):
        super(alertThread, self).__init__(parent)

    def setValue(self, database_info, database_info_old, startTime, endTime, factory, batch):
        self.database_info = database_info
        self.database_info_old = database_info_old
        self.startTime = startTime
        self.endTime = endTime
        self.factory = factory
        self.batch = batch
        # print(database_info)

    def run(self):
        try:
            db_op = oral_operate.oracledb(self.database_info[0], self.database_info[1], self.database_info[2])
            db_op_old = oral_operate.oracledb_old(self.database_info_old[0], self.database_info_old[1], self.database_info_old[2])
            if self.factory == '全部厂家':
                data1 = typechange.type_change_alert(
                    db_op.getAlertData(self.startTime, self.endTime))
                data2 = typechange.type_change_alert(
                    db_op_old.getAlertData(self.startTime, self.endTime))
                # if data == []:
                #     self.signal_zerodata.emit()
                #     return
                alertData1 = algorithm.alert_analyze(algorithm.classifyResource(data1))
                alertData2 = algorithm.alert_analyze(algorithm.classifyResource(data2))
                self.signal_alertdata.emit(alertData1, alertData2)
                self.signal_factory.emit(self.factory)
            elif self.batch == '全部批次':
                data1 = typechange.type_change_alert(
                    db_op.getAlertFacData(self.startTime, self.endTime, self.factory))
                data2 = typechange.type_change_alert(
                    db_op_old.getAlertFacData(self.startTime, self.endTime, self.factory))
                # if data == []:
                #     self.signal_zerodata.emit()
                #     return
                alertData1 = algorithm.alert_analyze(algorithm.classifyResource(data1))
                alertData2 = algorithm.alert_analyze(algorithm.classifyResource(data2))
                self.signal_alertdata.emit(alertData1, alertData2)
                self.signal_factory.emit(self.factory)
            else:
                data1 = typechange.type_change_alert(
                    db_op.getAlertBatchData(self.startTime, self.endTime, self.batch))
                data2 = typechange.type_change_alert(
                    db_op_old.getAlertBatchData(self.startTime, self.endTime, self.batch))
                # if data == []:
                #     self.signal_zerodata.emit()
                #     return
                alertData1 = algorithm.alert_analyze(algorithm.classifyResource(data1))
                alertData2 = algorithm.alert_analyze(algorithm.classifyResource(data2))
                self.signal_alertdata.emit(alertData1, alertData2)
                factory = db_op.batchToFactory(self.batch)
                if factory == '':
                    factory = db_op_old.batchToFactory(self.batch)
                self.signal_factory.emit(factory)
        except Exception as e:
            print(e)

class subalertThread(QtCore.QThread):
    signal_alertdata = QtCore.pyqtSignal(list, list)
    signal_zerodata = QtCore.pyqtSignal()
    signal_factory = QtCore.pyqtSignal(str)

    def __int__(self, parent=None):
        super(subalertThread, self).__init__(parent)

    def setValue(self, database_info, database_info_old, startTime, endTime, itemname, factory, batch):
        self.database_info = database_info
        self.database_info_old = database_info_old
        self.startTime = startTime
        self.endTime = endTime
        self.itemname = itemname
        self.factory = factory
        self.batch = batch

    def run(self):
        try:
            db_op = oral_operate.oracledb(self.database_info[0], self.database_info[1], self.database_info[2])
            db_op_old = oral_operate.oracledb_old(self.database_info_old[0], self.database_info_old[1],
                                                  self.database_info_old[2])
            if self.factory == '全部厂家':
                data1 = typechange.type_change_alert(
                    db_op.getSubAlertData(self.itemname, self.startTime, self.endTime))
                data2 = typechange.type_change_alert(
                    db_op_old.getSubAlertData(self.itemname, self.startTime, self.endTime))
                # if data1 == []:
                #     self.signal_zerodata.emit()
                #     return
                alertData1 = algorithm.alert_analyze(algorithm.classifyResource(data1))
                alertData2 = algorithm.alert_analyze(algorithm.classifyResource(data2))
                self.signal_alertdata.emit(alertData1, alertData2)
                self.signal_factory.emit(self.factory)
            elif self.batch == '全部批次':
                data1 = typechange.type_change_alert(
                    db_op.getSubAlertFacData(self.itemname, self.startTime, self.endTime, self.factory))
                data2 = typechange.type_change_alert(
                    db_op_old.getSubAlertFacData(self.itemname, self.startTime, self.endTime, self.factory))
                # if data1 == []:
                #     self.signal_zerodata.emit()
                #     return
                alertData1 = algorithm.alert_analyze(algorithm.classifyResource(data1))
                alertData2 = algorithm.alert_analyze(algorithm.classifyResource(data2))
                self.signal_alertdata.emit(alertData1, alertData2)
                self.signal_factory.emit(self.factory)
            else:
                data1 = typechange.type_change_alert(
                    db_op.getSubAlertBatchData(self.itemname, self.startTime, self.endTime, self.batch))
                data2 = typechange.type_change_alert(
                    db_op_old.getSubAlertBatchData(self.itemname, self.startTime, self.endTime, self.batch))
                # if data1 == []:
                #     self.signal_zerodata.emit()
                #     return
                alertData1 = algorithm.alert_analyze(algorithm.classifyResource(data1))
                alertData2 = algorithm.alert_analyze(algorithm.classifyResource(data2))
                self.signal_alertdata.emit(alertData1, alertData2)
                factory = db_op.batchToFactory(self.batch)
                if factory == '':
                    factory = db_op_old.batchToFactory(self.batch)
                self.signal_factory.emit(factory)
        except Exception as e:
            print(e)

class terrorThread(QtCore.QThread):
    signal_alertdata = QtCore.pyqtSignal(list, list, list, list)
    signal_zerodata = QtCore.pyqtSignal()

    def __int__(self, parent=None):
        super(terrorThread, self).__init__(parent)

    def setValue(self, database_info, database_info_old, startTime, endTime):
        self.database_info = database_info
        self.database_info_old = database_info_old
        self.startTime = startTime
        self.endTime = endTime
        # self.itemname = itemname
        # print(database_info)

    def run(self):
        try:
            db_op = oral_operate.oracledb(self.database_info[0], self.database_info[1], self.database_info[2])
            db_op_old = oral_operate.oracledb_old(self.database_info_old[0], self.database_info_old[1],
                                                  self.database_info_old[2])
            data1 = typechange.type_change_alert(
                db_op.getTErrorData(self.startTime, self.endTime))
            data2 = typechange.type_change_alert(
                db_op_old.getTErrorData(self.startTime, self.endTime))
            # if data == []:
            #     self.signal_zerodata.emit()
            #     return

            alertData1, alertSData1 = algorithm.terror_analyze(algorithm.classifyResource(data1))
            alertData2, alertSData2 = algorithm.terror_analyze(algorithm.classifyResource(data2))
            self.signal_alertdata.emit(alertData1, alertSData1, alertData2, alertSData2)
        except Exception as e:
            print(e)