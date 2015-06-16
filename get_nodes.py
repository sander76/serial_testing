import argparse
from rq import rqSet

__author__ = 'sander'
import serial

parser=argparse.ArgumentParser()
parser.add_argument('port',type=str)



if __name__=="__main__":
    ser=None
    try:
        rq_set = rqSet()
        alive=True
        args = parser.parse_args()
        ser=serial.Serial(args.port,timeout=5)
        ser.write(b'!000v?;')
        end_comm = bytes(';','ascii')
        cmd=bytearray()
        while alive:
            #print ("alive?: {}".format(alive))
            rq_in = ser.read(1)
            if rq_in != b'':
                if rq_in==end_comm:
                    cmd.extend(rq_in)
                    rq_set.parse(cmd)

                    cmd=bytearray()
                else:
                    cmd.extend(rq_in)
            else:
                print("serial timeout")
                alive=False

    finally:
        rq_set.save_json()
        ser.close()