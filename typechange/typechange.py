# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import traceback
# date= "2010-01-01"
# datetime.datetime.strptime(date, )
# datestr='2017/5/2 9:53:57'

# def str2date(datestr):
#     if datestr[6] == '/' and datestr[8] == ' ':
#         days = datestr[0:4] + '-' + datestr[5] + '-' + datestr[7] + datestr[8:]
#     elif datestr[6] == '/' and datestr[8] != ' ':
#         days = datestr[0:4] + '-' + datestr[5] + '-' + datestr[7:9] + datestr[9:]
#     elif datestr[7] == '/' and datestr[9] == ' ':
#         days = datestr[0:4] + '-' + datestr[5:7] + '-' + datestr[8] + datestr[9:]
#     elif datestr[7] == '/' and datestr[9] != ' ':
#         days = datestr[0:4] + '-' + datestr[5:7] + '-' + datestr[8:10] + datestr[10:]
#     else:
#         pass
#     date = str(datetime.strptime(days,'%Y-%m-%d %H:%M:%S'))
#     # daylist = days.split('-')
#     # Y = int(daylist[0])
#     # m = int(daylist[1])
#     # d = int(daylist[2])
#     # date = str(datetime.date(Y,m,d))
#     return date
# # print str2date('2017/5/2 9:53:57')
#
# def date2str(date):
#     num=date[0:4]+date[5:7]+date[8:10]
#     return num

def type_change_alert(data):
    try:
        for i in range(len(data)):
            data[i] = list(data[i])
            if data[i][0] >= 9 and data[i][0] <= 18:
                data[i][0] = data[i][0] - 8
            elif data[i][0] >= 23 and data[i][0] <= 32:
                data[i][0] = data[i][0] - 12
            try:
                data[i][2] = float(data[i][2])
            except:
                pass
    except:
        data = []
        traceback.print_exc()
    return data



def type_change_source(data):
    '''
    对数据类型进行预处理
    :param data:
    :return:
    '''
    try:
        result = []
        for i in range(len(data)):
            data[i] = list(data[i])
            try:
                data[i][4] = float(data[i][4])
                # if data[i][1] >= 9 and data[i][1] <= 18:
                #     data[i][1] = data[i][1] - 8
                # elif data[i][1] >= 23 and data[i][1] <= 32:
                #     data[i][1] = data[i][1] - 12
                datestr = data[i][6].strftime('%Y-%m-%d %H:%M:%S')
                data[i][6] = int(datestr[:4] + datestr[5:7] + datestr[8:10])

                data[i][7] = int(data[i][7])

                if data[i][8] == '基本误差P+,H,(1.0Ib,1.0)':
                    data[i][8] = 1
                result.append(data[i])
            except:
                print("存在无效值")
    except Exception as e:
        result = []
        print(e)
    return result

def type_change_insert(data):
    try:
        data = list(data)
        for i in range(len(data)):
            data[i] = list(data[i])
            if str(data[i][0]) == 'nan':
                data[i][0] = str(data[i][0])
        return data
    except Exception as e:
        print(e)
        return []

def type_change_result(data):
    '''
    对数据类型进行预处理
    :param data:
    :return:
    '''
    try:
        for i in range(len(data)):
            data[i] = list(data[i])
            data[i][3] = int(data[i][3])
            data[i][1] = float(data[i][1])
            if data[i][1] != 0:
                data[i][1] = "%.4f" % data[i][1]
            if data[i][2] == 1:
                data[i][2]='负向超差'
            elif data[i][2] == 2:
                data[i][2]='负向高风险'
            elif data[i][2] == 3:
                data[i][2] = '负向偏移'
            elif data[i][2] == 4:
                data[i][2]='正常'
            elif data[i][2] == 5:
                data[i][2]='正向偏移'
            elif data[i][2] == 6:
                data[i][2]='正向高风险'
            elif data[i][2] == 7:
                data[i][2]='正向超差'
            elif data[i][2] == 8:
                data[i][2]='虚拟参考'
            else:
                data[i][2]='未参与评估'
    except Exception as e:
        data = []
        print(e)
    return data

def type_change_hist(data):
    '''
    对数据类型进行预处理
    :param data:
    :return:
    '''
    try:
        for i in range(len(data)):
            data[i] = list(data[i])
            data[i][0] = int(data[i][0])
            if data[i][0] >= 9 and data[i][0] <= 18:
                data[i][0] = data[i][0] - 8
            elif data[i][0] >= 23 and data[i][0] <= 32:
                data[i][0] = data[i][0] - 12
            try:
                data[i][1] = float(data[i][1])
            except:
                data[i][1] = float('nan')


    except Exception as e:
        data = []
        print(e)
    return data

def dateRange(start, end, step=1, format="%Y-%m-%d"):
    strptime, strftime = datetime.strptime, datetime.strftime
    days = (strptime(end, format) - strptime(start, format) + timedelta(days=1)).days
    return [strptime(start, format) + timedelta(i) for i in range(0, days, step)]


# datestr='2017/5/2 00:00:00'
# datechange(datestr)
# dt = '2016-05-05'
# timeArray = time.strptime(dt, "%Y-%m-%d")
# timestamp = time.mktime(timeArray)
# print timestamp
# print type(timestamp)
#
# dt_new = float(time.strftime("%Y%m%d",timeArray))
# print dt_new
# print type(dt_new)
#
# #转换成localtime
# time_local = time.localtime(timestamp)
# #转换成新的时间格式(2016-05-05 20:28:54)
# dt = time.strftime("%Y-%m-%d",time_local)
# print dt
# print type(dt)