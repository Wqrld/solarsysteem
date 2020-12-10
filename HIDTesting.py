import usb.core
import time
import datetime
from array import array
broadcast1 = array("B", [1, 40, 72, 31, 148, 0, 60, 241, 51, 195, 126, 60, 102, 38, 255, 40, 72, 31, 148, 0, 71, 110, 233, 206, 96, 227, 216, 143, 255, 40, 72, 31, 148, 0, 60, 241, 51, 195, 126, 60, 102, 38, 255, 40, 72, 31, 148, 0, 71, 110, 233, 206, 96, 227, 216, 143, 255, 0, 18, 0, 0, 0, 0, 0])
broadcast2 = array("B", [1, 40, 72, 31, 148, 0, 71, 110, 233, 206, 96, 227, 216, 143, 255, 40, 72, 31, 148, 0, 71, 110, 233, 206, 96, 227, 216, 143, 255, 40, 72, 31, 148, 0, 60, 241, 51, 195, 126, 60, 102, 38, 255, 40, 72, 31, 148, 0, 71, 110, 233, 206, 96, 227, 216, 143, 255, 0, 18, 0, 0, 0, 0, 0])

dev = usb.core.find(idVendor=0x1a64, idProduct=0x0000)
oldtime = datetime.datetime.now()
oldbytes = ["not", "initialized"];

if dev is None:
    raise ValueError('Our device is not connected')
#print(dev)
dev.reset()

# set the active configuration. With no arguments, the first
# configuration will be the active one
#dev.set_configuration()

# get an endpoint instance
cfg = dev.get_active_configuration()
intf = cfg[(0,0)]

ep = usb.util.find_descriptor(
    intf,
    # match the first OUT endpoint
    custom_match = \
    lambda e: \
        usb.util.endpoint_direction(e.bEndpointAddress) == \
        usb.util.ENDPOINT_OUT)

assert ep is not None
#print("----------------------------")
#print(ep)
#dev.reset()
if dev.is_kernel_driver_active(0):
    reattach = True
    dev.detach_kernel_driver(0)
usb.util.dispose_resources(dev)
dev.reset()
hexbytes = []

#  dev.write(1, bytes.fromhex('1b 00 60 5a 9e 68 0f 9e ff ff 00 00 00 00 09 00 00 01 00 03 00 81 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00$
#reqbytes = '01 D4 40 1F 94 03 07 5F 00'
reqbytes = '01 2a 83 3c a8'
while len(reqbytes) < 191:
  reqbytes += " 00"
#  print("lenreq: " + str(len(reqbytes)))
#  print("writing")
#dev.write(1, bytes.fromhex(reqbytes), 5000);


#dev.write(1, bytes.fromhex(reqbytes), 5000);
while(True):
  oldtime = datetime.datetime.now()
  dev.write(1, bytes.fromhex(reqbytes), 5000);
  reading = dev.read(0x81, 64, 5000) # moet 64 zijn anders overflow

  print("\nTime Diff")
  print(datetime.datetime.now() - oldtime)
  print("\n\n")
#  print(reading)
#  print(broadcast1)
#  print(reading[1])
  if reading[1] != 40:
    print(reading)
    for i in range(1, len(reading)):
      if len(oldbytes) > 3 and reading[i] != oldbytes[i]:
        print("byte " + str(i) + " changed, old: " + str(oldbytes[i]) + " new: " + str(reading[i]))
    oldbytes = reading
    print("\n\nReading length")
    print(len(reading))
    time.sleep(8)
#  time.sleep(2)
#    print("\nTime Diff")
#    print(datetime.datetime.now() - oldtime)
#    print("\n\n")
#  realdec = reading
    oldtime = datetime.datetime.now()
  time.sleep(3)
#  time.sleep(2000)
#  for x in realdec:
#    hexbytes.append(hex(x))
#  print(hexbytes)
#  print(hexbytes[11] + hexbytes[10])
