import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# --------------------- initial values ----------------------------- #

DUTY = 0  # Duty initial
delay = 1000
inc = 2  # duty increment
vcali = 1  # in calibration
icali_in = (1)  # in Current correction value

# 10kHz
Range = 96
Clock = 20

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

def plot(x, y, xtext, ytext):
    plt.figure(figsize=(10, 4), dpi=80)
#     plt.cla()
    plt.scatter(x, y)
    plt.ylabel(ytext)
    plt.xlabel(xtext)
    plt.grid(True)
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


# --------------CSV maker function---------------------
def makecsv():
    today1 = datetime.datetime.today()
    year = str(today1.year)
    month = str(today1.month)
    day = str(today1.day)
    csv1 = year + '_' + month + '_' + day + '.csv'
    l1 = [date, v1, i1, p1, trueDuty]
    x = open(csv1, 'a')
    writer = csv.writer(x, lineterminator='\n')
    writer.writerow(l1)

miLim = int(Range * 0.1)  # Duty minimum
maLim = int(Range * 1)  # Duty maximum
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
    path = 't2.csv'
    data = readData(path)
    # print(data['V'], data['P'])

    t = getTime(data['datetime'])
    v = data['V']
    p = data['P']
    d = data['D']
    
    vout = []
    for i in range(len(d)):
        temp = (1 / (1 - float( d[i] / 100 ) )) * v[i]
        vout.append(temp)
    
    # plot(t, v, "x", "Input Voltage")
    # plot(t, d, "x", "Duty(alpha)")
    res = []
    [res.append(x) for x in p if x not in res]
    plot(v, p, "x", "Input Power")
    # plot(t, vout, "x", "Generated Voltage")
    
    # makecsv()
    plt.show()



if __name__=="__main__":
    print("Script is being ran directly...")
    main()