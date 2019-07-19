import crcmod
import time
import serial
import binascii
import errno
import json
import sysv_ipc
import logging
from os import path
import redis
import fcntl, socket, struct


FOURBYTES_LENGTH=8
THREEBYTES_LENGTH=6     
TWOBYTES_LENGTH=4
ONEBYTE_LENGTH=2
CRC_FORMAT='crc-16-mcrf4xx'
STRANDERD_FRAME_LENGTH=60

data ={
"epc": 0X12,
"time":0X22,
"antena": 1
}

red=redis.Redis(
    host="127.0.0.1",
    port=6379)

ser = serial.Serial(
  
   port='/dev/ttyUSB0',
   baudrate = 57600,
   parity=serial.PARITY_NONE,
   stopbits=serial.STOPBITS_ONE,
   bytesize=serial.EIGHTBITS,
   timeout=1
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# create a file handler
print("generating log file")
basepath = path.dirname(__file__)
handler = logging.FileHandler(basepath+"readerdata.log","a+")
handler.setLevel(logging.DEBUG)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)

def readdata(ser):
    try:
	return ser.readline()
    except IOError, e:
	if e.errno != errno.EINTR:
	    #raise   
	    None

def len_frame(sample):
    length=sample[0:ONEBYTE_LENGTH]
    #print(length)
    length=int(length,16)
    length=length*ONEBYTE_LENGTH
    #print(length)
    return length+ONEBYTE_LENGTH

def crc_check(message):
    # print("****************************\n")
    length=len_frame(message)                   
                                            
    frame_crc= message[length-TWOBYTES_LENGTH:]                      # remove CRC
    # print(frame_crc)
    message=message[:length-TWOBYTES_LENGTH]

    # print(message)
    z=message.decode("hex")
    message1 = z
    crc16 = crcmod.predefined.Crc('crc-16-mcrf4xx')
    crc16.update(message1)
    crc = crc16.hexdigest()
    # print(crc)

    return message
    
def crc_checkTest(message):
    # print("****************************\n")
    length=len_frame(message)                   
                                            
    frame_crc= message[length-TWOBYTES_LENGTH:]                      # remove CRC
    # print(frame_crc)
    message=message[:length-TWOBYTES_LENGTH]

    # print(message)
    z=message.decode("hex")
    message1 = z
    crc16 = crcmod.predefined.Crc('crc-16-mcrf4xx')
    crc16.update(message1)
    crc = crc16.hexdigest()
    # print(crc)
    if frame_crc==crc:
        return True
    else:
        return False

    return message


def get_frame(sample):
    length=len_frame(sample)
    #if(length >= STRANDERD_FRAME_LENGTH):
    #    return None
    sample=crc_check(sample[:length])
    # print(sample)
    sample = sample[:length]
    return sample

def verfy_cmd(frame):
    # print(frame)
    cmd=frame[TWOBYTES_LENGTH:THREEBYTES_LENGTH]
    # print(cmd)
    cmd=int(cmd,16)*ONEBYTE_LENGTH
    # print(cmd)
    if cmd == 476:
        frame = frame[6:]
    else:
        frame = ""
    return frame

def verfy_status(frame):
    # print(frame)
    cmd=frame[:ONEBYTE_LENGTH]
    # print(cmd)
    cmd=int(cmd,16)*ONEBYTE_LENGTH
    # print(cmd)
    if cmd == 00:
        frame = frame[2:]
    else:
        frame = ""
    return frame

def get_antena(frame):
    # print(frame)
    length=FOURBYTES_LENGTH+FOURBYTES_LENGTH+TWOBYTES_LENGTH
    antena=frame[length:length+ONEBYTE_LENGTH]
    # print(antena)
    return antena

def get_EPC(frame):
    # print(frame)
    length=FOURBYTES_LENGTH+FOURBYTES_LENGTH+TWOBYTES_LENGTH+ONEBYTE_LENGTH
    EPC=frame[length+ONEBYTE_LENGTH:]
    # print(EPC)
    return EPC

def getHwAddr(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', ifname[:15]))
    return ':'.join(['%02x' % ord(char) for char in info[18:24]])

 

ser.flushInput()
ser.flushOutput()                               #main program 
raw=""
MAC=getHwAddr('eth0:')

while True:
    x=readdata(ser)
    # print(x)

    if x != None:
        new_data = binascii.hexlify(x).decode('utf-8')
        print(new_data)
              
        index=new_data.find("05004400704c") 
        if index != -1:
            new_data = new_data[:index]+new_data[index+12:]
        
        raw=raw+new_data
        print(raw)
        print(len(raw))
        
        index=raw.find("1d00ee00")
        raw=raw[index:]                      
            
        if(len(raw) ==0):
            continue
        
        while (len(raw) >= STRANDERD_FRAME_LENGTH) :
            block = get_frame(raw)                          #getting first frame from raw
            frame = block
            print(frame)
            
            length=len_frame(frame)                         #verifing data frame break clear 

            if (length == (len(frame)+TWOBYTES_LENGTH)):
                position=raw.find(block)                    #removing frame from raw
                raw=raw[length:]
                                                            #verifing buffer command clear 
                if (length!=STRANDERD_FRAME_LENGTH):
                    continue
                else:
                    frame=verfy_cmd(frame)
                    # print(frame)
                    frame=verfy_status(frame)
                    # print(frame)

                    ts=time.time()                           #time filling
                    data["time"]=ts

                    data["antena"]=get_antena(frame)         #antena number filling 

                    data["epc"]=get_EPC(frame)                  #EPC filling 
                    print(data)
                    json_data=json.dumps(data)
                    print(json_data)
                    red.rpush(MAC, json_data)
