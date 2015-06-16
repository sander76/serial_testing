import time

__author__ = 'sander'

def test():
    while 1:
        time.sleep(10)

if __name__=="__main__":
    try:
        test()
    except KeyboardInterrupt as e:
        print ("exiting")