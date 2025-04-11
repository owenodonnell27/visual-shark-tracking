import os
import glob
import datetime

# TODO: move over _setDTfromIMG() and _setDTPCK() to coral_fswebcam?
import coral_fswebcam as cam
try:
  from periphery import Serial
except:
  pass

'''
NOTE:
- run this file with sudo
- modify the baud rate, uart peripheral, etc.


device path   | pin func  | pin
--------------+-----------+-----
/dev/ttymxc2  | UART3_TXD | 7
/dev/ttymxc2  | UART3_RXD | 11
--------------+-----------+-----
/dev/ttymxc0  | UART1_TXD | 8
/dev/ttymxc0  | UART1_RXD | 10
'''

# specific to the Coral Dev Board
UART_PERIPHERY = {
  "UART1": "/dev/ttymxc0",
  "UART3": "/dev/ttymxc0"
}

UARTN = "UART1"
UARTN_PATH = UART_PERIPHERY[UARTN]
BAUD_RATE = 9600
_VERBOSE_MODE = False

_uart = None
_img_dt = None

# :)
_dt_bytes = 0x00
_full_pck_bytes = 0x00


def beginSerial():
  global _uart
  _uart = Serial(UARTN_PATH, BAUD_RATE)
  return 0

def closeSerial():
  _uart.close()
  return 0

def _setBaudRate(baud):
  global BAUD_RATE
  BAUD_RATE = baud
  if _uart is not None:
    closeSerial()
    return beginSerial()
  return 0

def pollSerial(timeout=None):
  return _uart.poll(timeout)

def flushSerial():
  return _uart.flush()

def writeSerial(msg):
  uart_msg = str.encode(msg)
  if _VERBOSE_MODE: print(f"msg sent to {UARTN} with path {UARTN_PATH} with baud rate {BAUD_RATE}")
  return _uart.write(uart_msg) # returns number of bytes written

def readSerial(length, timeout=None):
  return _uart.read(length, timeout) # returns the data read

# def getDTfromIMG():
#   img_filename = ""
#   # len > 0
#   if len(cam._full_filename):
#     if _VERBOSE_MODE: print("file specified in coral_fswebcam")
#     img_filename = os.path.basename(cam._full_filename)
#   else:
#     if _VERBOSE_MODE: print("file found automatically")
#     img_files = glob.glob(f"{cam._cur_dir}/*{cam.FILE_FORMAT}")
#     # len == 0
#     if not len(img_files): return -1
#     img_filename = max(img_files, key=os.path.getctime) # get the most recent img
  
#   img_filename = os.path.basename(img_filename) # get the img basename
#   # rstrip and lstrip format and prefix respectively
#   img_filename = img_filename.lstrip(cam.FILENAME_PREFIX).rstrip(cam.FILE_FORMAT)
#   img_dt_lst = img_filename.split(cam.FILENAME_DELIMITER) # split from delimiter
#   # hm = img_dt_lst.pop()
#   # img_dt_lst.extend([hm[:2], hm[2:]])

#   # extract the datetime from the filename
#   # year, month, day, hour, minute, second
#   _img_dt = datetime.datetime(*map(int, img_dt_lst))
#   if _VERBOSE_MODE:
#     print(img_dt_lst)
#     print(_img_dt)
#   return 0


# NOTE: this function is deprecated, somebody please clean up
def _setDTfromIMG():
  global _img_dt
  # TODO: implement feature, pull name from global cam._full_filename in coral_fswebcam?
  # get the most recent file

  img_files = glob.glob(f"{cam.getDirectory()[0]}/*{cam.FILE_FORMAT}")
  # no file detected in directory
  if not len(img_files): return -1

  img_file_path = max(max(img_files, key=os.path.getctime))
  # strips the file path from the img
  img_filename = os.path.basename(img_file_path)
  # lstrip and rstrip will skip if substr arg not found in str
  img_filename = img_filename.lstrip(cam.FILENAME_PREFIX).rstrip(cam.FILE_FORMAT)
  idt = img_filename.split(cam.FILENAME_DELIMITER)
  _img_dt = datetime.datetime(*map(int, idt))

def _setDTfromIMG():
  if not len(cam.getFilename()): raise FileNotFoundError("Must capture image first with fswebcam!")

  img_filename = cam.getFilename()
  img_filename = os.path.basename(img_filename)
  img_filename = img_filename.lstrip(cam.FILENAME_PREFIX).rstrip(cam.FILE_FORMAT)
  idt = img_filename.split(cam.FILENAME_DELIMITER)
  _img_dt = datetime.datetime(*map(int, idt))

  if _VERBOSE_MODE:
    print(idt)
    print(_img_dt)
  return 0


## NOTE: originally thought that there were only 20 bytes of data available, we have max 229 bytes available.
## hence the compression with conversion to hex, not really necessary tbh
## probably allow faster inter-board TX but like seriously? this is not a speed issue
##
## from: https://github.com/ClusterDuck-Protocol/ClusterDuck-Protocol/blob/master/src/CdpPacket.h
##
## |0       |8       |16  |20|21|22|23  |27                                   255|
## |        |        |    |  |  |  |    |                                        |
## +--------+--------+----+--+--+--+----+----------------------------------------+
## | SDUID  | DDUID  |MUID|T |DT|HC|DCRC|                 DATA                   |
## |        |        |    |  |  |  |    |            (max 229 bytes)             |
## +--------+--------+----+--+--+--+----+----------------------------------------+
#
## SDUID:     08  byte array          - Source Device Unique ID
## DDUID:     08  byte array          - Destination Device Unique ID
## MUID:      04  byte array          - Message unique ID
## T   :      01  byte value          - Topic (topic 0..15 are reserved for internal use)
## DT  :      01  byte value          - Duck Type 
## HC  :      01  byte value          - Hop count (the number of times the packet was relayed)
## DCRC:      04  byte value          - Data section CRC
## DATA:      229 byte array          - Data payload (e.g sensor read, text,...)



# TODO: decide whether to deprecate this or not
def _setDTPCK():

  # packet structure (in bytes)
  # 0x YY | YM | DD | hh | mm --> 5 bytes
  # NOTE: 12 bits for year (YYY), 4 for month (M)
  # ex. 2025 04 31 10:47am --> 0x7e941f0a2f
  global _dt_bytes

  # prev implementation, slower than just accessing attributes
  ## dt_list = list(map(int, _img_dt.timetuple()[:5]))
  ## for i in range(len(dt_list)):
  ##   _dt_bytes <<= 4*(len(hex(dt_list[i]))-2);
  ##   _dt_bytes |= dt_list[i]
 
  _dt_bytes <<= 12
  _dt_bytes |= _img_dt.year

  _dt_bytes <<= 4
  _dt_bytes |= _img_dt.month

  _dt_bytes <<= 8
  _dt_bytes |= _img_dt.day

  _dt_bytes <<= 8
  _dt_bytes |= _img_dt.hour

  _dt_bytes <<= 8
  _dt_bytes |= _img_dt.minute

  return _dt_bytes

if __name__ == "__main__":
  # _VERBOSE_MODE = True
  # getDTfromIMG()
  # print()
  # cam._TEST_MODULE = True
  # cam._VERBOSE_MODE = True
  # cam.capture()
  # print(cam._full_filename)
  # print()

  _VERBOSE_MODE = True
  cam._VERBOSE_MODE = True
  print(cam.getDirectory()[1])

  