#!/usr/bin/python3
import serial
import requests
import sys
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import pymysql
import datetime
import time
hexbytes = []
maxbyte = bytes.fromhex("FF")
print(open("mysqlpassword.txt", "r").read())
db = pymysql.connect("localhost", "admin", open("mysqlpassword.txt", "r").read().strip(), "stats")
cursor = db.cursor()

ser = serial.Serial(port= '/dev/ttyUSB0', timeout= 5)  # open serial port
#ser.close()
print(ser.name)         # check which port was really used
#ser.write(bytes.fromhex("01 01 FF FF B6 00 00 00 B6"))     # write a string
ser.write(bytes.fromhex("C0 05 FF FF B6 00 00 00 79"))
#\x11\x00\x00\x00\xB6\x00\x00\x00\xC7
#ser.write(bytes.fromhex("00 00 FF FF C1 00 00 00 79"))    #identify omvormer
#counter = 1
#while(True):
#  print(ser.read(1))
#  counter = counter + 1
#  print(counter)
counter = 0
f = open('/var/www/html/datafile.txt','a')
reading = ser.read(62)
if reading[0] == 255 and reading[1] == 193: #if the first 255 byte falls off, dumb serial implementation
  print("adding 255")
  reading = maxbyte + reading
subreading = reading[8:62]
reading1 = subreading[0:23]
reading2 = subreading[31:59]
if reading[2] == 255:
  print("error")
else:
  print(reading.hex())
  print("\n")
  f.seek(0)
  f.truncate()
#  for i in range(len(reading)):
#    f.write(str(i) + " ")
#  f.write("\n")
  f.write("".join(str(x) + " " for x in reading))
  f.write("\n")
  f.write("".join(str(x) + " " for x in reading1))
  f.write("\n")
  f.write("".join(str(x) + " " for x in reading2))
  f.write("\n")
  dc = str(round(int.from_bytes(reading1[0:2], "little") * int.from_bytes(reading1[2:4], "little") / 100 + int.from_bytes(reading2[0:2], "little") * int.from_bytes(reading2[2:4], "little") / 100, 2)) # V * A / 100
#  dc = str(int.from_bytes(reading[0:1], "little")
#  if(float(dc) > 8000):
#    print(dc + "DC is too high, exiting")
#    sys.exit()
  ac = str(reading1[10] + reading2[10])
  wtot1 = int.from_bytes(reading[20:23], "little") / 100
  wtot2 = int.from_bytes(reading[51:54], "little") / 100
  runtime = int.from_bytes(reading[24:27], "little")
  print(reading[20:23])
  f.write(str(wtot1) + " + " + str(wtot2) + " = " + str(wtot1 + wtot2) + "kWh totaal \n")
  f.write(dc + " Watt DC\n")
  f.write(ac + " Watt AC\n")
  f.write(str(runtime) + " Minuten runtime = " + str(runtime / 60 / 24 / 365.25) + " Jaar")
 # x = requests.post('https://novumzon.wqrld.net/newdata', json={"apikey": "s7s5asdu87sj4sdhasdhgJFSADSFSDFSDFSDF78s9ydhf7864sd568f4sdf6g4dfh8g5dhf4G%DFg3d5fg7df", "wattTotaal": str(round(wtot1 + wtot2, 2)), "wattDC": dc, "wattAC": ac, "runtime": runtime })
  x = requests.post('https://novumzon.wqrld.net/newdata', json={"apikey": "s7s5asdu87sj4sdhasdhgJFSADSFSDFSDFSD8g5dhf4G%DFg3d5fg7df", "wattTotaal": str(round(wtot1 + wtot2, 2)), "wattDC": dc, "wattAC": ac, "runtime": runtime })
  print(x.text)
  if(float(dc) > 8000):
    print(dc + "DC is too high, exiting")
    sys.exit()
#  f.write()
  if float(dc) != 0:
    cursor.execute('insert into readings values("' + str(datetime.datetime.now().date()) + '","' + str(datetime.datetime.now().strftime('%H:%M')) + '","' + dc + '","' + ac + '")')
    db.commit()
  cursor.execute("select * from readings where date = '" + str(datetime.datetime.now().date()) + "' group by time order by STR_TO_DATE(time, '%H:%M') DESC LIMIT 50")
  results = cursor.fetchall()
  times = []

  values = []
  results = sorted(results)
  for row in results:
#    datething = datetime.datetime.strptime(row[0] + " " + row[1], "%Y-%m-%d %H:%M")
    times.append(row[1])
#    times.append(matplotlib.dates.date2num)
    values.append(float(row[2]))
  #times = mdates.date2num(times)
  plt.plot(times, values ,color = 'blue')
 # plt.plot([13:27,13:28,13:29],[\\\\\\)
  plt.title('Stroomopwekking voor het omvormen')
  #plt.xaxis.set_major_locator(mdates.HourLocator())
  plt.xlabel('Tijd')
  plt.ylabel('Watt DC')
  plt.ylim(bottom=0)
 # plt.figure(figsize=(10,20))
  plt.savefig('/var/www/html/plot.png')
#for x in reading[1]:
#3  hexbytes.append('' + reading + ' ')


#print(reading)
#print(counter)
#print(ser.read(1))
  ser.close()             # close port
