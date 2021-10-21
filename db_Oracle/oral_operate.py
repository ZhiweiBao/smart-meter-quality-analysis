# -*- coding: utf-8 -*-

import cx_Oracle
import traceback


class oracledb(object):
    def __init__(self, host='', user='',password=''):
        self.host = host
        self.user = user
        self.password = password

    def checkconnect(self):
        try:
            cnxn = cx_Oracle.connect(self.user, self.password, self.host)
            cur = cnxn.cursor()
            cur.close()
            cnxn.close()
            return True
        except:
            traceback.print_exc()
            return False

    def get_tablename(self):
        try:
            cnxn = cx_Oracle.connect(self.user, self.password, self.host)
            cur = cnxn.cursor()
            sql = "select TABLE_NAME from USER_TABLES"
            cur.execute(sql)
            rows = cur.fetchall()
            tablelist = []
            for i in range(len(rows)):
                tablelist.extend(rows[i])
            cur.close()
            cnxn.close()
            return tablelist
        except:
            traceback.print_exc()
            return []

    def getFactoryList(self):
        try:
            cnxn = cx_Oracle.connect(self.user, self.password, self.host)
            cur = cnxn.cursor()
            sql = "select distinct MANU_FACTUR from METER_INFO"
            cur.execute(sql)
            rows = cur.fetchall()
            factoryList = []
            for i in range(len(rows)):
                factoryList.extend(rows[i])
            cur.close()
            cnxn.close()
            return factoryList
        except:
            traceback.print_exc()
            return []
        
    def getBatchList(self, factory):
        try:
            cnxn = cx_Oracle.connect(self.user, self.password, self.host)
            cur = cnxn.cursor()
            sql = "select distinct BATCHID from METER_INFO where MANU_FACTUR = '%s'" % factory
            cur.execute(sql)
            rows = cur.fetchall()
            batchList = []
            for i in range(len(rows)):
                batchList.extend(rows[i])
            cur.close()
            cnxn.close()
            return batchList
        except:
            traceback.print_exc()
            return []

    def batchToFactory(self, batch):
        try:
            cnxn = cx_Oracle.connect(self.user, self.password, self.host)
            cur = cnxn.cursor()
            sql = "select distinct MANU_FACTUR from METER_INFO where BATCHID = '%s'" % batch
            cur.execute(sql)
            rows = cur.fetchall()
            factory = str(rows[0][0])
            cur.close()
            cnxn.close()
            return factory
        except:
            traceback.print_exc()
            return ''

    def getAlertData(self, startdate, enddate):
        try:
            cnxn = cx_Oracle.connect(self.user, self.password, self.host)
            cur = cnxn.cursor()
            sql = "select T.STATIONID,T.METERID,T.AVERGERROR from " \
                  "(select STATIONID,METERID,AVERGERROR,ITEMNAME,TRIALEND_DATE from TRIAL_DATA " \
                  "union all " \
                  "select STATIONID,METERID,AVERGERROR,ITEMNAME,TRIALEND_DATE from TRIAL_DATA_HIS) T " \
                  "where T.ITEMNAME like '基本误差%' " \
                  "and T.TRIALEND_DATE  " \
                  "between to_date('{0}','yyyy-mm-dd hh24:mi:ss') " \
                  "and to_date('{1}','yyyy-mm-dd hh24:mi:ss')".format(startdate, enddate)
            cur.execute(sql)
            rows = cur.fetchall()

            cur.close()
            cnxn.close()
            return rows
        except:
            traceback.print_exc()
            return []

    def getAlertFacData(self, startdate, enddate, factory):
        try:
            cnxn = cx_Oracle.connect(self.user, self.password, self.host)
            cur = cnxn.cursor()
            sql = "select T.STATIONID,T.METERID,T.AVERGERROR from " \
                  "(select STATIONID,METERID,AVERGERROR,ITEMNAME,TRIALEND_DATE,TASKID from TRIAL_DATA " \
                  "union all " \
                  "select STATIONID,METERID,AVERGERROR,ITEMNAME,TRIALEND_DATE,TASKID from TRIAL_DATA_HIS) T " \
                  "where T.ITEMNAME like '基本误差%' " \
                  "and T.TRIALEND_DATE " \
                  "between to_date('{0}','yyyy-mm-dd hh24:mi:ss') " \
                  "and to_date('{1}','yyyy-mm-dd hh24:mi:ss') " \
                  "and T.TASKID in (select distinct TASKID from METER_INFO where MANU_FACTUR = '{2}')".format(startdate, enddate, factory)
            cur.execute(sql)
            rows = cur.fetchall()

            cur.close()
            cnxn.close()
            return rows
        except:
            traceback.print_exc()
            return []

    def getAlertBatchData(self, startdate, enddate, batch):
        try:
            cnxn = cx_Oracle.connect(self.user, self.password, self.host)
            cur = cnxn.cursor()
            sql = "select T.STATIONID,T.METERID,T.AVERGERROR from " \
                  "(select STATIONID,METERID,AVERGERROR,ITEMNAME,TRIALEND_DATE,TASKID from TRIAL_DATA " \
                  "union all " \
                  "select STATIONID,METERID,AVERGERROR,ITEMNAME,TRIALEND_DATE,TASKID from TRIAL_DATA_HIS) T " \
                  "where T.ITEMNAME like '基本误差%' " \
                  "and T.TRIALEND_DATE " \
                  "between to_date('{0}','yyyy-mm-dd hh24:mi:ss') " \
                  "and to_date('{1}','yyyy-mm-dd hh24:mi:ss') " \
                  "and T.TASKID = '{2}'".format(startdate, enddate, batch)
            cur.execute(sql)
            rows = cur.fetchall()

            cur.close()
            cnxn.close()
            return rows
        except:
            traceback.print_exc()
            return []

    def getSubAlertData(self, itemname, startdate, enddate):
        try:
            cnxn = cx_Oracle.connect(self.user, self.password, self.host)
            cur = cnxn.cursor()
            sql = "select T.STATIONID,T.METERID,T.AVERGERROR from " \
                  "(select STATIONID,METERID,AVERGERROR,ITEMNAME,TRIALEND_DATE from TRIAL_DATA " \
                  "union all " \
                  "select STATIONID,METERID,AVERGERROR,ITEMNAME,TRIALEND_DATE from TRIAL_DATA_HIS) T " \
                  "where T.ITEMNAME = '基本误差{0}' " \
                  "and T.TRIALEND_DATE " \
                  "between to_date('{1}','yyyy-mm-dd hh24:mi:ss') " \
                  "and to_date('{2}','yyyy-mm-dd hh24:mi:ss')".format(itemname, startdate, enddate)
            cur.execute(sql)
            rows = cur.fetchall()

            cur.close()
            cnxn.close()
            return rows
        except:
            traceback.print_exc()
            return []

    def getSubAlertFacData(self, itemname, startdate, enddate, factory):
        try:
            cnxn = cx_Oracle.connect(self.user, self.password, self.host)
            cur = cnxn.cursor()
            sql = "select T.STATIONID,T.METERID,T.AVERGERROR from " \
                  "(select STATIONID,METERID,AVERGERROR,ITEMNAME,TRIALEND_DATE,TASKID from TRIAL_DATA " \
                  "union all " \
                  "select STATIONID,METERID,AVERGERROR,ITEMNAME,TRIALEND_DATE,TASKID from TRIAL_DATA_HIS) T " \
                  "where T.ITEMNAME = '基本误差{0}' " \
                  "and T.TRIALEND_DATE " \
                  "between to_date('{1}','yyyy-mm-dd hh24:mi:ss') " \
                  "and to_date('{2}','yyyy-mm-dd hh24:mi:ss') " \
                  "and T.TASKID in (select distinct TASKID from METER_INFO where MANU_FACTUR = '{3}')".format(itemname, startdate, enddate, factory)
            cur.execute(sql)
            rows = cur.fetchall()

            cur.close()
            cnxn.close()
            return rows
        except:
            traceback.print_exc()
            return []

    def getSubAlertBatchData(self, itemname, startdate, enddate, batch):
        try:
            cnxn = cx_Oracle.connect(self.user, self.password, self.host)
            cur = cnxn.cursor()
            sql = "select T.STATIONID,T.METERID,T.AVERGERROR from " \
                  "(select STATIONID,METERID,AVERGERROR,ITEMNAME,TRIALEND_DATE,TASKID from TRIAL_DATA " \
                  "union all " \
                  "select STATIONID,METERID,AVERGERROR,ITEMNAME,TRIALEND_DATE,TASKID from TRIAL_DATA_HIS) T " \
                  "where T.ITEMNAME = '基本误差{0}' " \
                  "and T.TRIALEND_DATE " \
                  "between to_date('{1}','yyyy-mm-dd hh24:mi:ss') " \
                  "and to_date('{2}','yyyy-mm-dd hh24:mi:ss') " \
                  "and T.TASKID = '{3}'".format(itemname, startdate, enddate, batch)
            cur.execute(sql)
            rows = cur.fetchall()

            cur.close()
            cnxn.close()
            return rows
        except:
            traceback.print_exc()
            return []

    def getTErrorData(self, startdate, enddate):
        try:
            cnxn = cx_Oracle.connect(self.user, self.password, self.host)
            cur = cnxn.cursor()
            sql = "select T.STATIONID,T.METERID,T.AVERGERROR from " \
                  "(select STATIONID,METERID,AVERGERROR,ITEMNAME,TRIALEND_DATE from TRIAL_DATA " \
                  "union all " \
                  "select STATIONID,METERID,AVERGERROR,ITEMNAME,TRIALEND_DATE from TRIAL_DATA_HIS) T " \
                  "where T.ITEMNAME = '日计时误差' " \
                  "and T.TRIALEND_DATE " \
                  "between to_date('{0}','yyyy-mm-dd hh24:mi:ss') " \
                  "and to_date('{1}','yyyy-mm-dd hh24:mi:ss')".format(startdate, enddate)
            cur.execute(sql)
            rows = cur.fetchall()
            cur.close()
            cnxn.close()
            return rows
        except:
            traceback.print_exc()
            return []


class oracledb_old(oracledb):

    def getBatchList(self, factory):
        try:
            cnxn = cx_Oracle.connect(self.user, self.password, self.host)
            cur = cnxn.cursor()
            sql = "select distinct BATCH_ID from METER_INFO where MANU_FACTUR = '%s'" % factory
            cur.execute(sql)
            rows = cur.fetchall()
            batchList = []
            for i in range(len(rows)):
                batchList.extend(rows[i])
            cur.close()
            cnxn.close()
            return batchList
        except:
            traceback.print_exc()
            return []

    def batchToFactory(self, batch):
        try:
            cnxn = cx_Oracle.connect(self.user, self.password, self.host)
            cur = cnxn.cursor()
            sql = "select distinct MANU_FACTUR from METER_INFO where BATCH_ID = '%s'" % batch
            cur.execute(sql)
            rows = cur.fetchall()
            factory = str(rows[0][0])
            cur.close()
            cnxn.close()
            return factory
        except:
            traceback.print_exc()
            return ''

    def getAlertData(self, startdate, enddate):
        try:
            cnxn = cx_Oracle.connect(self.user, self.password, self.host)
            cur = cnxn.cursor()
            sql = "select T.STATIONID,T.METERID,T.AVERGERROR from " \
                  "(select STATIONID,METERID,AVERGERROR,ITEMNAME,TRIAL_DATE from TRIAL_DATA " \
                  "union all " \
                  "select STATIONID,METERID,AVERGERROR,ITEMNAME,TRIAL_DATE from TRIAL_DATA_HIS) T " \
                  "where T.ITEMNAME like '基本误差%' " \
                  "and T.TRIAL_DATE  " \
                  "between to_date('{0}','yyyy-mm-dd hh24:mi:ss') " \
                  "and to_date('{1}','yyyy-mm-dd hh24:mi:ss')".format(startdate, enddate)
            cur.execute(sql)
            rows = cur.fetchall()

            cur.close()
            cnxn.close()
            return rows
        except:
            traceback.print_exc()
            return []

    def getAlertFacData(self, startdate, enddate, factory):
        try:
            cnxn = cx_Oracle.connect(self.user, self.password, self.host)
            cur = cnxn.cursor()
            sql = "select T.STATIONID,T.METERID,T.AVERGERROR from " \
                  "(select STATIONID,METERID,AVERGERROR,ITEMNAME,TRIAL_DATE,TASKID from TRIAL_DATA " \
                  "union all " \
                  "select STATIONID,METERID,AVERGERROR,ITEMNAME,TRIAL_DATE,TASKID from TRIAL_DATA_HIS) T " \
                  "where T.ITEMNAME like '基本误差%' " \
                  "and T.TRIAL_DATE " \
                  "between to_date('{0}','yyyy-mm-dd hh24:mi:ss') " \
                  "and to_date('{1}','yyyy-mm-dd hh24:mi:ss') " \
                  "and T.TASKID in (select distinct TASKID from METER_INFO where MANU_FACTUR = '{2}')".format(startdate, enddate, factory)
            cur.execute(sql)
            rows = cur.fetchall()

            cur.close()
            cnxn.close()
            return rows
        except:
            traceback.print_exc()
            return []

    def getAlertBatchData(self, startdate, enddate, batch):
        try:
            cnxn = cx_Oracle.connect(self.user, self.password, self.host)
            cur = cnxn.cursor()
            sql = "select T.STATIONID,T.METERID,T.AVERGERROR from " \
                  "(select STATIONID,METERID,AVERGERROR,ITEMNAME,TRIAL_DATE,TASKID from TRIAL_DATA " \
                  "union all " \
                  "select STATIONID,METERID,AVERGERROR,ITEMNAME,TRIAL_DATE,TASKID from TRIAL_DATA_HIS) T " \
                  "where T.ITEMNAME like '基本误差%' " \
                  "and T.TRIAL_DATE " \
                  "between to_date('{0}','yyyy-mm-dd hh24:mi:ss') " \
                  "and to_date('{1}','yyyy-mm-dd hh24:mi:ss') " \
                  "and T.TASKID = '{2}'".format(startdate, enddate, batch)
            cur.execute(sql)
            rows = cur.fetchall()

            cur.close()
            cnxn.close()
            return rows
        except:
            traceback.print_exc()
            return []

    def getSubAlertData(self, itemname, startdate, enddate):
        try:
            cnxn = cx_Oracle.connect(self.user, self.password, self.host)
            cur = cnxn.cursor()
            sql = "select T.STATIONID,T.METERID,T.AVERGERROR from " \
                  "(select STATIONID,METERID,AVERGERROR,ITEMNAME,TRIAL_DATE from TRIAL_DATA " \
                  "union all " \
                  "select STATIONID,METERID,AVERGERROR,ITEMNAME,TRIAL_DATE from TRIAL_DATA_HIS) T " \
                  "where T.ITEMNAME = '基本误差{0}' " \
                  "and T.TRIAL_DATE " \
                  "between to_date('{1}','yyyy-mm-dd hh24:mi:ss') " \
                  "and to_date('{2}','yyyy-mm-dd hh24:mi:ss')".format(itemname, startdate, enddate)
            cur.execute(sql)
            rows = cur.fetchall()

            cur.close()
            cnxn.close()
            return rows
        except:
            traceback.print_exc()
            return []

    def getSubAlertFacData(self, itemname, startdate, enddate, factory):
        try:
            cnxn = cx_Oracle.connect(self.user, self.password, self.host)
            cur = cnxn.cursor()
            sql = "select T.STATIONID,T.METERID,T.AVERGERROR from " \
                  "(select STATIONID,METERID,AVERGERROR,ITEMNAME,TRIAL_DATE,TASKID from TRIAL_DATA " \
                  "union all " \
                  "select STATIONID,METERID,AVERGERROR,ITEMNAME,TRIAL_DATE,TASKID from TRIAL_DATA_HIS) T " \
                  "where T.ITEMNAME = '基本误差{0}' " \
                  "and T.TRIAL_DATE " \
                  "between to_date('{1}','yyyy-mm-dd hh24:mi:ss') " \
                  "and to_date('{2}','yyyy-mm-dd hh24:mi:ss') " \
                  "and T.TASKID in (select distinct TASKID from METER_INFO where MANU_FACTUR = '{3}')".format(itemname, startdate, enddate, factory)
            cur.execute(sql)
            rows = cur.fetchall()

            cur.close()
            cnxn.close()
            return rows
        except:
            traceback.print_exc()
            return []

    def getSubAlertBatchData(self, itemname, startdate, enddate, batch):
        try:
            cnxn = cx_Oracle.connect(self.user, self.password, self.host)
            cur = cnxn.cursor()
            sql = "select T.STATIONID,T.METERID,T.AVERGERROR from " \
                  "(select STATIONID,METERID,AVERGERROR,ITEMNAME,TRIAL_DATE,TASKID from TRIAL_DATA " \
                  "union all " \
                  "select STATIONID,METERID,AVERGERROR,ITEMNAME,TRIAL_DATE,TASKID from TRIAL_DATA_HIS) T " \
                  "where T.ITEMNAME = '基本误差{0}' " \
                  "and T.TRIAL_DATE " \
                  "between to_date('{1}','yyyy-mm-dd hh24:mi:ss') " \
                  "and to_date('{2}','yyyy-mm-dd hh24:mi:ss') " \
                  "and T.TASKID = '{3}'".format(itemname, startdate, enddate, batch)
            cur.execute(sql)
            rows = cur.fetchall()

            cur.close()
            cnxn.close()
            return rows
        except:
            traceback.print_exc()
            return []

    def getTErrorData(self, startdate, enddate):
        try:
            cnxn = cx_Oracle.connect(self.user, self.password, self.host)
            cur = cnxn.cursor()
            sql = "select T.STATIONID,T.METERID,T.AVERGERROR from " \
                  "(select STATIONID,METERID,AVERGERROR,ITEMNAME,TRIAL_DATE from TRIAL_DATA " \
                  "union all " \
                  "select STATIONID,METERID,AVERGERROR,ITEMNAME,TRIAL_DATE from TRIAL_DATA_HIS) T " \
                  "where T.ITEMNAME = '日计时误差' " \
                  "and T.TRIAL_DATE " \
                  "between to_date('{0}','yyyy-mm-dd hh24:mi:ss') " \
                  "and to_date('{1}','yyyy-mm-dd hh24:mi:ss')".format(startdate, enddate)
            cur.execute(sql)
            rows = cur.fetchall()
            cur.close()
            cnxn.close()
            return rows
        except:
            traceback.print_exc()
            return []