import json

__author__ = 'sander'

class rqSet():
    def __init__(self):
        self.nodes=[]

    def parse(self,raw):
        address = self.get_address(raw)
        node =self.get_node(address)
        if node:
            node.raw_feedback.append(self.get_rawfeedback(raw))
        else:
            node = rqBaseNode(address)
            self.nodes.append(node)

    def get_rawfeedback(self,raw):
        return raw[4:]
    def get_address(self,raw):
        return raw[1:4]

    def get_node(self,address):
        node = next((nd for nd in self.nodes if nd.address==address),None)
        return node

    def save_json(self):
        with open("c://data/aptana/serial_testing/nodes.json","w") as fl:
            json.dump(self.nodes,fl,default=rqBaseNode.to_json)

    def from_json(self,file_path):
        with open(file_path,'r') as fl:
            js = json.load(fl)
        for ndjs in js:
            nd = rqBaseNode()
            for key,val in ndjs.items():
                if type(val)==str:
                    setattr(nd,key,bytes(val,'ascii'))
                else:
                    setattr(nd,key,val)
            self.nodes.append(nd)


class rqBaseNode():
    @staticmethod
    def to_json(obj):
        if type(obj)==bytes or type(obj)==bytearray:
            return obj.decode(encoding='UTF-8')
        return obj.__dict__

    def report(self):
        return ("{} {}".format(self.to_string(self.address),self.to_string(b' '.join(self.raw_feedback))))

    def to_string(self,byte_array):
        return byte_array.decode(encoding='UTF-8')

    def __init__(self,address=None):
        self.address=address
        self.raw_feedback=[]

    def get_version(self):
        c = bytearray(b'!')
        c.extend(self.address)
        c.extend(b"v?;")
        return c

    def get_lift_and_tilt(self):
        c=bytearray(b'!')
        c.extend(self.address)
        c.extend(b"m50b30;")
        return c

    def get_move(self):
        c=bytearray(b'!')
        c.extend(self.address)
        c.extend(b"m50;")
        return c



