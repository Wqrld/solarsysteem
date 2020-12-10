#!/usr/bin/python3
import serial
import json
import requests
import sys
import datetime
import time
hexbytes = []
maxbyte = bytes.fromhex("FF")
with open('config.json') as configfile:
  data = configfile.read()
config = json.loads(data)

ser = serial.Serial(port= '/dev/ttyUSB0', timeout= 5)  # open serial port
#ser.close()
print(ser.name)         # check which port was really used
#ser.write(bytes.fromhex("01 01 FF FF B6 00 00 00 B6"))     # write a string


with open('adres.txt', 'w+') as adresbestand:
  adres = adresbestand.read()
  if adres == "":
    ser.write(bytes.fromhex("00 00 FF FF C1 00 00 00 BF"))
    address = ser.read(9)[2:4]
    adresbestand.write(str(address))

#print the ID, these should be put as the first to bytes of every request.
#ser.write(bytes.fromhex("00 00 FF FF C1 00 00 00 BF"))    #identify omvormer
#print(ser.read(9))


# the last byte is the right byte of the sum of all bytes (excluding the last ofcourse)
ser.write(bytes.fromhex("C0 05 FF FF B6 00 00 00 79"))

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
  dc = str(round(int.from_bytes(reading1[0:2], "little") * int.from_bytes(reading1[2:4], "little") / 100 + int.from_bytes(reading2[0:2], "little") * int.from_bytes(reading2[2:4], "little") / 100, 2)) # V * A / 100
  ac = str(reading1[10] + reading2[10])
  wtot1 = int.from_bytes(reading[20:23], "little") / 100
  wtot2 = int.from_bytes(reading[51:54], "little") / 100
  runtime = int.from_bytes(reading[24:27], "little")
  print(reading[20:23])
  x = requests.post('https://novumzon.wqrld.net/newdata', json={"apikey": config['apikey'], "wattTotaal": str(round(wtot1 + wtot2, 2)), "wattDC": dc, "wattAC": ac, "runtime": runtime }, headers = {"apikey": config['apikey']})
  print(x.text)
  ser.close()             # close port
