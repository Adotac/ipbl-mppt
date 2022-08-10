# -*- coding: utf-8 -*-
import sys
import wiringpi
import datetime
import csv
# import commands
import subprocess
import argparse

# --------------------- initial values ----------------------------- #

ad_in = 0x41  # voltage_in, current_in
PWM_PIN = 18  # GPIOの18
DUTY = 0  # Duty initial
delay = 1000
inc = 2  # duty increment
vcali = 1  # in calibration
icali_in = (1)  # in Current correction value

# Frequency templates

# 1kHz
# Range=96
# Clock=200

# 2kHz
# Range=120
# Clock=80

# 5kHz
# Range=96
# Clock=40

# 10kHz
Range = 96
Clock = 20

# ------------------- console arguments ------------------------------- #

parser = argparse.ArgumentParser()

# Adding optional argument
parser.add_argument("-d", "--Duty", help="Set initial Duty value")
parser.add_argument("-i", "--D_Increment", help="Set duty incremental value")
parser.add_argument("-r", "--Range", help="Set Range value")
parser.add_argument("-g", "--Graph", help="Show real-time graph plot")

args = parser.parse_args()

if args.Duty:
    DUTY = int(args.Duty)

if args.D_Increment:
    inc = int(args.D_Increment)

if args.Range:
    Range = int(args.Range)
# --------------------------------------------------------------------- #

# Voltage, current, for calibration
in_v = "i2cget -y 1 " + hex(ad_in) + " 0x02 w"
in_c = "i2cget -y 1 " + hex(ad_in) + " 0x04 w"
in_cali = "i2cset -y 1 " + hex(ad_in) + " 0x05 0x0a 0x00 i"

miLim = int(Range * 0.1)  # Duty minimum
maLim = int(Range * 1)  # Duty maximum

# ----------------------Wiringpi config--------------------------
wiringpi.wiringPiSetupGpio()
wiringpi.pinMode(PWM_PIN, wiringpi.GPIO.PWM_OUTPUT)
wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)
wiringpi.pwmSetRange(Range)
wiringpi.pwmSetClock(Clock)
wiringpi.pwmWrite(PWM_PIN, DUTY)


# ---------------------Input Functions------------------------
def GetVin():
    check = subprocess.getoutput(in_v)
    # 	print(in_v)
    # 	print(check)
    V = (int(check[4:6], 16) * 256 + int(check[2:4], 16)) * 1.25 / 1000
    return V * vcali


def GetAin():
    check = subprocess.getoutput(in_c)
    if int(check[4:6], 16) < 128:

        A1 = (int(check[4:6], 16) * 256 + int(check[2:4], 16))
        return int(A1) * icali_in
    else:
        A2 = (int(check[4:6], 16) * 256 + int(check[2:4], 16) - 256 * 256)
        return int(A2) * icali_in


check = subprocess.getoutput(in_cali)


# -------------------Exception handling functions---------------------------------------
def error(address):
    er = "{}No. 1 (input side) sensor is disconnected or has a different number. Please check."
    error = er.format(hex(address))
    print(error)
    wiringpi.delay(3 * delay)


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
    Ddata = "\'" + year + '/' + month + '/' + day + '/' + hour + ':' + minute + ':' + second + "\'"
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

# v1,p1---->new,  v0,p0----->old
# --------------------------MPPT------------------------
def mppt(duty_now):
    case1 = (duty_now <= miLim)  # case when duty ratio reach lower limit
    case2 = (duty_now >= maLim)  # case when duty ratio reach upper limit

    mppt_case1 = (v0 > v1 and p0 > p1) or (v0 < v1 and p0 < p1)
    mppt_case2 = (v0 > v1 and p0 < p1) or (v0 < v1 and p0 > p1)
    # mppt_case3=(v0==v1 or p0==p1)

    if case1 or mppt_case2:
        duty_next = duty_now + inc
        return duty_next
    elif case2 or mppt_case1:
        duty_next = duty_now - inc
        return duty_next
    else:
        duty_next = duty_now
        return duty_next


# --------------------------display data------------------------
def disp():
    d = 'Date: ' + date + '    Vin:' + str(v1) + ' V' + '    Iin:' + str(i1) + ' A' + '    Pin: ' + str(
        p1) + ' W' + '    DUTY: ' + str(DUTY) + ' alpha'
    print(d)


def getTime(timestring):
    t = timestring.replace("'", '')
    t = t.split('/')
    timeObj = datetime.datetime.strptime(t[3], '%H:%M:%S')
    return timeObj


# ---------------------- Just comment if not needed ---------------------
import matplotlib.pyplot as plt


def plot(x, y1, y2, y3, xtext, ytext1, ytext2, ytext3):
    fig = plt.figure('Graph MPPT', figsize=(10, 12), dpi=90, tight_layout=True)
    plt.cla()
    rows = 3
    col = 1

    fig.add_subplot(rows, col, 1)
    plt.plot(x, y1, color='red')
    plt.ylabel(ytext1)
    plt.xlabel(xtext)
    plt.grid(True)

    fig.add_subplot(rows, col, 2)
    plt.plot(x, y2, color='green')
    plt.ylabel(ytext2)
    plt.xlabel(xtext)
    plt.grid(True)

    fig.add_subplot(rows, col, 3)
    plt.plot(x, y3, color='blue')
    plt.ylabel(ytext3)
    plt.xlabel(xtext)
    plt.grid(True)

    plt.pause(0.1)


v_arr, p_arr, d_arr, t_arr = [], [], [], []


def figures():
    v_arr.append(v1)
    p_arr.append(p1)
    d_arr.append(DUTY)
    t_arr.append(getTime(date))
    plot(t_arr, v_arr, p_arr, d_arr, "Time", "Voltage", "Power", "Duty Ratio")


# -----------------------initial measurement------------------------
try:
    v0 = '%.3f' % GetVin()
    i0 = '%.3f' % (GetAin() * 0.001)
    p0 = '%.3f' % (float(v0) * float(i0))
except:
    er1 = "Initial measurement could not be made. Sensor with {} number is disconnected or has the wrong number."
    error1 = er1.format(hex(ad_in))
    print(error1)
    print("Exit programme.")
    sys.exit()

# ---Change Duty---
DUTY += inc
wiringpi.pwmWrite(PWM_PIN, DUTY)
wiringpi.delay(delay)

# main flow here....
try:
    while True:
        # ---input---
        try:
            v1 = '%.3f' % GetVin()
            i1 = '%.3f' % (GetAin() * 0.001)
            p1 = '%.3f' % (float(v1) * float(i1))
        except:
            error(ad_in)
            continue

        # MPPT control for next DUTY change
        DUTY = mppt(DUTY)
        wiringpi.pwmWrite(PWM_PIN, DUTY)
        tDuty = float(DUTY) * 100 / Range
        trueDuty = '%.1f' % tDuty

        # creating or editing csv
        date = Ddata()
        makecsv()
        disp()

        if str(args.Graph) == "True":
            figures()  # Figure functions, uncomment if not needed

        wiringpi.delay(delay)

        v0 = v1
        i0 = i1
        p0 = p1

except KeyboardInterrupt:
    wiringpi.pwmWrite(PWM_PIN, 0)
