import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime



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
    rows = 1
    col = 2
    
    x_len, y_len, xt_len, yt_len = len(X), len(Y), len(Xtext), len(Ytext)
    
    if not (x_len == y_len and y_len == xt_len and xt_len == yt_len):
        raise TypeError("Arguments are not of the same size")
    
    # if (x_len + 1) > col:
    #     col += (x_len+1)
    #     col /= 3
    #     # col += 1
        
    # if col > 1:
        
    fig, ax = plt.subplots(rows, col, figsize=(9, 7), dpi=140, tight_layout=True)
    # ax.ticklabel_format(useOffset=False, style='plain')
    ctr = 1
    for i in range(x_len):
        plt.subplots_adjust(left=0.125, bottom=0.001, right=0.9, top=0.9, wspace=0.2, hspace=0.2)
        plt.ticklabel_format(useOffset=False, style='plain')
        fig.add_subplot(int(rows), int(col), ctr)
        plt.plot(X[i], Y[i])
        plt.ylabel(Ytext[i])
        plt.xlabel(Xtext[i])
        plt.grid(True)
        ctr+=1

    # fig, ax = plt.subplots(1, 2)
    # fig.canvas.set_window_title('OIT Readings Input values')
    # # ax[0, 0].set_title('(Vin, Iin, Pin, Duty)')
    # ax[0, 0].plot(X[0], Y[0], label="sadsad", color='r')
    # ax[0, 0].set_xlabel("Time (seconds)")
    # ax[0, 0].set_ylabel(Ytext[0], color='r')
    # ax[0, 0].legend(loc='upper left')
    # ax2 = ax[0, 0].twinx()
    #
    # ax2.plot(X[1], Y[1], label=Ytext[1],color='g')
    # ax2.set_ylabel(Ytext[1], color='g')
    # ax2.legend(loc='upper right')
    # ax3 = ax[0, 0].twinx()
    #
    # ax3.plot(X[2], Y[2], label=Ytext[2],color='g')
    # ax3.set_ylabel(Ytext[2], color='g')
    # ax3.legend(loc='upper right')
    # ax4 = ax[0, 0].twinx()


#     plt.pause(0.1)

def main():
    IDEAL_V = 18.2

    # path = '2022_8_12_IN.csv'
    path = 'final-data.csv'
    data = readData(path)

    # print(data['V'], data['P'])

    # t = getTime(data['datetime'])
    t = data['t']
    v = data['Vin']
    i = data['Iin']
    p = data['Pin']
    d = data['Duty']
    v2 = data['Vout']
    i2 = data['Iout']
    p2 = data['Pout']
    in_Yarr = [v, i, p, d, v2, i2, p2]
    in_Xarr = [t, t, t, t, t, t, t]
    in_YTarr = ["Vin", "Iin", "Pin", "Duty", "Vout", "Iout", "Pout"]
    in_XTarr = ["Time", "Time","Time","Time", "Time", "Time","Time"]
    
    plot(in_Xarr, in_Yarr, in_XTarr, in_YTarr)
    # plot(out_Xarr, out_Yarr, out_XTarr, out_YTarr)

    # duty_calc(t, v, i, p)
    
    # makecsv()
    plt.show()



if __name__=="__main__":
    print("Script is being ran directly...")
    main()