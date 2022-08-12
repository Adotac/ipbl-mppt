import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# --------------------- initial values ----------------------------- #

# DUTY = 0  # Duty initial
# delay = 1000
# inc = 2  # duty increment
# vcali = 1  # in calibration
# icali_in = (1)  # in Current correction value

# # 10kHz
# Range = 96
# Clock = 20

# reading csv with pandas
def readData(path):
    data = pd.read_csv(path)
    return data

def getTime(arr):
    temp = []
    for t in arr:
        t = t.replace("'", '')
        tt = t.split('/')
        timeObj = datetime.strptime(tt[3], '%H:%M:%S')
#         print(type(timeObj.time()))
        temp.append(timeObj)

    return temp

def plot(X, Y, Xtext, Ytext):
    
#     plt.cla()
    rows = 3
    col = 1
    
    x_len, y_len, xt_len, yt_len = len(X), len(Y), len(Xtext), len(Ytext)
    
    if not (x_len == y_len and y_len == xt_len and xt_len == yt_len):
        raise TypeError("Arguments are not of the same size")
    
    if (x_len + 1) > col:
        col += (x_len+1)
        col /= 3
        # col += 1
        
    # if col > 1:
        
    fig = plt.figure(figsize=(9, 7), dpi=140, tight_layout=True)
    # ax.ticklabel_format(useOffset=False, style='plain')
    ctr = 1
    for i in range(x_len):
        plt.subplots_adjust(left=0.125, bottom=0.001, right=0.9, top=0.9, wspace=0.2, hspace=0.2)
        plt.ticklabel_format(useOffset=False, style='plain')
        fig.add_subplot(rows, col, ctr)
        plt.plot(X[i], Y[i])
        plt.ylabel(Ytext[i])
        plt.xlabel(Xtext[i])
        # plt.grid(True)
        ctr+=1
        
        
    
#     plt.pause(0.1)

# --------------Datetime processing---------------------
def Ddata():
    today1 = datetime.datetime.today()
    year = str(today1.year)
    month = str(today1.month)
    day = str(today1.day)
    hour = str(today1.hour)
    minute = str(today1.minute)
    second = str(today1.second)
    if int(minute) < 10:
        minute = '0' + minute
    Ddata = "\'" + year + '/' + month + '/' + day + \
        '/' + hour + ':' + minute + ':' + second + "\'"
    return Ddata


# def mppt(duty_now):
#     case1 = (duty_now <= miLim)  # case when duty ratio reach lower limit
#     case2 = (duty_now >= maLim)  # case when duty ratio reach upper limit

#     mppt_case1 = (v0 > v1 and p0 > p1) or (v0 < v1 and p0 < p1)
#     mppt_case2 = (v0 > v1 and p0 < p1) or (v0 < v1 and p0 > p1)
#     # mppt_case3=(v0==v1 or p0==p1)

#     if case1 or mppt_case2:
#         duty_next = duty_now + inc
#         return duty_next
#     elif case2 or mppt_case1:
#         duty_next = duty_now - inc
#         return duty_next
#     else:
#         duty_next = duty_now
#         return duty_next
    
def main():
    # path = '2022_8_12_IN.csv'
    path = '2nd INPUT.csv'
    
    dataIN = readData(path)
    
    path = '2022_8_12_OUT.csv'
    # path = '2nd OUTPUT.csv'
    
    dataOUT = readData(path)
    # print(data['V'], data['P'])

    # t = getTime(dataIN['datetime'])
    t = dataIN['t']
    v = dataIN['Vin']
    i = dataIN['Iin']
    p = dataIN['Pin']
    d = dataIN['Duty']
    
    in_Yarr = [v, i, p, d]
    in_Xarr = [t, t, t, t]
    in_YTarr = ["Voltage Input", "Current Input", "Power Input", "Duty Ratio"]
    in_XTarr = ["Time", "Time","Time","Time"]
    
    t2 = dataOUT['t']
    v2 = dataOUT['Vout']
    i2 = dataOUT['Iout']
    p2 = dataOUT['Pout']
    # d2 = dataOUT['D']
    
    out_Yarr = [v2, i2, p2]
    out_Xarr = [t2, t2, t2]
    out_YTarr = ["Voltage Output", "Current Output", "Power Output"]
    out_XTarr = ["Time", "Time","Time"]
    
    plot(in_Xarr, in_Yarr, in_XTarr, in_YTarr)
    plot(out_Xarr, out_Yarr, out_XTarr, out_YTarr)
    
    # makecsv()
    plt.show()



if __name__=="__main__":
    print("Script is being ran directly...")
    main()