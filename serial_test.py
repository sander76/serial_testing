import argparse
import time
from rq import rqSet

__author__ = 'sander'
import serial
import threading
import logging

lgr =logging.getLogger(__name__)

parser=argparse.ArgumentParser(description="serial tester")
parser.add_argument("port",type=str)
parser.add_argument("interval",type=float,help='send interval in seconds.')
parser.add_argument('addresses',type=str)



class Test():
    end_comm = bytes(';','ascii')
    def __init__(self,port,interval,addresses):
        self.ser = serial.Serial(port=c_port,timeout=1)
        self.alive=True
        self.rq_set=rqSet()
        self.rq_set.from_json(addresses)

        self.t = threading.Thread(target=self.read_serial)
        self.t.setDaemon(True)
        self.t.start()

        self.move=0
        self.increase=10
        for i in range(20):
            if self.move==90:
                self.increase=-10
            elif self.move==10:
                self.increase=10
            self.move+=self.increase
            for node in self.rq_set.nodes:
                self.ser.write(node.get_move(self.move))
            time.sleep(50)

        # wait for all feedback to arrive.
        time.sleep(40)
        self.alive=False
        with open("log_result.txt",'w') as fl:
            for itm in self.rq_set.log_list:
                st = ",".join((str(x,encoding='ascii').ljust(10) for x in itm[1]))
                lgr.debug(st)
                fl.write(st+"\n")
        lgr.debug("closing connection")
        self.ser.close()
        self.t.join()


    def read_serial(self):
        cmd = bytearray()
        while self.alive:
            rq_in = self.ser.read(1)
            if rq_in != b'':
                if rq_in==Test.end_comm:
                    self.rq_set.parse(cmd)
                    cmd=bytearray()
                else:
                    cmd.extend(rq_in)
            else:
                lgr.debug("serial time out")
        lgr.debug("closing reading thread")





if __name__=="__main__":
    #alive=True
    logging.basicConfig(level=logging.DEBUG)
    args= parser.parse_args()
    c_port = args.port
    interval = args.interval
    addres_file = args.addresses

    tester=Test(c_port,interval,addres_file)
    #rq_set = rqSet()
    #rq_set.from_json(addres_file)
    #print("amount of nodes: {}".format(len(rq_set.nodes)))
    #commands_sent=0
    #ser = serial.Serial(args['port'],baudrate=115200)
    #ser = serial.Serial(port=c_port,timeout=1)
    # for node in rq_set.nodes:
    #     time1=time.time()
    #     #vers = node.get_version()
    #     vers=node.get_lift_and_tilt()
    #     #vers=node.get_move()
    #     ser.write(vers)
    #
    #     if interval:
    #         time.sleep(interval)
    #     time2=time.time()
    #
    #     commands_sent+=1
    #     print ("Command #{} sent to {} sent at timediff {}".format(commands_sent, node.address,time2-time1))
    # # t=threading.Thread(target=read_serial,args=(ser,alive,rq_set))
    # # t.setDaemon(True)
    # # t.start()
    # # # give it some time to fill the serial port.
    # end_comm = bytes(';','ascii')
    # return_count=0
    # cmd = bytearray()
    # while alive:
    #     #print ("alive?: {}".format(alive))
    #     try:
    #         rq_in = ser.read(1)
    #         if rq_in != b'':
    #             if rq_in==end_comm:
    #
    #                 return_count+=1
    #                 rq_set.parse(cmd)
    #                 #print ('rq command returned: {}. Command count: {}'.format(cmd,return_count))
    #                 cmd=bytearray()
    #             else:
    #                 cmd.append(rq_in[0])
    #         else:
    #             print("serial timeout")
    #             #alive=False
    #     except KeyboardInterrupt:
    #         print('keyboard interupt')
    #         alive=False
    # for node in rq_set.nodes:
    #     print(node.report())
