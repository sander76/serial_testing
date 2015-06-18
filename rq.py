import json
import time
import logging

lgr=logging.getLogger(__name__)

__author__ = 'sander'

class rqSet():
    def __init__(self):
        self.nodes=[]
        self.log_list=TimedList()

    def parse(self,raw):
        address = self.get_address(raw)
        node =self.get_node(address)
        if node:
            #node.raw_history.new_feedback(self.get_rawfeedback(raw))
            node.log_feedback(self.get_rawfeedback(raw))
        else:
            node = rqBaseNode(self.log_list,address=address)
            self.nodes.append(node)

    def get_rawfeedback(self,raw):
        return raw[4:]

    def get_address(self,raw):
        return raw[1:4]

    def get_node(self,address):
        node = next((nd for nd in self.nodes if nd.address==address),None)
        return node

    def save_json(self):
        with open("nodes.json","w") as fl:
            json.dump(self.nodes,fl,default=rqBaseNode.to_json)

    def from_json(self,file_path):
        with open(file_path,'r') as fl:
            js = json.load(fl)
        for ndjs in js:
            nd = rqBaseNode(self.log_list)
            for key,val in ndjs.items():
                if key == "raw_history" or key == "current_raw":
                    pass
                elif type(val)==str:
                    setattr(nd,key,bytes(val,'ascii'))
                else:
                    setattr(nd,key,val)
            self.nodes.append(nd)

class TimedList(list):
    # def __init__(self,iterable=None):
    #     list.__init__(self,iterable)

    def new_uplink(self,uplink_command):
        lgr.info("new uplink command: {}".format(uplink_command))
        upl = ((time.time(),[uplink_command]))
        self.append(upl)
        return upl

    # def new_feedback(self,feedback):
    #     lgr.info("    new feedback : {}".format(feedback))
    #     self[-1][1].append(feedback)
    #
    # def append(self, p_object):
    #     self.append((time.time(),p_object))
def uplink_decorator(func):
    def wrapper(self,*args):
        c = func(self,*args)
        self.current_raw = self.raw_history.new_uplink(c)
        return c
    return wrapper

class rqBaseNode():
    @staticmethod
    def to_json(obj):
        if type(obj)==bytes or type(obj)==bytearray:
            return obj.decode(encoding='UTF-8')
        return obj.__dict__

    def report(self):
        return ("{} {}".format(self.to_string(self.address),self.to_string(b' '.join(self.raw_history))))

    def log_feedback(self,raw):
        self.current_raw[1].append(raw)

    def to_string(self,byte_array):
        return byte_array.decode(encoding='UTF-8')

    def __init__(self,raw_list,serial=None,address=None):
        self.address=address
        self.raw_history=raw_list
        self.serial=serial
        self.current_raw=[]

    @uplink_decorator
    def get_version(self):
        c = bytearray(b'!')
        c.extend(self.address)
        c.extend(b"v?;")
        return c

    @uplink_decorator
    def get_lift_and_tilt(self,lift,tilt):
        c=bytearray(b'!')
        c.extend(self.address)
        c.extend(b"m")
        c.extend(bytes(str(lift),encoding='ascii'))
        c.extend(b"b")
        c.extend(bytes(str(tilt),encoding='ascii'))
        c.extend(b";")
        return c

    @uplink_decorator
    def get_move(self,move):
        c=bytearray(b'!')
        c.extend(self.address)
        c.extend(b"m")
        c.extend(bytes(str(move),encoding='ascii'))
        c.extend(b";")
        return c



